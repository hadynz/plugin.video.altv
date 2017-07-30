import requests
import logging

class ShowDto(object):
    def __init__(self, id, title, slug, videoCount, previewImage, coverImage):
        self.id = id
        self.title = title
        self.slug = slug
        self.videoCount = videoCount
        self.previewImage = previewImage
        self.coverImage = coverImage

class VideoSummaryDto(object):
    def __init__(self, id, title, slug, viewCount, duration, previewImage):
        self.id = id
        self.title = title
        self.slug = slug
        self.viewCount = viewCount
        self.duration = duration
        self.previewImage = previewImage

class VideoDto(object):
    def __init__(self, id, ooyala_id, title, description):
        self.id = id
        self.streamId = ooyala_id
        self.title = title
        self.description = description

class VideoStream(object):
    def __init__(self, url, videoBitrate, audioBitrate, muxingFormat):
        self.url = url
        self.videoBitrate = videoBitrate
        self.audioBitrate = audioBitrate
        self.muxingFormat = muxingFormat

class AltvRepository(object):

    def __init__(self, baseHttp):
        self._baseHttp = baseHttp

    def get_shows(self):
        response = requests.get("%s/shows" % self._baseHttp)

        shows = response.json()['data']['shows']

        return map(lambda show: ShowDto(show['id'], show['title'], show['slug'], show['videos'], show['images']['preview'], show['images']['cover']), shows)

    def get_show_videos(self, showSlug):
        response = requests.get("%s/videos?show=%s&per_page=9999" % (self._baseHttp, showSlug))

        videos = response.json()['data']['videos']

        return map(lambda video: VideoSummaryDto(video['id'], video['title'], video['slug'], video['views'], video['duration'], video['images']['preview']), videos)

    def get_video(self, videoId):
        response = requests.get("%s/videos/%s" % (self._baseHttp, videoId))

        video = response.json()['data']

        return VideoDto(video['id'], video['ooyala_id'], video['title'], video['description'])

    def get_video_streams(self, videoStreamId):
        response = requests.get("%s/videos/streams/%s" % (self._baseHttp, videoStreamId))

        streams = response.json()['data']['streams']

        return map(lambda stream: VideoStream(stream['url'], stream['average_video_bitrate'], stream['audio_bitrate'], stream['muxing_format']), streams)

repository = AltvRepository("https://api.altv.com:443/v3")
shows = repository.get_shows()
print shows
