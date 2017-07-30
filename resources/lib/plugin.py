# -*- coding: utf-8 -*-

import routing
import logging

import xbmcaddon
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl

from resources.lib import kodiutils
from resources.lib import kodilogging
from repository import AltvRepository

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()
repository = AltvRepository("https://api.altv.com:443/v3")

@plugin.route('/')
def list_shows():
    shows = repository.get_shows()

    for show in shows:
        addDirectoryItem(
            handle=plugin.handle,
            url=plugin.url_for(list_show_videos, show.slug),
            listitem=ListItem(
                label=show.title,
                thumbnailImage=show.previewImage
            ),
            isFolder=True,
            totalItems=show.videoCount
        )

    endOfDirectory(plugin.handle)

@plugin.route('/shows/<slug>')
def list_show_videos(slug):
    videos = repository.get_show_videos(slug)

    for video in videos:
        addDirectoryItem(
            handle=plugin.handle,
            url=plugin.url_for(play_video, video.id),
            listitem=ListItem(
                label=video.title,
                thumbnailImage=video.previewImage
            ),
            isFolder=False
        )

    endOfDirectory(plugin.handle)

@plugin.route('/video/<videoId>')
def play_video(videoId):
    logging.warn("playing video %s" % videoId)
    video = repository.get_video(videoId)
    streams = repository.get_video_streams(video.streamId)

    logging.warn("Stream xox")
    logging.warn(streams[0])

    setResolvedUrl()

    endOfDirectory(plugin.handle)

def run():
    plugin.run()
