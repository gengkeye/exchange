source /home/seven/workspace/py3/bin/activate
python /home/seven/workspace/exchange/apps/manage.py shell_plus << EOF
from exchange.models import Bid
Bid.objects.all().delete()
EOF