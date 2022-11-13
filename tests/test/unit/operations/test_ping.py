from unittest import mock

from monitor.operations import perform_ping


class TestPerformPing:
    def test_successful_ping_and_then_returns_true_with_ping_output(self):
        ip_to_test = "127.0.0.1"
        actual_ping_result, actual_output = perform_ping(ip_to_test)

        assert actual_ping_result is True
        assert "ping" in actual_output
        assert ip_to_test in actual_output

    def test_unsuccessful_ping_and_then_return_false_with_ping_output(self):
        ip_to_test = "A.0.0.0"
        actual_ping_result, actual_output = perform_ping(ip_to_test, timeout=1)

        expected_output = "Cannot resolve: Unknown host. (Host='A.0.0.0')"

        assert actual_ping_result is False
        assert actual_output == expected_output

    @mock.patch("ping3.verbose_ping", autospec=True)
    def test_when_ping_throws_exception_and_then_return_false_with_exception(
        self, mock_verbose_ping: mock.Mock
    ):
        ip_to_test = "127.0.0.0"
        mock_verbose_ping.side_effect = Exception("test exception")
        actual_ping_result, actual_output = perform_ping(ip_to_test, timeout=1)

        expected_output = (
            "Exception while attempting to ping - 127.0.0.0, " "error - Exception, test exception"
        )

        assert actual_ping_result is False
        assert expected_output == actual_output
