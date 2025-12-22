from syftr.studies import (  # noqa
    LOCAL_EMBEDDING_MODELS,
    Block,
    CritiqueRAGAgent,
    Evaluation,
    FewShotRetriever,
    Hyde,
    LATSRagAgent,
    LLMConfig,
    OptimizationConfig,
    QueryDecomposition,
    ReactRAGAgent,
    Reranker,
    Retriever,
    SearchSpace,
    Splitter,
    StudyConfig,
    SubQuestionRAGAgent,
    TimeoutConfig,
    TopK,
    TransferLearningConfig,
)

def get_optimization_parameters():
    optimization_config = OptimizationConfig(
        method="expanding",
        blocks=BLOCKS,
        shuffle_blocks=False,
        num_trials=NUM_TRIALS,
        baselines=BASELINES,
        baselines_cycle_llms=True,
        shuffle_baselines=True,
        max_concurrent_trials=49,
        num_eval_samples=49,
        num_eval_batch=5,
        rate_limiter_max_coros=30,  # control the number of concurrent evals ...
        rate_limiter_period=60,  # ... per given time unit
        max_trial_cost=40.0,
        cpus_per_trial=1,
        seeder_timeout=None,  # None: wait until finished, 0: don't wait
        # -----------------------------------------------
        # num_random_trials=0,
        num_random_trials=NUM_TRIALS,
        # -----------------------------------------------
        use_individual_baselines=False,
        use_agent_baselines=False,
        use_variations_of_baselines=False,
        # -----------------------------------------------
        use_pareto_baselines=False,  # required for transfer learning
        # -----------------------------------------------
        use_pareto_pruner=True,
        use_cost_pruner=True,
        use_runtime_pruner=True,
        # -----------------------------------------------
        use_toy_baselines=False,
        # -----------------------------------------------
        sampler="tpe",
    )

    for llm in LLMS:
        evaluation = Evaluation(
            mode=EVAL_MODE,
            raise_on_exception=False,
        )
        evaluation.llm_names = [llm]
        yield DATASETS, SEARCH_SPACE, optimization_config, evaluation