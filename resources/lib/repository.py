import requests
import logging


class Pagination(object):
    def __init__(self, currentPage, lastPage):
        self.currentPage = currentPage
        self.hasNext = currentPage < lastPage
        self.nextPage = self.currentPage + 1 if self.hasNext else self.currentPage


class PaginatedResponse(object):
    def __init__(self, items, pagination):
        self.items = items
        self.pagination = pagination


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

    def get_shows(self, currentPage):
        response = requests.get("%s/shows?page=%d" %
                                (self._baseHttp, currentPage)).json()

        shows = response['data']['shows']
        pagination = response['data']['pagination']

        items = map(lambda show: ShowDto(
            id=show['id'],
            title=show['title'],
            slug=show['slug'],
            videoCount=show['videos'],
            previewImage=show['images']['preview'],
            coverImage=show['images']['cover']
        ), shows)

        return PaginatedResponse(items, Pagination(pagination['currentPage'], pagination['lastPage']))

    def get_show_videos(self, showSlug):
        response = requests.get(
            "%s/videos?show=%s&per_page=9999" % (self._baseHttp, showSlug))

        videos = response.json()['data']['videos']

        return map(lambda video: VideoSummaryDto(video['id'], video['title'], video['slug'], video['views'], video['duration'], video['images']['preview']), videos)

    def get_video(self, videoId):
        response = requests.get("%s/videos/%s" % (self._baseHttp, videoId))

        video = response.json()['data']

        return VideoDto(video['id'], video['ooyala_id'], video['title'], video['description'])

    def get_video_streams(self, videoStreamId):
        response = requests.get("%s/videos/streams/%s" %
                                (self._baseHttp, videoStreamId))

        streams = response.json()['data']['streams']

        return map(lambda stream: VideoStream(stream['url'], stream['average_video_bitrate'], stream['audio_bitrate'], stream['muxing_format']), streams)
