from aw.config.main import config
from aw.api_endpoints.base import API_PERMISSION, get_api_user, GenericResponse, BaseResponse, GenericErrorResponse, \
    HDR_CACHE_1W, response_data_if_changed, API_PARAM_HASH
from aw.model.system import SystemConfig, get_config_from_db, SSHHostkeys, SSHHostkeyFile

def get(request):
        data = {
            'read_only': SystemConfig.api_fields_read_only,
            'env_vars': {k: config[k] for k in SystemConfig.get_set_public_env_vars()},
            'settings': {},
        }

        for field in SystemConfig.api_fields_read + data['read_only']:
            data['settings'][field] = config[field]

        data['settings']['mail_pass_is_set'] = get_config_from_db().mail_pass_is_set
        data['read_only'] += data['env_vars'].keys()
        data['read_only'] = list(set(data['read_only']))

        return response_data_if_changed(request, data=data)