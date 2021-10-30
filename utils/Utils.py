try:
    import os
    import requests
    import subprocess
    import shutil
    import errno
    import stat
except ImportError:
    raise ImportError


class Utils:

    @staticmethod
    def create_path(_dir: str, _file_name: str) -> str:
        return os.path.normpath(os.path.join(_dir, _file_name))

    @staticmethod
    def _file_walker(directory: str) -> list:
        file_list: list = []
        for i in range(1, len(os.listdir(directory))):
            file_list.append("%s%s.m4s" % (directory, i))
        return file_list

    @staticmethod
    def combine(m4s_path: str, output_path: str, init_mp4_path: str) -> bool or Exception:
        try:
            with open(output_path, "wb") as wF:
                with open(init_mp4_path, "rb") as rF:
                    wF.write(rF.read())
                for item in m4s_path:
                    with open(item, "rb") as rF:
                        wF.write(rF.read())
        except (PermissionError, OSError, FileNotFoundError, FileExistsError) as err:
            raise err
        return True

    @staticmethod
    def convert_to_mp4(audio_path: str, video_path: str, output: str) -> bool or Exception:
        p = subprocess.Popen(
            'ffmpeg -i %s -i %s -codec copy %s' % (audio_path, video_path, output), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True
        )
        stdout, stderr = p.communicate()
        if len(stderr):
            raise Exception("ffmpeg is not installed or file path is wrong !")
        return True

    @staticmethod
    def send_request(url: str) -> requests.Request or Exception:
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Error bad status code : %s" % r.status_code)
        return r

    @staticmethod
    def delete_repertory(directoryPath: str) -> None:
        """
        Permet de supprimer un repertoire
        :param directoryPath: Le chemin d'acces vers le repertoire
        :type directoryPath: str
        """
        if os.path.exists(directoryPath):
            # on supprime tous les fichier dans le repertoire
            for root, dirs, files in os.walk(directoryPath):
                # on parcours la liste des fichier du repertoire
                for file in files:
                    filePath = os.path.join(root, file)
                    try:
                        os.chmod(filePath, 0o777)
                        os.remove(filePath)
                    except FileNotFoundError:
                        continue
            # on supprime tous ce qui reste
            shutil.rmtree(directoryPath, ignore_errors=True, onerror=Utils.handleRemoveReadonly)

    @staticmethod
    def handleRemoveReadonly(func, path: str, exc):
        """
        Permet de gerer les erreur pendant la supprimer des dossier (probleme de permission)
        :param func: La fonction à executer
        :param path: Le chemin d'acces vers le dossier à supprimer
        :type path: str
        :param exc: L'exeption
        """
        excvalue = exc[1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
            # on change la permission sur le fichier
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
            # on retente le supprimer
            func(path)
        else:
            raise

    @staticmethod
    def create_directory(directory_path: str) -> bool or Exception:
        if os.path.exists(directory_path):
            return True
        try:
            os.mkdir(directory_path)
        except (PermissionError, OSError, FileNotFoundError, FileExistsError) as err:
            raise err
        return True
