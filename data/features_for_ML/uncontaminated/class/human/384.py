import os
from pathlib import Path
import yaml
from dataclasses import dataclass, field

class ProductionConfig:
    devops: DevopsConfig = field(default_factory=DevopsConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    observability: ObservabilityConfig = field(default_factory=ObservabilityConfig)

    # ------------------------------------------------------------------
    # 1. Load YAML (defaults)
    # ------------------------------------------------------------------
    @classmethod
    def _from_yaml(cls, path: Path) -> "ProductionConfig":
        if not path.exists():
            logger.warning("config.yaml not found – using built-in defaults")
            return cls()
        with path.open() as f:
            data = yaml.safe_load(f) or {}
        return cls(
            devops=DevopsConfig(**data.get("devops", {})),
            agent=AgentConfig(**data.get("agent", {})),
            model=ModelConfig(**data.get("model", {})),
            storage=StorageConfig(**data.get("storage", {})),
            security=SecurityConfig(**data.get("security", {})),
            observability=ObservabilityConfig(**data.get("observability", {})),
        )

    # ------------------------------------------------------------------
    # 2. Override with env vars (same mapping you already had)
    # ------------------------------------------------------------------
    @classmethod
    def _apply_env_overrides(cls, cfg: "ProductionConfig") -> "ProductionConfig":
        # Helper to get int/bool/float safely
        def _int(key, default):
            return int(os.getenv(key, default))

        def _bool(key, default):
            return os.getenv(key, str(default)).lower() == "true"

        def _float(key, default):
            return float(os.getenv(key, default))

        # ---- devops ----------------------------------------------------
        cfg.devops.timeout_seconds = _int("DEVOPS_TIMEOUT", cfg.devops.timeout_seconds)
        cfg.devops.max_output_chars = _int(
            "DEVOPS_MAX_OUTPUT", cfg.devops.max_output_chars
        )
        cfg.devops.enable_history = _bool(
            "DEVOPS_ENABLE_HISTORY", cfg.devops.enable_history
        )
        cfg.devops.max_history_size = _int(
            "DEVOPS_HISTORY_SIZE", cfg.devops.max_history_size
        )
        cfg.devops.working_directory = os.getenv(
            "DEVOPS_WORKING_DIR", cfg.devops.working_directory
        )

        # ---- agent -----------------------------------------------------
        cfg.agent.name = os.getenv("AGENT_NAME", cfg.agent.name)
        cfg.agent.max_steps = _int("AGENT_MAX_STEPS", cfg.agent.max_steps)
        cfg.agent.tool_call_timeout = _int(
            "AGENT_TOOL_TIMEOUT", cfg.agent.tool_call_timeout
        )
        cfg.agent.memory_mode = os.getenv("AGENT_MEMORY_MODE", cfg.agent.memory_mode)
        cfg.agent.memory_window_size = _int(
            "AGENT_MEMORY_WINDOW", cfg.agent.memory_window_size
        )
        cfg.agent.request_limit = _int("AGENT_REQUEST_LIMIT", cfg.agent.request_limit)
        cfg.agent.total_tokens_limit = _int(
            "AGENT_TOKEN_LIMIT", cfg.agent.total_tokens_limit
        )

        # --- Memory Retrieval Config ---
        cfg.agent.memory_results_limit = _int(
            "AGENT_MEMORY_RESULTS_LIMIT", cfg.agent.memory_results_limit
        )
        cfg.agent.memory_similarity_threshold = _float(
            "AGENT_MEMORY_SIMILARITY_THRESHOLD", cfg.agent.memory_similarity_threshold
        )

        # --- Tool Retrieval Config ---
        cfg.agent.enable_tools_knowledge_base = _bool(
            "AGENT_ENABLE_TOOLS_KB", cfg.agent.enable_tools_knowledge_base
        )
        cfg.agent.tools_results_limit = _int(
            "AGENT_TOOLS_RESULTS_LIMIT", cfg.agent.tools_results_limit
        )
        cfg.agent.tools_similarity_threshold = _float(
            "AGENT_TOOLS_SIMILARITY_THRESHOLD", cfg.agent.tools_similarity_threshold
        )

        # --- Memory Tool Backend ---
        cfg.agent.memory_tool_backend = os.getenv(
            "AGENT_MEMORY_TOOL_BACKEND", cfg.agent.memory_tool_backend
        )

        # ---- model -----------------------------------------------------
        cfg.model.provider = os.getenv("MODEL_PROVIDER", cfg.model.provider)
        cfg.model.model = os.getenv("MODEL_NAME", cfg.model.model)
        cfg.model.temperature = _float("MODEL_TEMPERATURE", cfg.model.temperature)
        cfg.model.top_p = _float("MODEL_TOP_P", cfg.model.top_p)
        cfg.model.max_context_length = _int(
            "MODEL_MAX_CONTEXT", cfg.model.max_context_length
        )
        cfg.model.llm_api_key = os.getenv("LLM_API_KEY") or cfg.model.llm_api_key

        # ---- storage ---------------------------------------------------
        cfg.storage.memory_store_type = os.getenv(
            "MEMORY_STORE_TYPE", cfg.storage.memory_store_type
        )
        cfg.storage.event_store_type = os.getenv(
            "EVENT_STORE_TYPE", cfg.storage.event_store_type
        )
        cfg.storage.redis_url = os.getenv("REDIS_URL", cfg.storage.redis_url)
        cfg.storage.redis_max_connections = _int(
            "REDIS_MAX_CONN", cfg.storage.redis_max_connections
        )

        # ---- security --------------------------------------------------
        cfg.security.enable_rate_limiting = _bool(
            "SECURITY_RATE_LIMIT", cfg.security.enable_rate_limiting
        )
        cfg.security.rate_limit_requests = _int(
            "SECURITY_RATE_LIMIT_REQUESTS", cfg.security.rate_limit_requests
        )
        cfg.security.enable_audit_logging = _bool(
            "SECURITY_AUDIT_LOG", cfg.security.enable_audit_logging
        )

        # ---- observability ---------------------------------------------
        cfg.observability.enable_metrics = _bool(
            "OBSERVABILITY_METRICS", cfg.observability.enable_metrics
        )
        cfg.observability.log_level = os.getenv(
            "LOG_LEVEL", cfg.observability.log_level
        )
        cfg.observability.log_format = os.getenv(
            "LOG_FORMAT", cfg.observability.log_format
        )
        cfg.observability.log_file = os.getenv(
            "OBSERVABILITY_LOG_FILE", cfg.observability.log_file
        )
        cfg.security.audit_log_file = os.getenv(
            "SECURITY_AUDIT_LOG_FILE", cfg.security.audit_log_file
        )
        cfg.observability.metrics_port = _int(
            "OBSERVABILITY_METRICS_PORT", cfg.observability.metrics_port
        )

        return cfg

    # ------------------------------------------------------------------
    # Public factory – **single entry point**
    # ------------------------------------------------------------------
    @classmethod
    def load(cls, yaml_path: str = "config.yaml") -> "ProductionConfig":
        cfg = cls._from_yaml(Path(yaml_path))
        cfg = cls._apply_env_overrides(cfg)
        cfg.validate()
        logger.info("Configuration loaded & validated")
        return cfg

    # ------------------------------------------------------------------
    # Validation (unchanged)
    # ------------------------------------------------------------------
    def validate(self) -> None:
        self.devops.validate()
        self.agent.validate()
        self.model.validate()
        self.storage.validate()
        self.security.validate()
        self.observability.validate()