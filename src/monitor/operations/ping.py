import io
import logging
from contextlib import redirect_stdout

import ping3

logger = logging.getLogger(__name__)


def perform_ping(ip_address: str, timeout: int = 5) -> (bool, str):
    logger.debug(f"Pinging IP - {ip_address}")

    ping3.EXCEPTIONS = True
    try:
        with redirect_stdout(io.StringIO()) as output:
            ping3.verbose_ping(ip_address, timeout=timeout)

        result = (True, output.getvalue())
    except ping3.errors.PingError as e:
        result = (False, e.message)
    except Exception as e:
        result = (
            False,
            f"Exception while attempting to ping - {ip_address}, "
            f"error - {e.__class__.__name__}, {e}",
        )

    logger.debug(f"Ping result - IP {ip_address}, result = {result[0]}, output = {result[1]}")

    return result
