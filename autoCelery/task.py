from autoCelery.celery import app
from crawler.crawler.spiders import uptv_spider, hexdownload_spider
from celery.schedules import crontab


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=14, minute=20),
        uptv.s(),
    )
    sender.add_periodic_task(
        crontab(hour=14, minute=22),
        hex_dl.s(),
    )


@app.task
def uptv():
    uptv_spider.run_upt()


@app.task
def hex_dl():
    hexdownload_spider.run_hex()

