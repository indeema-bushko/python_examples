import subprocess
import threading
import time
import sys
import shlex

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
            time.sleep(delta_time / 2)
            elapsed_time_sec = delta_time
        time.sleep(1)
        elapsed_time_sec -= 1


def not_routed():
    print(' - tcp_sniffer::not_routed')


def routed():
    print(' - tcp_sniffer::routed')


def print_help():
    print(' - help: command line arguments for (tcpdump)')
    print(' - (src=) source host address, default 127.0.0.1')
    print(' - (port=) port number for listening, default 80')
    print(' - (size=) dump size in bytes')


if __name__ == '__main__':
    print(' - tcp_sniffer::main')
    print(' - argv: {}'.format(sys.argv))

    command = 'sudo tcpdump '
    src = '127.0.0.1'
    dst = None
    port = '80'
    size = '128'
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
        raise ValueError('A [des] argument is not present')
        print_help()
        sys.exit(0)

    command = command + '-s {} -n dst host {} and port {}'.format(size, dst, port)
    print(' - start command: {}'.format(command))

    threading.Thread(target=status).start()

    while True:
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            out_str = output.strip()
            print(out_str)
            print(' - des {}'.format(dst))
            # Do process of the output, Do process of the output, make comparison if src or dst host exist
            if dst in str(out_str):
                print(' - routed src: {}, dst: {}'.format(src, dst))
                routed()
                elapsed_time_sec = delta_time
        time.sleep(delta_time / 2)

        process.poll()
        # while True:
        #     output = process.stdout.readline()
        #     if output == '' and process.poll() is not None:
        #         break
        #     if output:
        #         out_str = output.strip()
        #         print(out_str)
        #         print(' - des {}'.format(dst))
        #         # Do process of the output, Do process of the output, make comparison if src or dst host exist
        #         if dst in str(out_str):
        #             print(' - routed src: {}, dst: {}'.format(src, dst))
        #             routed()
        #             elapsed_time_sec = delta_time
        #
        #     process.poll()

    time.sleep(1)
