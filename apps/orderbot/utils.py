# -*- coding: utf-8 -*-
#

import re

def convert_str_to_list(text, seperator=' '):
    text_list = text.split(seperator)
    return list(filter(None, text_list))

def convert_str_to_num_list(text, seperator=' '):
    text_list = re.sub(r'\D', seperator, text).split(seperator)
    return list(filter(None, text_list))




