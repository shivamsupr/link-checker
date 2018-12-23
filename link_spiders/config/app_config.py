import os


class ApplicationConfig(object):
    __configuration = {}

    __config_initialized = False
    __logging_initialized = False

    @staticmethod
    def get_project_root():
        current_path, filename = os.path.split(os.path.abspath(__file__))
        components = current_path.split(os.sep)
        _project_root = str.join(os.sep, components[:components.index('link-checker') + 1])
        return _project_root

    @staticmethod
    def get_app_root():
        current_path, filename = os.path.split(os.path.abspath(__file__))
        components = current_path.split(os.sep)
        _app_root = str.join(os.sep, components[:components.index('src') + 1])
        return _app_root

    @staticmethod
    def init_config():
        print('init_config')
        if ApplicationConfig.__config_initialized:
            return
        ApplicationConfig.__config_initialized = True

        return

    @staticmethod
    def get(key):
        parts = key.split('.')
        first, sub_parts = parts[0], parts[1:]

        _config = ApplicationConfig.__configuration[first]
        for index in range(len(sub_parts)):
            if not _config or not isinstance(_config, dict) or sub_parts[index] not in _config:
                raise KeyError("Key '{0}' not found or invalid".format(key))
            _config = _config[sub_parts[index]]

        return _config

    @staticmethod
    def get_config_root():
        return os.path.join(ApplicationConfig.get_project_root(), 'link_spiders', 'config')

    @staticmethod
    def get_shared_root():
        return os.path.join(ApplicationConfig.get_project_root(), 'shared')
