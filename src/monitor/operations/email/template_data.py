from typing import Any, Iterator

from monitor.database import model_list_to_json, models


class HealthCheckReport:
    scheduled_job: models.ScheduledJob
    hosts: Iterator[models.Host] | list[models.Host]
    host_health_checks: list[models.HostHealthCheck]

    def __init__(
        self,
        scheduled_job: models.ScheduledJob,
        hosts: Iterator[models.Host] | list[models.Host],
        host_health_checks: list[models.HostHealthCheck],
    ):
        super().__init__()

        self.scheduled_job = scheduled_job
        self.host_health_checks = host_health_checks
        self.hosts = hosts

    def json(self) -> dict[str, Any]:
        host_health_checks_as_json = model_list_to_json(self.host_health_checks)
        scheduled_job_as_json = self.scheduled_job.json()
        hosts_as_json = model_list_to_json(self.hosts)

        hosts_as_dict: dict[int, dict[str, Any]] = {}
        for host in hosts_as_json:
            hosts_as_dict[host["id"]] = host

        result = {
            "host_health_check": host_health_checks_as_json,
            "scheduled_job": scheduled_job_as_json,
            "hosts": hosts_as_dict,
        }

        return result
