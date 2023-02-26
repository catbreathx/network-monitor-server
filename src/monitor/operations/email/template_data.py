from monitor.database import model_list_to_json, models


class HealthCheckReport:
    scheduled_job: models.ScheduledJob
    host_health_checks: list[models.HostHealthCheck]

    def __init__(
        self, scheduled_job: models.ScheduledJob, host_health_checks: list[models.HostHealthCheck]
    ):
        super().__init__()

        self.scheduled_job = scheduled_job
        self.host_health_checks = host_health_checks

    def json(self):
        host_health_checks_as_json = model_list_to_json(self.host_health_checks)
        scheduled_job_as_json = self.scheduled_job.json()

        result = {
            "host_health_check": host_health_checks_as_json,
            "scheduled_job": scheduled_job_as_json,
        }

        return result
