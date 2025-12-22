from vagen.server.serial import serialize_observation

def reset_single_env(env_id, seed):     
            env = self.environments[env_id]
            observation, info = env.reset(seed=seed)
            serialized_observation = serialize_observation(observation)
            return env_id, (serialized_observation, info), None