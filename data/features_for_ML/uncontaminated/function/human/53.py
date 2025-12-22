from jorvik.utils import databricks, git
from typing import Callable

def get_isolation_provider() -> Callable:
    """ Get the isolation provider for the current Spark session.

        Returns:
            Callable: A function that returns isolation context as a string.
    """
    provider_config = get_spark_config("io.jorvik.storage.isolation_provider", default_value="NO_ISOLATION")

    PROVIDERS = {
        'NO_ISOLATION': get_no_isolation_context,
        'DATABRICKS_GIT_BRANCH': databricks.get_active_branch,
        'DATABRICKS_USER': databricks.get_current_user,
        'DATABRICKS_CLUSTER': databricks.get_cluster_id,
        'GIT_BRANCH': git.get_current_git_branch,
        'ENVIRONMENT_VARIABLE': get_isolation_context_from_env_var,
        'SPARK_CONFIG': get_isolation_context_from_spark_config
    }

    try:
        provider = PROVIDERS[provider_config]
    except KeyError:
        raise ValueError(f"Unknown isolation provider: {provider_config}. Supported providers are: {list(PROVIDERS.keys())}.")  # noqa: E501
    if provider_config != 'NO_ISOLATION':
        _validate_isolation_context(provider())
    return provider