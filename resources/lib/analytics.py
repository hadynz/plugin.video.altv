from resources.lib.googlemeasurementprotocol import Event, report


class Analytics(object):
    def __init__(self, clientId, googleTrackingId):
        self.clientId = clientId
        self.googleTrackingId = googleTrackingId

    def trackVideoPlayed(self, videoId):
        event = Event('kodi', 'video_played', label=videoId)
        report(self.googleTrackingId, self.clientId, event)
