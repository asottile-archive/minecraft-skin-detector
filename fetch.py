
import urllib2

from util.ghetto_retry import ghetto_retry

SKIN_URL = 'http://s3.amazonaws.com/MinecraftSkins/%s.png'

TIMEOUT = 10

class FailedRequestError(ValueError): pass

@ghetto_retry(3, exceptions=(urllib2.URLError, FailedRequestError))
def get_player_skin(player_name):
    """Fetches a players skin.  Returns raw binary data."""
    request = urllib2.urlopen(SKIN_URL % player_name)

    if request.getcode() != 200:
        raise FailedRequestError

    return request.read()
