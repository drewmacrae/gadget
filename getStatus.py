import serial
import argparse
import time
import typing
from atcommand import ATCommand, NOECHO
import re
import datetime
import os
from rssiLogParser import getRSSISummary

def getRSSI(retries:int = 0):
    for eachtry in range(retries+1):
        response,message=ATCommand('CSQ').execute()
        for line in message:
            result = re.search(r'\+CSQ:\s*(\d*),(\d*)',line)
            if result:
                network_signal_quality = result.group(1)
                bit_error_rate = result.group(2)
                return bit_error_rate , network_signal_quality
    raise HardwareFlakinessError(f"Failed to read network time after {retries+1} attempts. Got {message}{response}")


def getNetworkTime(retries:int = 0):
    for eachtry in range(retries+1):
        response,message=ATCommand('CCLK?').execute()
        for line in message:
            result = re.search(r'\+CCLK:\s*"([/\d]*),(\d+:\d+)',line)
            if result:
                date = result.group(1)
                time = result.group(2)
                return date, time
    raise HardwareFlakinessError(f"Failed to read network time after {retries+1} attempts. Got {message}{response}")

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

def get_summary():
    NOECHO.execute()
    summary = " ".join(getNetworkTime(10))+"\n"
    summary+=f"utm: {int(get_uptime())}(s)\n"
    summary+=",".join([str(x)[:4] for x in os.getloadavg()])+"\n"
    summary+=getRSSISummary()
    with open("/home/pygu/sms.txt","r") as smses:
       for line in smses.readlines()[::-1]:
           result = re.search(r'\+(\d{11}).*?,\s*\'(.*)\',',line)
           if result:
               number = result.group(1)
               message = result.group(2)
               summary+=number+":"+message+"\n"
    return summary[:160]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rssi","-r",action="store_true",help="rssi for logs")
    parser.add_argument("--time","-t",action="store_true",help="read network time from modem")
    parser.add_argument("--summary","-s",action="store_true",help="provide a summary of less than 160 characters")

    args = parser.parse_args()
    
    NOECHO.execute()
    if args.rssi:
        print(".".join(getRSSI(10)))
    if args.time:
        print(",".join(getNetworkTime(10)))
    if args.summary:
        summary=get_summary()
        print(str(len(summary))+"/160\n")
        print(summary)
