import serial  # Importa la librería pyserial
import time
import csv

puerto_serie = 'COM3'  # Puerto serial
baud_rate = 9600  
datos_arduino = []


# Abre el puerto serie
ser = serial.Serial(puerto_serie, baud_rate)
time.sleep(2)  # Espera 2 segundos para asegurar que la conexión se establezca

while True:
    if ser.in_waiting > 0:  # Si hay datos disponibles para leer
        datos = ser.readline().decode('utf-8').strip()  # Lee la línea y la decodifica
        #readline() lee todos los datos hasta encontrar un salto de línea,decode('utf-8') convierte los bytes leídos en una cadena de texto utilizando la codificación,strip() elimina los espacios en blanco
        number = datos.split(',')
        print(f"Valor recibido: {number}")  # Imprime el valor en la terminal
        datos_arduino.append(number)

        with open('0001.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(datos_arduino)
    