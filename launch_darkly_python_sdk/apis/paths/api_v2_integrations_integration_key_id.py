from launch_darkly_python_sdk.paths.api_v2_integrations_integration_key_id.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_integrations_integration_key_id.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_integrations_integration_key_id.patch import ApiForpatch


class ApiV2IntegrationsIntegrationKeyId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
