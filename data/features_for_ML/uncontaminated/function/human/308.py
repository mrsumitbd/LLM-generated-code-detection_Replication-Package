from typing import List, Optional
from derisk_app.base import (
    _create_model_start_listener,
    _migration_db_storage,
    server_init,
)
from derisk_app.config import ApplicationConfig, ServiceWebParameters, SystemParameters
from derisk.model.cluster import initialize_worker_manager_in_client
from derisk_serve.model.serve import Serve as ModelServe
from derisk_app.component_configs import initialize_components
from derisk.model.cluster.storage import ModelStorage

def initialize_app(param: ApplicationConfig, args: List[str] = None):
    """Initialize app
    If you use gunicorn as a process manager, initialize_app can be invoke in
    `on_starting` hook.
    Args:
        param:WebWerverParameters
        args:List[str]
    """

    # import after param is initialized, accelerate --help speed
    from derisk.model.cluster import initialize_worker_manager_in_client

    web_config = param.service.web
    print(param)

    server_init(param, system_app)
    mount_routers(app, param)
    model_start_listener = _create_model_start_listener(system_app)

    # Migration db storage, so you db models must be imported before this
    _migration_db_storage(
        param.service.web.database, web_config.disable_alembic_upgrade
    )

    initialize_components(
        param,
        system_app,
    )
    system_app.on_init()



    # After init, when the database is ready
    system_app.after_init()

    binding_port = web_config.port
    binding_host = web_config.host
    if not web_config.light:
        from derisk.model.cluster.storage import ModelStorage
        from derisk_serve.model.serve import Serve as ModelServe

        logger.info(
            "Model Unified Deployment Mode, run all services in the same process"
        )
        model_serve = ModelServe.get_instance(system_app)
        # Persistent model storage
        model_storage = ModelStorage(model_serve.model_storage)
        initialize_worker_manager_in_client(
            worker_params=param.service.model.worker,
            models_config=param.models,
            app=app,
            binding_port=binding_port,
            binding_host=binding_host,
            start_listener=model_start_listener,
            system_app=system_app,
            model_storage=model_storage,
        )

    else:
        # MODEL_SERVER is controller address now
        controller_addr = web_config.controller_addr
        param.models.llms = []
        param.models.rerankers = []
        param.models.embeddings = []
        initialize_worker_manager_in_client(
            worker_params=param.service.model.worker,
            models_config=param.models,
            app=app,
            run_locally=False,
            controller_addr=controller_addr,
            binding_port=binding_port,
            binding_host=binding_host,
            start_listener=model_start_listener,
            system_app=system_app,
        )

    mount_static_files(app, param)

    # Before start, after on_init
    system_app.before_start()
    return param