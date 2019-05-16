import os
from recargasyservicios import recargaCelular
import json


result = recargaCelular('Demo','RS1234','040100001','5560217769',10).to_blocking().first()
dir(result)
salida = json.dumps(result)
print ("dumps del result")
print (salida)