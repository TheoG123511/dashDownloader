try:
    import os
    import logging
    from Config import Config
    from utils.Singleton import Singleton
    from logging.handlers import RotatingFileHandler
except ImportError:
    raise ImportError


class Logging(metaclass=Singleton):
    """
    Classe permetant de gérer l'affichage des log dans la console et de les enregistrer dans un fichier
    text dans le répertoire courant du programme
    """

    def __init__(self, formatlog: str = '%(asctime)s :: %(levelname)s :: %(message)s',
                 level: str = logging.DEBUG) -> None:
        """
        Constructeur de la classe Logging
        :param formatlog: chaine contenant le formatage des log
        :type formatlog: str
        :param level: level minimum des log
        :type level logging
        """
        # Initial construct.
        self._format: str = formatlog
        self._level: str = level
        # configuration du loggeur
        self._logger = logging.getLogger()
        self._logger.setLevel(self._level)
        # configuration du formatage
        self._formatter = logging.Formatter(self._format)
        # on vérifie que le fichier de log existe
        if not os.path.exists(Config.LOG_FILE_PATH):
            try:
                with open(Config.LOG_FILE_PATH, "w"):
                    pass
            except (FileNotFoundError, OSError, PermissionError) as err:
                print("[%s] Unable to create log file :: %s" % (self.__class__.__name__, err))
        self._fileHandler = RotatingFileHandler(Config.LOG_FILE_PATH, 'a')
        self._fileHandler.setLevel(logging.INFO)
        self._fileHandler.setFormatter(self._formatter)
        self._logger.addHandler(self._fileHandler)
        self._streamHandler = logging.StreamHandler()
        self._streamHandler.setLevel(logging.DEBUG)
        self._logger.addHandler(self._streamHandler)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def writeLog(self, className: object, message: str, level: str = "INFO") -> None:
        """
        Ecrit le message dans la console et dans le fichier de log
        :param className: Le nom de la classe
        :type className: str
        :param message: le texte a afficher
        :type message: str
        :param level: l'importance du texte a afficher
        :type level: str
        """
        try:
            className = className.__class__.__name__
            if level == "INFO":
                self._logger.info("[%s] %s" % (className, message))
            elif level == "DEBUG":
                self._logger.debug("[%s] %s" % (className, message))
            elif level == "WARNING":
                self._logger.warning("[%s] %s" % (className, message))
            elif level == "ERROR":
                self._logger.error("[%s] %s" % (className, message))
            elif level == "CRITICAL":
                self._logger.critical("[%s] %s" % (className, message))
            else:
                self._logger.warning("[%s][%s] Error, unknown level : %s" % (self.__class__.__name__, className, level))
        except TypeError:
            raise Exception("[%s][%s] Error -> TypeError" % (self.__class__.__name__, className))
