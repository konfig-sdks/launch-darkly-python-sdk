from launch_darkly_python_sdk.paths.api_v2_tokens_id.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_tokens_id.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_tokens_id.patch import ApiForpatch


class ApiV2TokensId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
