# -*- coding: utf-8 -*-
#

import re
import unicodedata

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