import os
import shlex
import socket
import subprocess
import time
from typing import Optional, Dict

import alembic
from _pytest.config import ExitCode
from alembic.config import Config
from dotenv import dotenv_values

PORT = 5002

server_process: subprocess.Popen
settings: Dict[str, Optional[str]]


def pytest_configure(config):
    load_settings("e2e.env")
    apply_migrations()
    global server_process
    check_port_is_unused(port=PORT)
    server_process = start_server()

    wait_for_server(server_process)


def pytest_sessionfinish(session, exitstatus):
    global server_process
    server_process.kill()

    if exitstatus == ExitCode.OK:
        teardown_migration()


def load_settings(env_file: str):
    global settings
    settings = dotenv_values(env_file)


def wait_for_server(server_process: subprocess.Popen) -> None:
    try:
        wait_for_port(port=PORT)

        if server_process.poll() is not None:
            raise Exception("Server didn't start successfully")
    except TimeoutError as e:
        print(server_process.stdout.readline())
        server_process.kill()
        raise e


def wait_for_port(port: int, host: str = "localhost", timeout: float = 5.0) -> None:
    """Wait until a port starts accepting TCP connections.
    Args:
        port: Port number.
        host: Host address on which the port should exist.
        timeout: In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(
                    "Waited too long for the port {} on host {} to start accepting "
                    "connections.".format(port, host)
                ) from ex


def start_server(port: int = PORT) -> subprocess.Popen:
    cmd = f"python start.py --envfile=e2e.env --port={port}"

    cmds = shlex.split(cmd)

    process = subprocess.Popen(
        cmds, shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return process


def check_port_is_unused(port: int = PORT) -> None:
    try:
        wait_for_port(port=port, timeout=0.1)
        raise Exception(f"Port {port} is already in use.")
    except TimeoutError:
        pass


def apply_migrations():
    os.environ["TEST"] = "True"
    config = Config("alembic.ini")
    global settings
    config.set_main_option("sqlalchemy.url", settings["DATABASE_URL"])
    alembic.command.upgrade(config, "head")


def teardown_migration():
    config = Config("alembic.ini")
    alembic.command.downgrade(config, "base")
