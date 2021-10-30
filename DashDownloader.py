try:
    import time
    from Config import Config
    from log.log import Logging
    from utils.Utils import Utils
except ImportError:
    raise ImportError


class DashDownloader:

    _WRITE_MODE: str = "wb"

    def __init__(
            self, url_audio: str, base_audio: str, init_audio_url: str, base_video: str, url_video: str,
            init_video_url: str, download=True
    ) -> None:
        self._log: Logging = Logging()
        self._base_audio: str = base_audio
        self._url_audio: str = url_audio
        self._init_audio_url: str = init_audio_url
        self._base_video: str = base_video
        self._url_video: str = url_video
        self._init_video_url: str = init_video_url
        self._config: str = Config.OUTPUT
        self._init_audio_path: str = ""
        self._init_video_path: str = ""
        self._count = 1
        if download:
            self.download()

    def _writeLog(self, message: str) -> None: self._log.writeLog(self, message)

    def download(self) -> None:
        timer1: time.time = time.time()
        Utils.create_directory(Config.OUTPUT_AUDIO), Utils.create_directory(Config.OUTPUT_VIDEO)
        Utils.create_directory(Config.OUTPUT_MERGED)
        self._init_audio_path, self._init_video_path = "", ""
        self._get_m4s(self._url_audio, self._base_audio, 1)
        self._get_m4s(self._url_video, self._base_video)
        output_audio: str = Utils.create_path(Config.OUTPUT_MERGED, "audio.mp4")
        output_video: str = Utils.create_path(Config.OUTPUT_MERGED, "video.mp4")
        Utils.combine(Config.OUTPUT_AUDIO, output_audio, self._init_audio_path)
        Utils.combine(Config.OUTPUT_VIDEO, output_video, self._init_video_path)
        Utils.convert_to_mp4(output_audio, output_video, Utils.create_path(Config.OUTPUT, "myVideo.mp4"))
        time_to_run: float = time.time() - timer1
        self._writeLog("Download done on %s second%s" % (time_to_run, "s" if time_to_run > 1 else ""))

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
            request_url: str = "%s%s%s" % (url, base, self._count)
            self._writeLog("Request at : %s" % request_url)
            r = Utils.send_request(request_url)
            self._writeLog("Response - status code : %s - %s" % (r.status_code, request_url))
            with open(Utils.create_path(output_dir, '%s.m4s' % self._count), self._WRITE_MODE) as wF:
                wF.write(r.content)
            self._count += 1

