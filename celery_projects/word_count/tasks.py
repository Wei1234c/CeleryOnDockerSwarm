from celery import group
from word_count.celery import app 


@app.task
def mapper(word):
    return (word, 1) if len(word) >= 5 else None    # 過濾掉太短的word