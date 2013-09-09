
from __future__ import absolute_import

import __builtin__

import contextlib
import mock
import os.path
import testify as T

from skin_compare import has_changed
from testing.utilities import FakeFile

class TestHasChanged(T.TestCase):

    @T.setup_teardown
    def setup_mocks(self):
        with contextlib.nested(
            mock.patch.object(os.path, 'exists', autospec=True),
            mock.patch.object(__builtin__, 'open', autospec=True),
        ) as (
            self.exists_mock,
            self.open_mock,
        ):
            yield

    def test_file_does_not_exist_returns_false_and_writes_file(self):
        self.exists_mock.return_value = False
        self.open_mock.return_value = FakeFile()

        ret = has_changed('Notch', 'fakedata')
        T.assert_equal(ret, False)
        self.open_mock().write.assert_called_once_with('fakedata')

    def test_file_exists_compares_and_writes_files_same(self):
        self.exists_mock.return_value = True
        filedata = 'fakedata'
        self.open_mock.return_value = FakeFile(filedata)

        ret = has_changed('Notch', filedata)
        T.assert_equal(ret, False)
        self.open_mock().write.assert_called_once_with(filedata)

    def test_file_exists_comparse_and_writes_files_different(self):
        self.exists_mock.return_value = True
        filedata1 = 'fakedata'
        filedata2 = 'fakedata_different'
        self.open_mock.return_value = FakeFile(filedata1)

        ret = has_changed('Notch', filedata2)
        T.assert_equal(ret, True)
        self.open_mock().write.assert_called_once_with(filedata2)
