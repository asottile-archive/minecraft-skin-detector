
import mock
import testify as T
import urllib2

from fetch import get_player_skin
from fetch import SKIN_URL

class TestGetPlayerSkin(T.TestCase):
    @T.setup_teardown
    def setup_mocks(self):
        with mock.patch.object(
            urllib2, 'urlopen', autospec=True,
        ) as self.urlopen_mock:
            yield

    def test_get_player_skin(self):
        self.urlopen_mock.return_value.getcode.return_value = 200
        PLAYER = 'Notch'
        ret = get_player_skin(PLAYER)

        self.urlopen_mock.assert_called_once_with(SKIN_URL % PLAYER)
        T.assert_equal(ret, self.urlopen_mock(None).read())

@T.suite('integration')
@T.suite('external_deps')
class TestGetPlayerSkinIntegration(T.TestCase):
    def test_get_player_skin_integration(self):
        ret = get_player_skin('Notch')
        assert ret
