from launch_darkly_python_sdk.paths.api_v2_webhooks_id.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_webhooks_id.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_webhooks_id.patch import ApiForpatch


class ApiV2WebhooksId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
