from celery import Celery

celery_app = None


def create_celery_app():
    """Starts a celery application"""
    global celery_app

    if not celery_app:
        celery_app = Celery('tasks', broker='amqp://guest@localhost//')
    return celery_app
