
# coding: utf-8

# # Celery結構規劃

# In[1]:

from celery import Celery


# In[2]:

import pandas as pd
from pandas import Series, DataFrame


# In[3]:

import os
from pprint import pprint


# ### 預設的參數

# In[4]:

def listDefaultCeleryConfigurations():
    app = Celery()
    configs = app.conf.__dict__['_order'][2]
    configs = sorted([(k, v) for k, v in configs.items()])
    for k, v in configs:
        print ('{0} = {1}'.format(k,  ("'" + v + "'") if isinstance(v, str) else v) )


# In[5]:

listDefaultCeleryConfigurations()


# ---
# ### 抓取 規劃檔案 內容

# In[6]:

def getExcelData(file):
    df = pd.read_excel(file)
    df.dropna(axis=0, how='all', inplace=True)

    return df


# ---
# #### Import Kombu classes

# In[7]:

def import_Kombu_classes(plan, summary):
    output = [] 
    output.extend(['', '#{0:_^78}'.format('Import Kombu classes')])
    output.append('{0}'.format('from kombu import Exchange, Queue'))
    summary.extend(output)
    
    return summary


# ---
# #### CELERY_TIMEZONE & Misc.

# In[8]:

def set_CELERY_TIMEZONE_Misc(plan, summary):
    # 自訂的
    CELERY_TIMEZONE = 'Asia/Taipei' 

    output = [] 
    output.extend(['', '#{0:_^78}'.format('CELERY_TIMEZONE & Misc.')])
    output.append("CELERY_TIMEZONE = '{0}'".format(CELERY_TIMEZONE))
    output.append('CELERYD_POOL_RESTARTS = True')
    summary.extend(output)
    
    return summary


# ---
# #### BROKER_URL
# BROKER_URL = 'redis://netbrain.noip.me:6379/0'

# In[9]:

def set_BROKER_URL(plan, summary):
    BROKER_URL = plan.Broker.drop_duplicates()[0]

    output = [] 
    output.extend(['', '#{0:_^78}'.format('BROKER_URL')])
    output.append("BROKER_URL = '{0}'".format(BROKER_URL))
    summary.extend(output)
    
    return summary


# ---
# #### CELERY_RESULT_BACKEND
# CELERY_RESULT_BACKEND = 'redis://netbrain.noip.me:6379/1'

# In[10]:

def set_CELERY_RESULT_BACKEND(plan, summary):
    CELERY_RESULT_BACKEND = plan.Result_backend.drop_duplicates()[0]

    output = [] 
    output.extend(['', '#{0:_^78}'.format('CELERY_RESULT_BACKEND')])
    output.append("CELERY_RESULT_BACKEND = '{0}'".format(CELERY_RESULT_BACKEND))
    summary.extend(output)
    
    return summary


# ---
# #### CELERY_IMPORTS
# CELERY_IMPORTS = ('proj.tasks', )

# In[11]:

def set_CELERY_IMPORTS(plan, summary):
    Celery_app_tasks = plan[['Celery_app', 'Tasks_module']].drop_duplicates()
    modules = ('{0}.{1}'.format(Celery_app_tasks.ix[i, 'Celery_app'], Celery_app_tasks.ix[i, 'Tasks_module']) for i in range(len(Celery_app_tasks)))
    CELERY_IMPORTS = tuple(modules)

    output = [] 
    output.extend(['', '#{0:_^78}'.format('CELERY_IMPORTS')])
    output.append('CELERY_IMPORTS = {0}'.format(CELERY_IMPORTS))
    summary.extend(output)
    
    return summary


# ---
# #### CELERY_QUEUES

#     CELERY_QUEUES = (
#         Queue('feed_tasks', routing_key='feed.#'),
#         Queue('regular_tasks', routing_key='task.#'),
#         Queue('image_tasks', exchange=Exchange('mediatasks', type='direct'), routing_key='image.compress'),
#     )
# 
#     CELERY_QUEUES = (
#         Queue('default', Exchange('default'), routing_key='default'),
#         Queue('videos',  Exchange('media'),   routing_key='media.video'),
#         Queue('images',  Exchange('media'),   routing_key='media.image'),
#     )

# In[12]:

def set_CELERY_QUEUES(plan, summary):
    queues = plan[['Queue', 'Exchange', 'Exchange_Type', 'Routing_Key']].drop_duplicates()
    output = [] 
    output.extend(['', '#{0:_^78}'.format('CELERY_QUEUES')])

    output.append('CELERY_QUEUES = (')

    for i in range(len(queues)):
        output.append("    Queue('{queue}', Exchange('{exchange}', type = '{exchange_Type}'), routing_key='{routing_key}'),"               .format(queue = queues.ix[i, 'Queue'],
                       exchange = queues.ix[i, 'Exchange'],
                       exchange_Type = queues.ix[i, 'Exchange_Type'], 
                       routing_key = queues.ix[i, 'Routing_Key'] 
                      )
              )
    output.append(')')

    summary.extend(output)
    
    return summary


# ---
# #### CELERY_ROUTES

#     CELERY_ROUTES = {
#             'feeds.tasks.import_feed': {
#                 'queue': 'feed_tasks',
#                 'routing_key': 'feed.import',
#             },
#     }

# In[13]:

def set_CELERY_ROUTES(plan, summary):
    routes = plan[['Celery_app', 'Tasks_module', 'Task', 'Queue', 'Routing_Key']].drop_duplicates()
    output = [] 
    output.extend(['', '#{0:_^78}'.format('CELERY_ROUTES')])

    output.append('CELERY_ROUTES = {')

    for i in range(len(routes)):
        output.append("    '{app}.{module}.{task}': {{\n        'queue': '{queue}',\n        'routing_key': '{routing_key}',\n    }},"               .format(app = routes.ix[i, 'Celery_app'],
                       module = routes.ix[i, 'Tasks_module'],
                       task = routes.ix[i, 'Task'], 
                       queue = routes.ix[i, 'Queue'],                   
                       routing_key = routes.ix[i, 'Routing_Key'])
              )
    output.append('}')

    summary.extend(output)
    
    return summary


# ---
# #### WORKERS

# In[14]:

def set_Workers_Scripts(plan, summary):
    workers = plan[['Node', 'Celery_app', 'Worker', 'Queue', 'Concurrency', 'Log_level']].drop_duplicates()
    output = []
    output.extend(['', '#{0:_^78}'.format('Workers Scripts')])

    for i in range(len(workers)):
        output.append('#[Node - {node}] : celery -A {app} worker -n {worker} -Q {queue} --concurrency={concurrency} --loglevel={loglevel}'               .format(node = workers.ix[i, 'Node'],
                       app = workers.ix[i, 'Celery_app'],
                       worker = workers.ix[i, 'Worker'], 
                       queue = workers.ix[i, 'Queue'], 
                       concurrency = workers.ix[i, 'Concurrency'],                   
                       loglevel = workers.ix[i, 'Log_level']
                      )
              )

    summary.extend(output)
    
    return summary


# ---
# #### FLOWER

# In[15]:

def set_FLOWER(plan, summary):
    app = plan.Celery_app.drop_duplicates()[0]
    output = [] 
    output.extend(['', '#{0:_^78}'.format('FLOWER')])
    
    output.append('#[Flower] : celery -A {app} flower'.format(app = app))
    summary.extend(output)
    
    return summary


# ## Summarize

# In[16]:

def summarizeConfigurations(planExcelFile):
    
    summary = []
    
#     listDefaultCeleryConfigurations()

    plan = getExcelData(planExcelFile)
    
    import_Kombu_classes(plan, summary)
    set_CELERY_TIMEZONE_Misc(plan, summary)
    set_BROKER_URL(plan, summary)
    set_CELERY_RESULT_BACKEND(plan, summary)
    set_CELERY_IMPORTS(plan, summary)
    set_CELERY_QUEUES(plan, summary)
    set_CELERY_ROUTES(plan, summary)
    
    set_Workers_Scripts(plan, summary)
    set_FLOWER(plan, summary)
    
    return summary


# ## Output Configuration File

# In[17]:

def writeConfigurationFile(summary, file = 'celeryconfig.py'):
    with open(file, 'w', encoding = 'utf8') as f:
        for line in summary: f.write(line + '\n')


# In[18]:

def genConfigFile():
    # 指定規劃檔案
    folder = os.getcwd()
    files = [file for file in os.listdir(folder) if file.rpartition('.')[2] in ('xls','xlsx')]    
    
    if len(files) == 1 :        
        file = os.path.join(folder, files[0])
        summary = summarizeConfigurations(file)
        for line in summary: print (line) 
        writeConfigurationFile(summary)
        
    else:
        print('There must be one and only one plan Excel file.')    


# ## Main

# In[19]:

if __name__ == '__main__':
    genConfigFile()


# In[ ]:



