#!/var/www/html/binweb/bin_temperature/venv/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
#sys.path.insert(0,"/var/www/html/python/")
sys.path.insert(0,"/var/www/html/binweb/bin_temperature/")

#from flaskapp import app as application
from graphs import app as application
application.secret_key = '123'
