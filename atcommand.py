import serial
import typing
import filelock
import time

port = serial.Serial("/dev/serial0",115200)
lock = filelock.FileLock("/tmp/serial0.lock")
 
class ATCommand:
    def __init__(self,name:str,value:typing.Optional[str]=None):
        if value is not None:
            self.command = "AT+"+name+"="+value
        else:
            self.command = "AT+"+name
    def execute(self,
               timeout:float=1.0):
        with lock:
            port.write(bytearray(self.command+"\r","ascii"))
            response = b''
            end_time = time.time() + timeout
            while b'OK' not in response and b'ERROR' not in response and b'>' not in response:
                if time.time() > end_time:
                    print(response)
                    raise TimeoutError()
                response += port.read(port.in_waiting)
            
            response = response.decode().split("\r\n")
            return response[-1], response[:-1]

def sendSMS(number,message, timeout:float=1.0):
    with lock:
        result,response = ATCommand("CMGF","1").execute()
        print(response+[result])
        assert 'OK' in result
        result,response = ATCommand("CMGS",f'"{number}"').execute()
        print(response+[result])
        assert '>' in result
        port.write(bytearray(f"{message}{chr(26)}","ascii"))
        response = b''
        end_time = time.time() + timeout
        while b'OK' not in response and b'ERROR' not in response and b'>' not in response:
            if time.time() > end_time:
                print(response)
                raise TimeoutError()
            response += port.read(port.in_waiting)
            
        response = response.decode().split("\r\n")
        result = response[-1]
        response = response[:-1]
        print(response+[result])
        assert 'OK' in result     
        return result, response

NOECHO = ATCommand("")
NOECHO.command="ATE0"
