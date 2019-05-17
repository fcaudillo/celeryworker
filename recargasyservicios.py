from rx import Observable, Observer
from zeep import Client
from datetime import datetime, date, time, timedelta
import xml.etree.ElementTree as ET

wsdl = 'https://www.recargasyservicios.com/demo/transact.asmx?wsdl'
client = Client(wsdl=wsdl)

def saldo(usuario, password):
  def defer():
    try:
       ini = datetime.today()
       resp = client.service.GetBalance(usuario,password)
       print ("obtener balance " + usuario + " - " + password)
       print (resp)
       fin = datetime.today()
       delta = fin - ini
       print (ini.strftime('Inicio: %H:%M:%S Tiempo de ejecucion : ') + str(delta.seconds) +   ' segundos -  GetBalance')
       tree = ET.ElementTree(ET.fromstring(resp))
       monto = tree.find("balance").text
       print (monto)
       return Observable.just( (monto))
    except:
       return Observable.just( (None))
  return Observable.defer(defer)

def requestId(usuario, password):
  def defer():
    try:
       ini = datetime.today()
       id = client.service.GetTRequestID(usuario,password,'')
       fin = datetime.today()
       delta = fin - ini
       print (ini.strftime('Inicio: %H:%M:%S Tiempo de ejecucion : ') + str(delta.seconds) +   ' segundos -  GetTRequestID')
       print (id)
       return Observable.just( (id))
    except:
       return Observable.just( (None))
  return Observable.defer(defer)
  
def solicitaTAE (id, usuario, password, sku_code, celular, monto):
  def defer():
    try: 
       ini = datetime.today()
       resp = client.service.DoT(id,usuario, sku_code, celular, monto)  
       fin = datetime.today()
       delta = fin - ini
       print (ini.strftime('Inicio: %H:%M:%S Tiempo de ejecucion: ') + str(delta.seconds) +   ' segundos -  DoT')
       return Observable.just( (id, resp) )
    except:
       return Observable.just({"rcode": 12, "rcode_description": "Servicio  DoT no disponible"})	
  return Observable.defer(defer)
  
def checkTransaction (id, usuario):
  def defer():
    try:
       ini = datetime.today()
       resp =  client.service.CheckTransaction(id,usuario)
       fin = datetime.today()
       delta = fin - ini
       print (ini.strftime('Inicio: %H:%M:%S Tiempo de ejecucion: ') + str(delta.seconds) +   ' segundos -  CheckTransaction')
       #respDic = {'transaction_id': resp['transaction_id'], 'rcode': resp['rcode´],'rcode_description': resp['rcode_description'],'op_account': resp['op_account'],'op_authorization': resp['op_authorization'],'printData': resp['printData'],'xmlDevData': resp['xmlDevData'] }
       respDic = {'transaction_id': resp['transaction_id'], 'rcode': resp['rcode'],'rcode_description': resp['rcode_description'],'op_account': resp['op_account'],'op_authorization': resp['op_authorization'],'xmlDevData': resp['xmlDevData'] }		
       print("valor respDic")
       print(respDic)
       return Observable.just( respDic )
    except:
       return Observable.just({"rcode": 12, "rcode_description": "Servicio  CheckTransaction no disponible"})		
    
  return Observable.defer(defer)
  
  
def recargaTAE(id, usuario, password, sku_code, celular, monto):
  #devuelve una trupla
  #print ("Recarga  1", id, usuario, password, sku_code, celular, monto)
  
  
  #srcCheckTransaction  = Observable.of((14)).flat_map(lambda x : Observable.just( (x)))
  # .on_error_resume_next(lambda x : {'error': x } )
  srcCheckTransaction  = Observable.timer(2500).flat_map(lambda tiempo : verifyRecargaTAE(id, usuario, password, sku_code, celular, monto)).retry(10).timeout(62000)
   
  source = Observable.combine_latest(solicitaTAE(id,usuario, password, sku_code, celular, monto), srcCheckTransaction,lambda o1,o2 :  o2   )
  
  return source
 
def verifyRecargaTAE (id, usuario, password, sku_code, celular, monto): 
  source = checkTransaction(id,usuario).flat_map(lambda r : verifyCheckTransaction(id, usuario, password, sku_code, celular, monto, r))
  return source

def verifyCheckTransaction (id, usuario, password, sku_code, celular, monto, r):
  print ('verifyCheckTransaction')
  print (r)
  print ('/verifyCheckTransaction')
  if r['rcode'] != 0:
     #print ('va a ocurrir un error')
     raise Exception(r)
	 
#  if r[1].rcode == 0:
     #print ('va a ocurrir un error')
#     raise Exception({ 'code' : 11 , 'description' : 'Saldo insuficiente' })	 

  return Observable.just(r)

def verifyRequestId (id, usuario, password, sku_code, celular, monto):
  if id == None:
    error = { 'code' : 1 , 'description' : 'La solicitud de la transaccion Fallo' }
    return Observable.just ( (id, error) )
	
#  if id != None:
#    raise Exception({'code' : 10 , 'description' : 'La solicitud de fallo intencional' })
	
  return recargaTAE (id, usuario, password, sku_code, celular, monto)
  
def recargaCelular (usuario, password, sku_code, celular, monto):
  print ("****2. Modificando para ver comportamiento de tlapape si requiere reinicio cuando se modifica celeryworker")
  #obs = Observable.from_(requestId(usuario,password) ).flat_map (lambda id :  Observable.from_future(recargaTAE (id, usuario, password, sku_code, celular, monto)))
  obs = requestId(usuario,password).flat_map (lambda id : verifyRequestId(id, usuario, password, sku_code, celular, monto) ).on_error_resume_next(lambda err : Observable.just (err.args[0] )  )
  return obs 

  