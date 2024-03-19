from launch_darkly_python_sdk.paths.api_v2_applications_application_key.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_applications_application_key.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_applications_application_key.patch import ApiForpatch


class ApiV2ApplicationsApplicationKey(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
