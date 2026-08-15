import serial
import argparse
import time
import typing
from atcommand import ATCommand, NOECHO

parser = argparse.ArgumentParser()
parser.add_argument("--port","-p",default=None)
args = parser.parse_args()


NOECHO.execute()
for i in range(0,30):
    result,message=ATCommand('CMGR',str(i)).execute()
    if result != 'OK' or message != ['','']:
       print(message)
       ATCommand('CMGD',str(i)).execute()

