import os
import json
import sys
import json

Data = sys.stdin.read()
Rutas = json.loads(Data)

#Informacion requerida

InputRequeridos=["Marca","Vin","Economico","Modelo","Año","Version","Color","Pedido","Disponibilidad","VehiculoSucursal","TipoCombustible"]

#Variables

Bandera=None
RutaOrigen = None

#Rutas
print(Rutas[0])
RutaData = os.path.join(RutaOrigen,Rutas[0])

#Abrimos el Archvio con formato json

with open(RutaData,'r') as DataBruta:
    Data = DataBruta.read()

try:

    DataJson = json.loads(Data)

    #Validamos los campos Requeridos
    for Dato in InputRequeridos:
        if Dato in DataJson:
            print("Se encontro")
            Bandera = True
        else:
            print("Falta el siguiente valor:'{Dato}'")
            Bandera = False
            break
    
    if Bandera == True:
        print("Paso la validacion")

    


     
except KeyError :
    print('El archivo no cuenta con un formato json') 