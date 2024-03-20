from serial import Serial, SerialException
import time
import board
import RPi.GPIO as GPIO

enable_pin = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.output(enable_pin, 1)

pc_mode_start = "spc set pcmode"
pc_mode_end = "spc end pcmode"
delete_steps = "spc del steps"
add_step_one = "spc add step 5000 10"
get_steps = "spc get steps"
start = "spc run"

def connect(com_port) -> Serial:
    try:
        spc_serial_connection = Serial(com_port, baudrate=9600, timeout=None)
        if spc_serial_connection.is_open is False:
            raise Exception("Connection's is_open is False, connection failed.")
        else:
            return spc_serial_connection
    
    except SerialException as E:
        print(E)
        return None
    
def send_command(command: str, spc_connection: Serial) -> None:
    spc_connection.write(command.encode("ascii"))

def board_return(spc_connection: Serial) -> str:
    return_data = spc_connection.read_all()
    return_data = return_data.decode('utf-8')
    return return_data

def console_loop(spc_connection: Serial):
    while(True):
        cmd = input(">")
        if cmd.lower() == "stop":
            break

        try:
            send_command(cmd, spc_connection)
            time.sleep(0.5)
            data = board_return(spc_connection)
            print(f"Board returned: {data}")
        except Exception as E:
            print(E)

def run():
    input()
    spc = connect("/dev/ttyACM0")

    if spc is None:
        print("Connection Failed, see exception above.")
        input()
        exit()
        
    console_loop(spc)

    input()
    exit()

if __name__ == "__main__":
    run()
