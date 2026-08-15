import re
from statistics import mean

errors = 0
bit_error_rates = []
network_signal_qualities = []
with open("/tmp/rssi.log", "r") as logfile:
    for line in logfile.readlines():
        result = re.search(r"^(\d+)\.(\d+)$",line)
        if result:
            bit_error_rates+=[int(result.group(1))]
            network_signal_qualities+=[int(result.group(2))]
        else:
            errors+=1

def getRSSISummary():
    return f"{len(bit_error_rates)}rcrds, {errors}errs.\n"\
            f"BER: {min(bit_error_rates)}-{mean(bit_error_rates):.1f}-{max(bit_error_rates)}\n"\
           f"NSQ: {min(network_signal_qualities)}-{mean(network_signal_qualities):.1f}-{max(network_signal_qualities)}\n"

if __name__=="__main__":
    print(getRSSISummary())
