try:
    import time
    from Config import Config
    from log.log import Logging
    from utils.Utils import Utils
    from utils.Exception import StatusCodeError
except ImportError:
    raise ImportError


class DashDownloader:

    _WRITE_MODE: str = "wb"
    _OUTPUT_NAME: str = "myVideo.mp4"

    def __init__(
            self, url_audio: str, base_audio: str, url_video: str, base_video: str, download=True
    ) -> None:
        self._log: Logging = Logging()
        self._base_audio: str = base_audio
        if not url_audio.endswith("="):
            raise Exception("url audio is not invalid")
        self._url_audio: str = url_audio
        self._init_audio_url: str = "%s%s.dash" % (self._url_audio, self._base_audio)
        self._base_video: str = base_video
        if not url_video.endswith("="):
            raise Exception("url video is not invalid")
        self._url_video: str = url_video
        self._init_video_url: str = "%s%s.dash" % (self._url_video, self._base_video)
        self._config: str = Config.OUTPUT
        self._init_audio_path: str = ""
        self._init_video_path: str = ""
        self._count = 1
        if download:
            self.download()

    def _writeLog(self, message: str) -> None: self._log.writeLog(self, message)

    def download(self) -> None:
        self.clean(), self.create()
        timer1: time.time = time.time()
        self._init_audio_path, self._init_video_path = "", ""
        self._get_m4s(self._url_audio, self._base_audio, 1)
        self._get_m4s(self._url_video, self._base_video)
        output_audio: str = Utils.create_path(Config.OUTPUT_MERGED, "audio.mp4")
        output_video: str = Utils.create_path(Config.OUTPUT_MERGED, "video.mp4")
        Utils.combine(Config.OUTPUT_AUDIO, output_audio, self._init_audio_path)
        Utils.combine(Config.OUTPUT_VIDEO, output_video, self._init_video_path)
        Utils.convert_to_mp4(output_audio, output_video, Utils.create_path(Config.OUTPUT, self._OUTPUT_NAME))
        time_to_run: float = time.time() - timer1
        self._writeLog("Download done on %s second%s" % (time_to_run, "(s)" if time_to_run > 1 else ""))

    def _get_m4s(self, url: str, base: str, _type=0) -> None:
        if _type > 2:
            raise Exception("Invalid type : %s - Use : 0 -> video, 1 -> audio ")
        output_dir: str = Config.OUTPUT_AUDIO
        if _type == 0:
            output_dir = Config.OUTPUT_VIDEO
            r = Utils.send_request(self._init_video_url)
            self._init_video_path = Utils.create_path(Config.OUTPUT_MERGED, "video.dash")
        else:
            r = Utils.send_request(self._init_audio_url)
            self._init_audio_path = Utils.create_path(Config.OUTPUT_MERGED, "audio.dash")
        with open(self._init_audio_path if _type != 0 else self._init_video_path, self._WRITE_MODE) as wF:
            wF.write(r.content)
        self._count: int = 1
        while True:
            request_url: str = "%s%s-%s.m4s" % (url, base, self._count)
            self._writeLog("Request at : %s" % request_url)
            try:
                r = Utils.send_request(request_url)
            except StatusCodeError:
                break
            self._writeLog("Response - status code : %s - %s" % (r.status_code, request_url))
            with open(Utils.create_path(output_dir, '%s.m4s' % self._count), self._WRITE_MODE) as wF:
                wF.write(r.content)
            self._count += 1

    @staticmethod
    def clean() -> None or Exception:
        if Utils.exist(Config.OUTPUT_AUDIO):
            Utils.delete(Config.OUTPUT_AUDIO)
        if Utils.exist(Config.OUTPUT_AUDIO):
            Utils.delete(Config.OUTPUT_VIDEO)
        if Utils.exist(Config.OUTPUT_MERGED):
            Utils.delete(Config.OUTPUT_MERGED)
        if Utils.exist(Utils.create_path(Config.OUTPUT, DashDownloader._OUTPUT_NAME)):
            Utils.delete(Utils.create_path(Config.OUTPUT, DashDownloader._OUTPUT_NAME))

    @staticmethod
    def create() -> None or Exception:
        if not Utils.exist(Config.OUTPUT):
            Utils.create_directory(Config.OUTPUT)
        Utils.create_directory(Config.OUTPUT_AUDIO), Utils.create_directory(Config.OUTPUT_VIDEO)
        Utils.create_directory(Config.OUTPUT_MERGED)
