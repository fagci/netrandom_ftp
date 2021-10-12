#!/usr/bin/env python3
from ftplib import FTP, all_errors
from ipaddress import IPv4Address
from random import randint
from threading import Event, Thread

TT = ('file', 'dir')


def scan(run_event: Event):
    while run_event.is_set():
        ip_address = IPv4Address(randint(0x1000000, 0xE0000000))
        if not ip_address.is_global:
            continue

        try:
            with FTP(str(ip_address), timeout=2) as ftp:
                ftp.login()
                ff = [n for n, p in ftp.mlsd() if p.get('type', '') in TT]
                if ff:
                    print(ip_address, *ff)
        except all_errors:
            pass
        except (ConnectionError, UnicodeDecodeError):
            pass


def main():
    pool = []
    run_event = Event()
    run_event.set()

    try:
        for _ in range(1024):
            t = Thread(target=scan, args=(run_event, ))
            t.start()
            pool.append(t)

        for t in pool:
            t.join()
    except KeyboardInterrupt:
        run_event.clear()
        print('\rStop')


if __name__ == '__main__':
    main()
