import argparse
from getStatus import get_summary
from atcommand import ATCommand, sendSMS



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sms_no",help="Where to send reports of status")
    args = parser.parse_args()
    summary = get_summary()
    sendSMS(args.sms_no,summary)
