from autoCelery.celery import app
from crawler.crawler.spiders import uptv_spider, hexdownload_spider
from celery.schedules import crontab


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=13, minute=26),
        uptv.s(),
    )
    sender.add_periodic_task(
        crontab(hour=13, minute=27),
        hex_dl.s(),
    )


@app.task
def uptv():
    uptv_spider.run_upt()


@app.task
def hex_dl():
    hexdownload_spider.run_hex()

