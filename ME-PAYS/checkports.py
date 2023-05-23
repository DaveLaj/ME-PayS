import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())  # Use list() to force evaluation of the generator

if len(ports) == 0:
    print("No serial ports found.")
else:
    for port in ports:
        print(f"Port: {port.device} - Description: {port.description}")