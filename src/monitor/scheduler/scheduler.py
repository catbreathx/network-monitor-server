from apscheduler.schedulers.asyncio import AsyncIOScheduler

from monitor.scheduler import ping_job

scheduler_instance: AsyncIOScheduler


def shutdown_scheduler():
    scheduler_instance.shutdown()


def setup_scheduler():
    global scheduler_instance
    scheduler_instance = AsyncIOScheduler()
    scheduler_instance.add_job(
        ping_job.HostPingJob().run, "interval", seconds=10, id="ping_job", max_instances=1
    )

    scheduler_instance.start(paused=False)
