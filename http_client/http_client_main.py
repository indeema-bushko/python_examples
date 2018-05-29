import requests
import signal
import sys
import time

date_time_format = '%Y-%m-%d %H:%M:%S'


def exit_handler(sys_signal, frame):
    print(' - http_client_main::exit_handler')
    sys.exit(0)


def print_help():
    print(' - help: command line arguments')
    print(' - (host) an ip address of destination server')
    print(' - (port) port number of destination server')
    print(' - (delay) delay in seconds between request')


if __name__ == '__main__':
    print(' - http_client_main::main')
    signal.signal(signal.SIGINT, exit_handler)

    host = '127.0.0.1'
    port = '80'
    delay = 10

    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            if 'host=' in sys.argv[i]:
                host = sys.argv[i].replace('host=', '')
            elif 'port=' in sys.argv[i]:
                port = sys.argv[i].replace('port=', '')
            elif 'delay=' in sys.argv[i]:
                delay = int(sys.argv[i].replace('delay=', ''))
            elif '-h' in sys.argv[i]:
                print_help()
                sys.exit(0)
            elif '-v' in sys.argv[i]:
                print('http_client v 0.0.1')
                sys.exit(0)

    print(' - host = {}'.format(host))
    print(' - port = {}'.format(port))
    print(' - delay = {}'.format(delay))

    url = 'http://{}:{}'.format(host, port)

    while True:
        headers = {'content-type': 'application/json'}
        try:
            response = requests.get(url, headers=headers)
            print(str('{} - Response STATUS CODE: {}, TEXT: {}'.format(time.strftime(date_time_format),
                                                                       response.status_code, response.text)))
        except requests.ConnectionError as e:
            print(' - ConnectionError: {}'.format(e))

        time.sleep(delay)

    print(' - end main')


