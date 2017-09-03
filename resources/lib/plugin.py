# -*- coding: utf-8 -*-

import sys
import routing
import logging

import xbmcaddon
from xbmc import Player, PlayList, PLAYLIST_VIDEO
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl

from resources.lib import kodilogging
from repository import AltvRepository
from analytics import Analytics

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()

repository = AltvRepository('https://api.altv.com/v3')
analytics = Analytics('UA-59891600-7')


@plugin.route('/')
def list_shows():
    currentPage = 1 if 'currentPage' not in plugin.args else int(plugin.args['currentPage'][0])
    response = repository.get_shows(currentPage)

    for show in response.items:
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

    if response.pagination.hasNext:
        addDirectoryItem(
            handle=plugin.handle,
            url=plugin.url_for(list_shows, currentPage=str(
                response.pagination.nextPage)),
            listitem=ListItem(label='Next...'),
            isFolder=True
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
    video = repository.get_video(videoId)
    streams = repository.get_video_streams(video.streamId)

    item = ListItem(path=streams[0].url)
    item.setProperty(u'IsPlayable', u'true')
    item.setInfo(
        type='Video',
        infoLabels={'Title': video.title, 'Plot': video.description}
    )

    analytics.trackVideoPlayed(video.slug)

    playlist = PlayList(PLAYLIST_VIDEO)
    playlist.clear()
    playlist.add(streams[0].url, item)

    player = Player()
    player.play(playlist)


def run():
    plugin.run()
