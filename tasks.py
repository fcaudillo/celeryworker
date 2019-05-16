from celery import Celery
import os
from recargasyservicios import recargaCelular
import json

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

#app = Celery('tasks',backend='rpc://', broker='amqp://guest@localhost:5672//')

app = Celery('tasks')
app.config_from_object('celeryconfig')

#@app.task
def sum(x,y):
  return x + y
  

@app.task
def recarga(compania,plan,numero,monto):
  result = recargaCelular('Demo','RS1234',plan,numero,monto).to_blocking().first()
  print ("1..respuesta final desde tarea")
  print (result)
  jsonString = json.dumps(result)
  return jsonString
  
