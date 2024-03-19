from launch_darkly_python_sdk.paths.api_v2_flags_project_key_feature_flag_key.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_flags_project_key_feature_flag_key.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_flags_project_key_feature_flag_key.patch import ApiForpatch


class ApiV2FlagsProjectKeyFeatureFlagKey(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
