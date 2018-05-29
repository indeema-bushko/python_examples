import subprocess
import threading
import time
import sys
import shlex
import os
import requests

date_time_format = '%Y-%m-%d %H:%M:%S'

delta_time = 10
is_routed = False
elapsed_time_sec = delta_time


def status():
    print(' - tcp_sniffer_main::status')
    while True:
        global elapsed_time_sec

        if elapsed_time_sec < 0:
            not_routed()
            global delta_time
            # time.sleep(delta_time / 2)
            elapsed_time_sec = delta_time
        # time.sleep(1)
        elapsed_time_sec -= 1
        print(' - elapsed_time : {}'.format(elapsed_time_sec))


def fill_buffer(process):
    print(' -- fill --')
    while True:
        process.stdin.write('############################################'.encode('utf-8'))
        # time.sleep(1)
    # url = 'http://127.0.0.1:80'
    # while True:
    #     headers = {'content-type': 'application/json'}
    #     try:
    #         print(' - fill buffer')
    #         response = requests.get(url, headers=headers)
    #         # print(str('{} - Response STATUS CODE: {}, TEXT: {}'.format(time.strftime(date_time_format),
    #         #                                                            response.status_code, response.text)))
    #     except requests.ConnectionError as e:
    #         # print(' - ConnectionError: {}'.format(e))
    #         time.sleep(2)
    #
    #     # time.sleep(1)


def not_routed():
    print(' - tcp_sniffer::not_routed')


def routed():
    print(' - tcp_sniffer::routed')


def print_help():
    print(' - help: command line arguments for (tcpdump)')
    print(' - [dst=] destination host address, this param is required')
    print(' - (src=) source host address, default is None')
    print(' - (port=) port number for listening, default 80')
    print(' - (size=) dump size in bytes default 128')


def myrun(cmd):
    """from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        print(line)
        if line == '' and p.poll() != None:
            break
    return ''.join(stdout)


if __name__ == '__main__':
    print(' - tcp_sniffer::main')

    command = 'sudo tcpdump '
    src = None
    dst = None
    port = '80'
    size = 128
    elapsed_time_sec = delta_time

    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            print(' - {} argv: {}'.format(i, sys.argv[i]))
            if 'src=' in sys.argv[i]:
                src = sys.argv[i].replace('src=', '')
                print(' - src host: {}'.format(src))
            elif 'dst=' in sys.argv[i]:
                dst = sys.argv[i].replace('dst=', '')
                print(' - dst host: {}'.format(dst))
            elif 'port=' in sys.argv[i]:
                port = sys.argv[i].replace('port=', '')
                print(' - port: {}'.format(port))
            elif 'size=' in sys.argv[i]:
                size = sys.argv[i].replace('size=', '')
                print(' - size: {}'.format(size))
            elif '-h' in sys.argv[i]:
                print_help()
                sys.exit(0)
            elif '-v':
                print('tcp_sniffer v 0.0.1')
                sys.exit(0)

    if not dst:
        raise ValueError(' - error: [des] argument is not present')
        print_help()
        sys.exit(0)

    if not src:
        command = command + '-n dst host {} and port {}'.format(dst, port)
    else:
        command = command + '-s {} -n src host {} and dst host {} and port {}'.format(size, src, dst, port)

    print(' - start command: {}'.format(command))

    # threading.Thread(target=status).start()

    # threading.Thread(target=fill_buffer()).start()

    # command = 'sudo tcpdump -n port 80 -w dump'
    # process = subprocess.Popen(shlex.split(command))

    # process = subprocess.Popen(['tcpdump', '-v'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

    # for line in iter(process.stdout.readline, b''):
    #     print("{} >> {}".format(time.strftime(date_time_format), line.rstrip()))
    #     process.stdout.flush()
    #
    # process.terminate()
    # process.wait()

    # while True:
    #     output = process.communicate()
    #     if output:
    #         print('{} -- {}'.format(time.strftime(date_time_format), output))
    #         elapsed_time_sec = delta_time
    #         routed()

    # sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    # process.stdout.flush()

    # threading.Thread(target=fill_buffer, args=(process,)).start()
    while True:
        output = process.stdout.readline()
        if dst in str(output):
            print(' --------------------------------------------------------------- ')
            print('{} -- {}'.format(time.strftime(date_time_format), output))
            print(' --------------------------------------------------------------- ')


    # while True:
    #     print(' ------------- ------------------------------------------------------------------')
    #     print(' ------------- ------------------------------------------------------------------')
    #     print(' ------------- ------------------------------------------------------------------')
    #     p = subprocess.check_call(shlex.split(command))

