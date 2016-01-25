
#_____________________________Import Kombu classes_____________________________
from kombu import Exchange, Queue

#___________________________CELERY_TIMEZONE & Misc.____________________________
CELERY_TIMEZONE = 'Asia/Taipei'
CELERYD_POOL_RESTARTS = True

#__________________________________BROKER_URL__________________________________
BROKER_URL = 'redis://192.168.0.114:6379/0'

#____________________________CELERY_RESULT_BACKEND_____________________________
CELERY_RESULT_BACKEND = 'redis://192.168.0.114:6379/1'

#________________________________CELERY_IMPORTS________________________________
CELERY_IMPORTS = ('word_count.tasks',)

#________________________________CELERY_QUEUES_________________________________
CELERY_QUEUES = (
    Queue('word_counting', Exchange('celery', type = 'direct'), routing_key='word_counting'),
)

#________________________________CELERY_ROUTES_________________________________
CELERY_ROUTES = {
    'word_count.tasks.mapper': {
        'queue': 'word_counting',
        'routing_key': 'word_counting',
    },
}
