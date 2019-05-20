import os
from recargasyservicios import recargaCelular,saldo
import json


result = recargaCelular('Demo','RS1234','040100001','5514214121',10).to_blocking().first()

#result = saldo('Demo','RS1234').to_blocking().first()

dir(result)
salida = json.dumps(result)
print ("dumps del result")
print (salida)