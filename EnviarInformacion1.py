import os
import json
import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def MostrarPopup(Mensaje):
    Ventana = tk.Tk()
    Ventana.withdraw() 
    messagebox.showinfo("Información", Mensaje)
    Ventana.destroy()

def ValidarInformacion(datos):
    bandera = 0
    # Información requerida
    InputRequeridos = ["MarcaInput", "VinInput", "Economico", "ModeloInput", "YearInput", "VersionInput", "ColorInput", "NoPedidoInput", "DisponibilidadInput", "SucursalInput", "CombustiblesInput","PrecioInput","TipoVehiculo"]

    Fecha = datetime.now().strftime("%D-%M-%Y %H:%M:%S")
    
    url = 'https://mylsa.com.mx/Pilot/php/AgregarStock.php'
    
    Reporte = []
    Reporte.append("=== Reporte de Validación de Campos ===\n")
    Reporte.append(f"Fecha de generación del reporte: {Fecha}\n")
    Reporte.append(f"Archivo procesado desde la URL: {url}\n\n")

    # Procesamos cada registro en el JSON
    for i, Registro in enumerate(datos):

        # Obtener el valor de 'Economico' para identificar el registro
        Economico = Registro.get("Economico", f"Registro {i + 1}")

        Faltantes = []

        # Validamos los campos requeridos y generamos checklist
        for Dato in InputRequeridos:
            if Dato not in Registro or not Registro[Dato]:  # Verifica si está vacío
                Faltantes.append(Dato)

        # Determinamos si el registro es completo o incompleto
        Estado = "Completo" if not Faltantes else "Incompleto"

        # Encabezado de cada registro con su estado
        Reporte.append(f"{Economico} -------------------------------------------------------------- ({Estado})\n")

        # Añadimos la checklist
        for Dato in InputRequeridos:
            if Dato not in Registro or not Registro[Dato]:  
                Reporte.append(f"[ ] {Dato}\n")  # Casilla vacía si falta el campo
                bandera += 1

            else:
                Reporte.append(f"[x] {Dato}\n")  # Casilla marcada si el campo está presente

        Reporte.append("\n")

        if bandera == 0:
            Registro['Usuario']='Tonatiuh'
            data = Registro

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:

                print("se hizo el post")
                print(response.text)
                if 'Inexistencia Token' in response.text:
                    Reporte.append("Inexistencia Token")

                if 'Exito' in response.text:
                    Reporte.append("Exito")
                
            else:
                    print(f"Error al acceder a la URL: {response.status_code}")
        else:
            Reporte.append("!!Datos Incompletos!!")

        bandera= 0

    # Guardamos el reporte en un archivo de texto
    NombreReporte = "Reporte.txt"
    with open(NombreReporte, 'w', encoding = 'utf-8') as file:
        file.writelines(Reporte)

    print(f"Reporte generado: {NombreReporte}")

    MostrarPopup("Se validaron y se subieron los datos aceptados")

try:
    with open('Datos.txt', 'r') as archivo:
        contenido = archivo.read()

    # Convierte el texto en un diccionario de Python
    datos = json.loads(contenido)
    ValidarInformacion(datos)

except FileNotFoundError:
    print("Error: El archivo no fue encontrado.")
except json.JSONDecodeError:
    print("Error: El contenido del archivo no es un JSON válido.")
except KeyError as e:
    print(f"Error: La clave {e} no existe en el JSON.")
except Exception as e:
    print("Ocurrió un error inesperado:", str(e))


