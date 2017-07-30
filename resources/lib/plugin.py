# -*- coding: utf-8 -*-

import sys
import routing
import logging

import xbmcaddon
from xbmc import Player, PlayList, PLAYLIST_VIDEO
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl

from resources.lib import kodiutils
from resources.lib import kodilogging
from repository import AltvRepository

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()
repository = AltvRepository('https://api.altv.com:443/v3')


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
    video = repository.get_video(videoId)
    streams = repository.get_video_streams(video.streamId)

    logging.warn('*****url***: ' + streams[0].url)

    item = ListItem(path=streams[0].url)
    item.setProperty(u'IsPlayable', u'true')
    item.setInfo(
        type='Video',
        infoLabels={'Title': video.title, 'Plot': video.description}
    )

    playlist = PlayList(PLAYLIST_VIDEO)
    playlist.clear()
    playlist.add(streams[0].url, item)

    player = Player()
    player.play(playlist)

def run():
    plugin.run()
