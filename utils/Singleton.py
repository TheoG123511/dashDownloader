class Singleton(type):
    """
    Permet d'initialiser une seul instance de MainControlleur (singleton)
    """
    _instances: dict = {}

    def __call__(cls, *args: tuple, **kwargs: dict) -> isinstance:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
