import serial
import time

# Configuración del puerto serie
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Ajusta el puerto según tu configuración
time.sleep(2)  # Esperar a que el Arduino se reinicie

try:
    while True:
        # Enviar datos de prueba, ajusta según sea necesario
        ser.write(b'1,1\n')
        # Leer la respuesta del Arduino
        line = ser.readline().decode('utf-8').rstrip()
        if line:
            try:
                state1, state2 = map(int, line.split(','))
                print(f"Leído -> Pin 2: {state1}, Pin 3: {state2}")
                print(f"Enviado -> Pin 4: {state1}, Pin 5: {state2}")
            except ValueError:
                print(f"Error de formato en la línea recibida: {line}")
        
        time.sleep(1)  # Ajusta el retardo según tus necesidades

except serial.SerialException as e:
    print(f"Error en la comunicación serial: {e}")
except KeyboardInterrupt:
    print("Interrupción por teclado recibida. Cerrando el puerto serie.")
finally:
    ser.close()
    print("Puerto serie cerrado.")
