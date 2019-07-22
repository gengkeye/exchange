#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

from threading import Thread
import os
import subprocess


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

apps_dir = os.path.join(BASE_DIR, 'apps')


def start_celery():
    os.chdir(apps_dir)
    os.environ.setdefault('C_FORCE_ROOT', '1')
    os.environ.setdefault('PYTHONOPTIMIZE', '1')
    print('start celery')
    subprocess.call('celery -E -A exchange worker -B -s /tmp/celerybeat-schedule -l debug', shell=True)


def main():
    t = Thread(target=start_celery, args=())
    t.start()
    t.join()


if __name__ == '__main__':
    main()
