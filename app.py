from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import serial

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize Serial Port
try:
    ser = serial.Serial('COM8', 9600)  # Update 'COM8' if your port is different
    print("Serial port opened successfully.")
except serial.SerialException as e:
    ser = None
    print(f"Failed to open serial port: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    print("Received Message: " + msg)
    
    # Sending the received message to the serial port
    if ser:
        try:
            # Ensure the message is sent as bytes, same as in your standalone test
            print(f"Sending to serial: {msg}")  # Debug statement
            ser.write(msg.encode('utf-8'))  # Sending the message to the serial port
            print("Message sent to Arduino.")
        except Exception as e:
            print(f"Error sending message: {e}")
    
    # Responding back to the client
    emit("response", {'data': 'Message Received: ' + msg})

if __name__ == '__main__':
    socketio.run(app)
