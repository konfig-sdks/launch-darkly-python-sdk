from launch_darkly_python_sdk.paths.api_v2_oauth_clients_client_id.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_oauth_clients_client_id.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_oauth_clients_client_id.patch import ApiForpatch


class ApiV2OauthClientsClientId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
