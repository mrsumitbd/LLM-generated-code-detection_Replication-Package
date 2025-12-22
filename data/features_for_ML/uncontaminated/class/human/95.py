import asyncio
from typing import Any, Dict
import gem
from gem.wrappers.wrapper_factory import get_wrapper_fns
import logging

class VectorizedGemEnv:

    def __init__(self):
        self.num_envs = NUM_ENVS

        self.available_buckets = asyncio.Queue()
        for i in range(self.num_envs):
            self.available_buckets.put_nowait(i)

        self.episode_to_bucket = {}
        self.episode_to_bucket_lock = asyncio.Lock()

        self.cohort_id_counter = 0
        self.episode_to_cohort_id = {}
        self.cohorts = {}  # cohort_id -> {
        #   "episodes": set(), "done_episodes": set(),
        #   "pending_actions": {}, "pending_futures": {}, "lock": asyncio.Lock()
        # }
        self.cohort_lock = asyncio.Lock()

        self.reset_pending_futures = {}
        self.reset_pending_episodes = {}
        self.reset_lock = asyncio.Lock()

        self.vec_env = gem.make_vec(
            [GAME] * NUM_ENVS,
            vec_kwargs=[{"seed": 233 + i} for i in range(NUM_ENVS)],
            wrappers=get_wrapper_fns(WRAPPERS if WRAPPERS else "", tokenizer=None),
            async_mode=True,
        )

    async def reset_episode(self, extra_info: Dict[str, Any]) -> str:
        episode_idx = extra_info["idx"]

        bucket_idx = await self.available_buckets.get()

        async with self.episode_to_bucket_lock:
            self.episode_to_bucket[episode_idx] = bucket_idx

        future = asyncio.get_running_loop().create_future()

        async with self.reset_lock:
            self.reset_pending_futures[bucket_idx] = future
            self.reset_pending_episodes[bucket_idx] = episode_idx

            if len(self.reset_pending_episodes) == self.num_envs:
                async with self.cohort_lock:
                    cohort_id = self.cohort_id_counter
                    self.cohort_id_counter += 1

                    episodes_in_cohort = set(self.reset_pending_episodes.values())
                    self.cohorts[cohort_id] = {
                        "episodes": episodes_in_cohort,
                        "done_episodes": set(),
                        "pending_actions": {},
                        "pending_futures": {},
                        "lock": asyncio.Lock(),
                    }
                    for ep_idx in episodes_in_cohort:
                        self.episode_to_cohort_id[ep_idx] = cohort_id
                    logging.info(
                        f"[Reset] Created Cohort {cohort_id} with episodes: {episodes_in_cohort}"
                    )

                observations, _ = self.vec_env.reset()

                for bucket_idx in range(self.num_envs):
                    obs = observations[bucket_idx]

                    ep_idx = self.reset_pending_episodes[bucket_idx]
                    fut = self.reset_pending_futures[bucket_idx]

                    template_fn = TEMPLATE_FACTORY.get(
                        PROMPT_TEMPLATE, apply_no_template
                    )
                    formatted_obs = template_fn(obs)

                    if not fut.done():
                        fut.set_result(formatted_obs)

                self.reset_pending_futures.clear()
                self.reset_pending_episodes.clear()

        return await future

    async def step_episode(
        self, state: str, action: str, extra_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        episode_idx = extra_info["idx"]

        if episode_idx not in self.episode_to_cohort_id:
            raise RuntimeError(
                f"Episode {episode_idx} has no cohort. Did you reset it properly?"
            )
        cohort_id = self.episode_to_cohort_id[episode_idx]

        async with self.cohort_lock:
            if cohort_id not in self.cohorts:
                return {
                    "next_state": "",
                    "reward": 0.0,
                    "score": 0.0,
                    "done": True,
                    "extra_info": {},
                }
            cohort = self.cohorts[cohort_id]

        future = asyncio.get_running_loop().create_future()

        async with cohort["lock"]:
            cohort["pending_actions"][episode_idx] = action
            cohort["pending_futures"][episode_idx] = future

            active_episodes = cohort["episodes"] - cohort["done_episodes"]
            if set(cohort["pending_actions"].keys()) == active_episodes:
                logging.info(
                    f"[Step] All active episodes in Cohort {cohort_id} have submitted actions. Triggering step."
                )

                step_actions = [""] * self.num_envs

                async with self.episode_to_bucket_lock:
                    for ep_idx in cohort["episodes"]:
                        bucket_idx = self.episode_to_bucket[ep_idx]
                        if ep_idx in active_episodes:
                            step_actions[bucket_idx] = cohort["pending_actions"][ep_idx]

                pending_futures_copy = dict(cohort["pending_futures"])
                cohort["pending_actions"].clear()
                cohort["pending_futures"].clear()

                obs, rewards, terminateds, truncateds, infos = self.vec_env.step(
                    step_actions
                )

                newly_done_episodes = set()
                async with self.episode_to_bucket_lock:
                    for ep_idx in active_episodes:
                        bucket_idx = self.episode_to_bucket[ep_idx]
                        is_done = terminateds[bucket_idx] or truncateds[bucket_idx]

                        template_fn = TEMPLATE_FACTORY.get(
                            PROMPT_TEMPLATE, apply_no_template
                        )
                        result_dict = {
                            "next_state": template_fn(obs[bucket_idx]),
                            "reward": rewards[bucket_idx],
                            "score": rewards[bucket_idx],
                            "done": is_done,
                            "extra_info": {**infos[bucket_idx], "idx": ep_idx},
                        }

                        fut = pending_futures_copy[ep_idx]
                        if not fut.done():
                            fut.set_result(result_dict)

                        if is_done:
                            newly_done_episodes.add(ep_idx)

                cohort["done_episodes"].update(newly_done_episodes)

                if cohort["done_episodes"] == cohort["episodes"]:
                    logging.info(
                        f"[Step] Cohort {cohort_id} is fully done. Releasing all buckets."
                    )
                    async with self.cohort_lock, self.episode_to_bucket_lock:
                        for ep_idx in cohort["episodes"]:
                            bucket_to_release = self.episode_to_bucket.pop(ep_idx, None)
                            if bucket_to_release is not None:
                                await self.available_buckets.put(bucket_to_release)
                            self.episode_to_cohort_id.pop(ep_idx, None)
                        self.cohorts.pop(cohort_id, None)

        return await future