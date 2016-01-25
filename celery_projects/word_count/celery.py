from celery import Celery
from kombu import Exchange, Queue


app = Celery()
app.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()