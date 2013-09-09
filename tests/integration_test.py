
from __future__ import absolute_import

import __builtin__

import contextlib
import mock
import os.path
import shutil
import tempfile
import testify as T

import config
from fetch import get_player_skin
from minecraft_skin_detector import main
from testing.utilities import get_datafile

@T.suite('integration')
@T.suite('external_deps')
class TestIntegration(T.TestCase):

    username = 'Notch'

    @T.setup_teardown
    def move_data_dir_to_tempdir(self):
        self.data_tmp_dir = tempfile.mkdtemp()
        try:
            with contextlib.nested(
                mock.patch.object(__builtin__, 'print', autospec=True),
                mock.patch.object(config, 'DATA_DIR', self.data_tmp_dir),
            ) as (
                self.print_mock, _,
            ):
                yield
        finally:
            shutil.rmtree(self.data_tmp_dir)

    def _get_skin_file_path(self):
        return os.path.join(self.data_tmp_dir, '%s.png' % self.username)

    def test_creates_data_dir_if_not_there(self):
        shutil.rmtree(self.data_tmp_dir)
        main([self.username])
        T.assert_equal(os.path.exists(self.data_tmp_dir), True)

    def test_empty_data_dir(self):
        T.assert_equal(os.path.exists(self._get_skin_file_path()), False)
        main([self.username])
        T.assert_equal(self.print_mock.call_count, 0)
        T.assert_equal(os.path.exists(self._get_skin_file_path()), True)

    def test_data_dir_contains_same_skin(self):
        # Put notch's skin in the directory
        notch_skin = get_player_skin(self.username)
        with open(self._get_skin_file_path(), 'w') as skin_file:
            skin_file.write(notch_skin)

        # Note this will flake if notch changed his skin between above call and
        # now
        main([self.username])
        T.assert_equal(self.print_mock.call_count, 0)

    def test_data_dir_contains_different_skin(self):
        dinnerbone_skin = get_datafile('Dinnerbone.png')
        with open(self._get_skin_file_path(), 'w') as skin_file:
            skin_file.write(dinnerbone_skin)

        # Note: this test will fail if notch ever changes his skin to
        # dinnerbone's skin
        main([self.username])
        self.print_mock.assert_called_once_with(
            '{0} has a new skin!'.format(self.username)
        )
