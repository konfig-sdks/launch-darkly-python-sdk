# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from launch_darkly_python_sdk.paths.api_v2_usage_mau_bycategory import Api

from launch_darkly_python_sdk.paths import PathValues

path = PathValues.API_V2_USAGE_MAU_BYCATEGORY