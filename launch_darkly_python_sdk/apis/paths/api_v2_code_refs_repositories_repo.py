from launch_darkly_python_sdk.paths.api_v2_code_refs_repositories_repo.get import ApiForget
from launch_darkly_python_sdk.paths.api_v2_code_refs_repositories_repo.delete import ApiFordelete
from launch_darkly_python_sdk.paths.api_v2_code_refs_repositories_repo.patch import ApiForpatch


class ApiV2CodeRefsRepositoriesRepo(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
