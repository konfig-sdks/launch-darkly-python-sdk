from launch_darkly_python_sdk.paths.api_v2_teams_team_key.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_teams_team_key.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_teams_team_key.patch import ApiForpatch


class ApiV2TeamsTeamKey(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
