from launch_darkly_python_sdk.paths.api_v2_roles_custom_role_key.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_roles_custom_role_key.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_roles_custom_role_key.patch import ApiForpatch


class ApiV2RolesCustomRoleKey(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
