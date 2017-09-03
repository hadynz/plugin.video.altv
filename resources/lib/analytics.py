from resources.lib.googlemeasurementprotocol import Event, report
from resources.lib import kodiutils
import uuid


class Analytics(object):
    def __init__(self, googleTrackingId):
        self.googleTrackingId = googleTrackingId

    def getClientId(self):
        clientId = kodiutils.get_setting('clientId')

        if not clientId:
            clientId = uuid.uuid4()
            kodiutils.set_setting('clientId', clientId)

        return clientId

    def trackVideoPlayed(self, videoId):
        event = Event('kodi', 'video_played', label=videoId)
        report(self.googleTrackingId, self.getClientId(), event)
