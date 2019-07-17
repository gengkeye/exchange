#!/bin/bash

source /home/ec2-user/py3/bin/activate
python /home/ec2-user/exchange/apps/manage.py shell_plus << EOF
from exchange.models import Bid
Bid.objects.all().delete()
EOF
