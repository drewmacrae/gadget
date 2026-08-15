# Setup
```shell
> git submodule init
> git submodule update
> python -m venv .venv
> .venv/bin/activate
(.venv)> pip install -r requirements.txt
```

Schedule daily dumps of the sms's and status logging with `crontab -e`
by adding the lines
```crontab
#m h  dom mon dow   command
# This only writes when there are new SMS's so we can put them on the SD card
 0 0  *   *   *     /home/gadget/gadget/.venv/bin/python /home/gadget/gadget/dumpSMS.py >> /home/gadget/sms.txt 2>&1
# This happens every minute and is written to /tmp where it's placed in RAM
 * *  *   *   *     /home/gadget/gadget/.venv/bin/python /home/gadget/gadget/getStatus.py --rssi >> /tmp/rssi.log 2>&1
# Report status every day at noon (system time)
 0 12 *   *   *     /home/gadget/gadget/.venv/bin/python /home/gadget/gadget/sendStatus.py $SMS_NO >> /home/gadget/send.log 2>&1i
# Report status an hour after reboot
@reboot sleep 3600 && /home/gadget/gadget/.venv/bin/python /home/gadget/gadget/sendStatus.py $SMS_NO >> /home/gadget/send.log 2>&1

```
Where `$SMS_NO` specifies where to send the status reports as a 10 digit phone number like `13218675309`
