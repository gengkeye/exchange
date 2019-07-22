#!/bin/bash

source /home/ec2-user/py3/bin/activate
python /home/ec2-user/exchange/apps/manage.py shell_plus << EOF
from exchange.tasks import send_bids_period
send_bids_period.run()
EOF
