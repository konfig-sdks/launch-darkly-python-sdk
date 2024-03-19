from launch_darkly_python_sdk.paths.api_v2_members.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_members.post import ApiForpost
from launch_darkly_python_sdk.paths.api_v2_members.patch import ApiForpatch


class ApiV2Members(
    ApiForget,
    ApiForpost,
    ApiForpatch,
):
    pass
