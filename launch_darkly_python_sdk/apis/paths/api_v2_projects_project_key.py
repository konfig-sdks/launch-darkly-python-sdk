from launch_darkly_python_sdk.paths.api_v2_projects_project_key.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_projects_project_key.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_projects_project_key.patch import ApiForpatch


class ApiV2ProjectsProjectKey(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
