from typing import List

from monitor import schema
from monitor.database import models


class TestHealthCheckScheduledJob:
    def test_scheduled_job_flow(self, test_user: schema.User, test_hosts: List[models.Host]):
        pass
        # todo: to be completed
        # access_token = commands.authenticate(test_user.email)
        # response = commands.run_health_check(access_token)
        #
        # assert response
