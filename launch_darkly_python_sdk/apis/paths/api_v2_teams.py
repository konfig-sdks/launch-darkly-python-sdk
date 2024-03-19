from launch_darkly_python_sdk.paths.api_v2_teams.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_teams.post import ApiForpost
from launch_darkly_python_sdk.paths.api_v2_teams.patch import ApiForpatch


class ApiV2Teams(
    ApiForget,
    ApiForpost,
    ApiForpatch,
):
    pass
