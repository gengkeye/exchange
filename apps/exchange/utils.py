# -*- coding: utf-8 -*-
#

import re
import unicodedata
import json
from functools import wraps

from django.db.utils import ProgrammingError, OperationalError
from django.core.cache import cache
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule


def convert_str_to_list(text, seperator=' '):
    text_list = text.split(seperator)
    return list(filter(None, text_list))

def convert_str_to_num_list(text, seperator=' '):
    text_list = re.sub(r'\D', seperator, text).split(seperator)
    return list(filter(None, text_list))

def chr_width(c):
    if (unicodedata.east_asian_width(c) in ('F','W','A')):
        return 2
    else:
        return 1

def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj

def trans(text):
    h = {
        "人民币": "CNY",
        "CNY": "CNY",
        "美元": "USD",
        "美金": "USD",
        "USD": "USD",
        "皮索": "PHP",
        "PHP": "PHP",
        "比索": "PHP",
        "台币": "TWD",
        "新台币": "TWD",
        "TWD": "TWD",
        "HKD": "HKD",
        "港币": "HKD",
        "香港币": "HKD",
    }
    try:
        return h[text.strip().upper()]
    except:
        return None

def mapping_restaurant(text):
    h = {
        "点餐": "restaurant",
        "菜单": "restaurant",
        "早餐": "breakfast",
        "午餐": "lunch",
        "晚餐": "lunch",
        "奶茶": "milk tea",
        "水果": "fruit",

        "MAKATI": "makati",
        "玛卡提": "makati",
        "玛卡蹄": "makati",
        "玛卡题": "makati",
        "玛卡踢": "makati",
        "马尼拉": "manila",

        "码卡提": "makati",
        "码卡提": "makati",
        "玛卡提": "makati",

        "PASAY": "pasay",
        "PASSAY": "pasay",
        "怕赛": "pasay",
        "爬赛": "pasay",
        "帕赛": "pasay",
        "趴赛": "pasay",

        "曼达卢永": "mandaluyong",
        "曼达卢勇": "mandaluyong",
        "MANDALUYONG": "mandaluyong",

        "BGC": "bgc",
        "阿拉邦": "alabang",
        "ALABANG": "alabang",
    }
    try:
        return h[text.strip().upper()]
    except:
        return None

def add_register_period_task(name):
    key = "__REGISTER_PERIODIC_TASKS"
    value = cache.get(key, [])
    value.append(name)
    cache.set(key, value)


def get_register_period_tasks():
    key = "__REGISTER_PERIODIC_TASKS"
    return cache.get(key, [])


def add_after_app_shutdown_clean_task(name):
    key = "__AFTER_APP_SHUTDOWN_CLEAN_TASKS"
    value = cache.get(key, [])
    value.append(name)
    cache.set(key, value)


def get_after_app_shutdown_clean_tasks():
    key = "__AFTER_APP_SHUTDOWN_CLEAN_TASKS"
    return cache.get(key, [])


def add_after_app_ready_task(name):
    key = "__AFTER_APP_READY_RUN_TASKS"
    value = cache.get(key, [])
    value.append(name)
    cache.set(key, value)


def get_after_app_ready_tasks():
    key = "__AFTER_APP_READY_RUN_TASKS"
    return cache.get(key, [])


def create_or_update_celery_periodic_tasks(tasks):
    """
    :param tasks: {
        'add-every-monday-morning': {
            'task': 'tasks.add' # A registered celery task,
            'interval': 30,
            'crontab': "30 7 * * *",
            'args': (16, 16),
            'kwargs': {},
            'enabled': False,
        },
    }
    :return:
    """
    # Todo: check task valid, task and callback must be a celery task
    for name, detail in tasks.items():
        interval = None
        crontab = None
        try:
            IntervalSchedule.objects.all().count()
        except (ProgrammingError, OperationalError):
            return None

        if isinstance(detail.get("interval"), int):
            intervals = IntervalSchedule.objects.filter(
                every=detail["interval"], period=IntervalSchedule.SECONDS
            )
            if intervals:
                interval = intervals[0]
            else:
                interval = IntervalSchedule.objects.create(
                    every=detail['interval'],
                    period=IntervalSchedule.SECONDS,
                )
        elif isinstance(detail.get("crontab"), str):
            try:
                minute, hour, day, month, week = detail["crontab"].split()
            except ValueError:
                raise SyntaxError("crontab is not valid")
            kwargs = dict(
                minute=minute, hour=hour, day_of_week=week,
                day_of_month=day, month_of_year=month,
            )
            contabs = CrontabSchedule.objects.filter(
                **kwargs
            )
            if contabs:
                crontab = contabs[0]
            else:
                crontab = CrontabSchedule.objects.create(**kwargs)
        else:
            raise SyntaxError("Schedule is not valid")

        defaults = dict(
            interval=interval,
            crontab=crontab,
            name=name,
            task=detail['task'],
            args=json.dumps(detail.get('args', [])),
            kwargs=json.dumps(detail.get('kwargs', {})),
            enabled=detail.get('enabled', True),
        )

        task = PeriodicTask.objects.update_or_create(
            defaults=defaults, name=name,
        )
        return task


def disable_celery_periodic_task(task_name):
    from django_celery_beat.models import PeriodicTask
    PeriodicTask.objects.filter(name=task_name).update(enabled=False)


def delete_celery_periodic_task(task_name):
    from django_celery_beat.models import PeriodicTask
    PeriodicTask.objects.filter(name=task_name).delete()


def register_as_period_task(crontab=None, interval=None):
    """
    Warning: Task must be have not any args and kwargs
    :param crontab:  "* * * * *"
    :param interval:  60*60*60
    :return:
    """
    if crontab is None and interval is None:
        raise SyntaxError("Must set crontab or interval one")

    def decorate(func):
        if crontab is None and interval is None:
            raise SyntaxError("Interval and crontab must set one")

        # Because when this decorator run, the task was not created,
        # So we can't use func.name
        name = '{func.__module__}.{func.__name__}'.format(func=func)
        if name not in get_register_period_tasks():
            create_or_update_celery_periodic_tasks({
                name: {
                    'task': name,
                    'interval': interval,
                    'crontab': crontab,
                    'args': (),
                    'enabled': True,
                }
            })
            add_register_period_task(name)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorate


def after_app_ready_start(func):
    # Because when this decorator run, the task was not created,
    # So we can't use func.name
    name = '{func.__module__}.{func.__name__}'.format(func=func)
    if name not in get_after_app_ready_tasks():
        add_after_app_ready_task(name)

    @wraps(func)
    def decorate(*args, **kwargs):
        return func(*args, **kwargs)
    return decorate


def after_app_shutdown_clean(func):
    # Because when this decorator run, the task was not created,
    # So we can't use func.name
    name = '{func.__module__}.{func.__name__}'.format(func=func)
    if name not in get_after_app_shutdown_clean_tasks():
        add_after_app_shutdown_clean_task(name)

    @wraps(func)
    def decorate(*args, **kwargs):
        return func(*args, **kwargs)
    return decorate
