
from __future__ import absolute_import

import mock
import os.path
import shutil
import tempfile
import testify as T

import config
from fetch import get_player_skin
from skin_compare import has_changed
from testing.utilities import get_datafile

@T.suite('integration')
@T.suite('external_deps')
class TestIntegration(T.TestCase):

    username = 'Notch'

    @T.setup_teardown
    def move_data_dir_to_tempdir(self):
        self.data_tmp_dir = tempfile.mkdtemp()
        try:
            with mock.patch.object(config, 'DATA_DIR', self.data_tmp_dir):
                yield
        finally:
            shutil.rmtree(self.data_tmp_dir)

    def _get_skin_file_path(self):
        return os.path.join(self.data_tmp_dir, '%s.png' % self.username)


    def test_empty_data_dir(self):
        notch_skin = get_player_skin(self.username)
        T.assert_equal(os.path.exists(self._get_skin_file_path()), False)

        ret = has_changed(self.username, notch_skin)
        T.assert_equal(ret, False)
        T.assert_equal(os.path.exists(self._get_skin_file_path()), True)

    def test_data_dir_contains_same_skin(self):
        notch_skin = get_player_skin(self.username)
        with open(self._get_skin_file_path(), 'w') as skin_file:
            skin_file.write(notch_skin)

        ret = has_changed(self.username, notch_skin)
        T.assert_equal(ret, False)

    def test_data_dir_contains_different_skin(self):
        notch_skin = get_player_skin(self.username)
        # Note: this test will fail if notch ever changes his skin to
        # dinnerbone's skin
        dinnerbone_skin = get_datafile('Dinnerbone.png')
        with open(self._get_skin_file_path(), 'w') as skin_file:
            skin_file.write(dinnerbone_skin)

        ret = has_changed(self.username, notch_skin)
        T.assert_equal(ret, True)
        with open(self._get_skin_file_path(), 'r') as skin_file:
            T.assert_equal(skin_file.read(), notch_skin)
