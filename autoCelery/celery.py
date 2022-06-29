from celery import Celery

app = Celery('autoCelery',
             broker='redis://localhost:6379/0'
             )

app.conf.timezone = "Asia/Tehran"
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
