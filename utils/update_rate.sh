#!/bin/bash
#
source /home/seven/workspace/py3/bin/activate
python /home/seven/workspace/exchange/apps/manage.py shell_plus << EOF
from exchange.tasks import update_rate
update_rate()
EOF