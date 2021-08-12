import pyfiglet
import platform
import os
import sys
import socket
import threading
from time import sleep
from queue import Queue

def banner():
    banner = pyfiglet.figlet_format('PORT SCANNER')
    print('\033[93m'+banner+'\033[m')


ports = Queue()

first_port = 1
last_port = 65535


for i in range(first_port, last_port+1):
    ports.put(i)


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')


def validate_ip(ip):

    splited_ip = ip.split('.') 

    if len(splited_ip) == 4:
        for ip_part in splited_ip:
            if len(ip_part) <= 3 and len(ip_part) > 0:
                return True
            
            else:
                return False

    else:
        return False


def scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        res = sock.connect_ex((target, port))
            
        if res == 0:
            print(f'Port {port} is open!')

        sock.close()
    except:
        pass


def worker():
    while not ports.empty():
        port = ports.get()
        scan(port)
    ports.task_done()


def start_workers():
    threads = []

    for i in range(500):
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def start_scanning():
    clear_screen()
    banner()
    sleep(1)
    print(f'Scanning the ports from {first_port} to {last_port}...\n')
    start_workers()


banner()


try:
    target = sys.argv[1]
except IndexError:
    raise ValueError('\033[91mYou need to pass an IP address as an argument! e.g.'+
                     'python portscanner.py an.ip.address.here\033[m')


print('\033[93m'+
      '--------------------Welcome to the port scanner!--------------------'+
      '\033[m')


print(f'\n\nThis program will scan now the ports of the address {target}')

while True:
    ip_is_okay = input('Is this okay? [Y/N]')

    if ip_is_okay.strip().upper() == 'Y':
        break

    elif ip_is_okay.strip().upper() == 'N':

        while True:
            new_ip = input('Enter a new IP: ')
            if validate_ip(new_ip):
                target = new_ip
                print('\033[34mYou succefully changed the target IP adress.\033[m')
                sleep(1.5)
                break

            else:
                print('''\033[91mERROR! The IP you writed is invalid. Please write 
an valid ip address, in the format: 000.000.000.000\033[m \n''')
                sleep(2)
                continue

        break

    else:
        continue


start_scanning()

print('\n\033[93mAll the ports were scanned. Goodbye!\033[m')
