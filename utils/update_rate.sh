#!/bin/bash
#
source /home/ec2-user/py3/bin/activate
python /home/ec2-user/exchange/apps/manage.py shell_plus << EOF
from exchange.tasks import update_rate
update_rate()
EOF
