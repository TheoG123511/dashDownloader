try:
    from DashDownloader import DashDownloader
except ImportError:
    raise ImportError


if __name__ == '__main__':
    url_audio: str = "https://das-q1-ssl.tf1.fr/2/USP-0x0/93/58/13649358/ssm/13649358.ism/dash/13649358-audio="
    base_audio: str = "128000"

    url_video: str = "https://das-q1-ssl.tf1.fr/2/USP-0x0/93/58/13649358/ssm/13649358.ism/dash/13649358-video="
    base_video: str = "2498848"
    try:
        DashDownloader(url_audio, base_audio, url_video, base_video)
    except KeyboardInterrupt:
        DashDownloader.clean()
