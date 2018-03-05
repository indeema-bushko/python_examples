import subprocess
import time
import re

if __name__ == '__main__':
    print('tcp_sniffer::main')

    # process = subprocess.Popen('sudo tcpdump -n dst port 80', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    # process = subprocess.Popen('sudo tcpdump -n src 192.168.1.146', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    process = subprocess.Popen('sudo tcpdump -i wlp2s0' , stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    while True:
        for row in iter(process.stdout.readline, b''):
            _str = row.rstrip()
            if re.match(r'192.168.1.146', _str):
                print('-------------------------------------------------------------------------')
                print(_str)
                print('-------------------------------------------------------------------------')
        # out = process.stdout.read()
        # print('--------------------------------------------------------------------------')
        # print(out)
        # print('--------------------------------------------------------------------------')
        # time.sleep(1)
