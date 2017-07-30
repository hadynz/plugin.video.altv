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

class VideoDto(object):
    def __init__(self, id, title, slug, viewCount, duration, previewImage):
        self.id = id
        self.title = title
        self.slug = slug
        self.viewCount = viewCount
        self.duration = duration
        self.previewImage = previewImage

class AltvRepository(object):

    def __init__(self, baseHttp):
        self._baseHttp = baseHttp

    def get_shows(self):
        response = requests.get("%s/shows" % self._baseHttp)
        # TODO: Check if status is 200
        logging.warn(response.json())

        shows = response.json()['data']['shows']
        return map(lambda show: ShowDto(show['id'], show['title'], show['slug'], show['videos'], show['images']['preview'], show['images']['cover']), shows)

    def get_show_videos(self, showSlug):
        logging.warn("%s/videos?show=%s&per_page=9999" % (self._baseHttp, showSlug))
        response = requests.get("%s/videos?show=%s&per_page=9999" % (self._baseHttp, showSlug))
        logging.warn(response.json())

        videos = response.json()['data']['videos']
        return map(lambda show: VideoDto(show['id'], show['title'], show['slug'], show['views'], show['duration'], show['images']['preview']), videos)


repository = AltvRepository("https://api.altv.com:443/v3")
shows = repository.get_shows()
print shows
