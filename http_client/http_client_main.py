import  requests
import signal
import sys
import time


def exit_handler(sys_signal, frame):
    print(' - http_client_main::exit_handler')
    sys.exit(0)


if __name__ == '__main__':
    print(' - http_client_main::main')
    signal.signal(signal.SIGINT, exit_handler)

    delay = 10
    if len(sys.argv) > 1:
        print(' - delay: {}'.format(sys.argv[1]))
    else:
        print(' - delay: default')

    while True:
        url = 'http://192.168.0.89:80'
        headers = {'content-type': 'application/json'}
        response = requests.get(url, headers=headers)
        print(str(' - Response STATUS CODE: {}, TEXT: {}'.format(response.status_code, response.text)))
        time.sleep(delay)

    print(' - end main')