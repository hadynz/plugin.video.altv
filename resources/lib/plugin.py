# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory
from repository import AltvRepository

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()

repository = AltvRepository("https://api.altv.com:443/v3")


@plugin.route('/')
def index():
    shows = repository.get_shows()

    for show in shows:
        addDirectoryItem(plugin.handle, plugin.url_for(show_show, show.slug), ListItem(show.title), True)

    endOfDirectory(plugin.handle)

@plugin.route('/shows/<slug>')
def show_show(slug):
    videos = repository.get_show_videos(slug)
    
    for video in videos:
        addDirectoryItem(plugin.handle, "", ListItem(video.title))

    endOfDirectory(plugin.handle)

def run():
    plugin.run()
