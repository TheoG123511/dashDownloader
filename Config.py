try:
    import os
    import output
    import log
except ImportError:
    raise ImportError


class Config:
    _BASE_MODULE: str = "__init__.py"
    _BASE_MODULE_COMPILED: str = "__init__.pyc"
    OUTPUT: str = os.path.normpath(output.__file__.replace(_BASE_MODULE_COMPILED, '').replace(_BASE_MODULE, ''))
    OUTPUT_AUDIO: str = os.path.normpath(
        output.__file__.replace(_BASE_MODULE_COMPILED, 'audio\\').replace(_BASE_MODULE, 'audio\\')
    )
    OUTPUT_VIDEO: str = os.path.normpath(
        output.__file__.replace(_BASE_MODULE_COMPILED, 'video\\').replace(_BASE_MODULE, 'video\\')
    )
    LOG_FILE_PATH: str = os.path.normpath(
        log.__file__.replace(_BASE_MODULE_COMPILED, 'activity.log').replace(_BASE_MODULE, 'activity.log')
    )
    OUTPUT_MERGED: str = os.path.normpath(
        output.__file__.replace(_BASE_MODULE_COMPILED, 'merged\\').replace(_BASE_MODULE, 'merged\\')
    )
