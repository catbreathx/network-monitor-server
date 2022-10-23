import getopt
import os
import sys

import uvicorn

DEFAULT_PORT = 5001

if __name__ == "__main__":
    env_file = "dev.env"
    port = DEFAULT_PORT

    opts, args = getopt.getopt(sys.argv[1:], "ep", ["envfile=", "port="])

    for opt, arg in opts:
        if opt in ["-e", "--envfile"]:
            env_file = arg
        if opt in ["-p", "--port"]:
            port = int(arg)

    os.environ["ENV_FILE"] = env_file

    from monitor.app import app_instance

    uvicorn.run(app_instance, host="0.0.0.0", port=port)
