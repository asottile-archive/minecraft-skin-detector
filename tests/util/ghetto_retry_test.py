
import mock
import testify as T

from util.ghetto_retry import ghetto_retry

class TestGhettoRetry(T.TestCase):

    def get_mock_callable(self):
        """mock.Mock() does not have a __name__ so we wrap it in a function."""
        mock_callable = mock.Mock()
        def callable(*args, **kwargs):
            return mock_callable(*args, **kwargs)
        return callable, mock_callable

    def test_ghetto_retry_function_is_called_normally(self):
        callable, mock_callable = self.get_mock_callable()
        callable = ghetto_retry(3)(callable)
        args = (object(), object())
        kwargs = {str(object()): object()}
        callable(*args, **kwargs)
        mock_callable.assert_called_once_with(*args, **kwargs)

    def test_ghetto_retry_reraises_exception(self):
        callable, mock_callable = self.get_mock_callable()
        mock_callable.side_effect = AssertionError
        with T.assert_raises(AssertionError):
            ghetto_retry(1)(callable)()

    def test_ghetto_retry_tries_correct_number_of_times(self):
        callable, mock_callable = self.get_mock_callable()
        mock_callable.side_effect = AssertionError
        COUNT = 3
        with T.assert_raises(AssertionError):
            ghetto_retry(COUNT, exceptions=(AssertionError,))(callable)()

        T.assert_equal(mock_callable.call_count, COUNT)

    def test_ghetto_retry_does_not_capture_exception_of_incorrect_type(self):
        callable, mock_callable = self.get_mock_callable()
        mock_callable.side_effect = AssertionError
        with T.assert_raises(AssertionError):
            ghetto_retry(3, exceptions=(ValueError,))(callable)()
        mock_callable.assert_called_once_with()
