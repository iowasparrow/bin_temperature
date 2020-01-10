bintemp.conf virtaul host settings

WSGIDaemonProcess flaskapp user=pi
WSGIProcessGroup flaskapp
WSGIScriptAlias /bin_temperature /var/www/html/binweb/bin_temperature/flaskapp.wsgi


WSGIDaemonProcess binapp user=pi
WSGIProcessGroup binapp
WSGIScriptAlias /binapi /var/www/html/binweb/binapi/binapp.wsgi

ServerName bintemp.com
ServerAlias www.bintemp.com
ServerAdmin grant@siebrecht.us
DocumentRoot /var/www/html/binweb


mosquitto.conf settings

listener 1883

listener 9001
protocol websockets


rc.local settings
sleep 20
#sudo -H -u pi /usr/bin/python3 /var/www/html/binweb/bin_temperature/logger.py &
#sudo -H -u pi /usr/bin/python3 /var/www/html/binweb/bin_temperature/subMqtt.py &

crontab settings

*/15 * * * * /usr/bin/python3 /var/www/html/binweb/bin_temperature/appDHT.py
5 */1 * * * /usr/bin/python3 /var/www/html/binweb/bin_temperature/check_lowtemp.py
*/1 * * * * /usr/bin/python3 /var/www/html/binweb/bin_temperature/publishmqtt.py
*/1 * * * * /usr/bin/python3 /var/www/html/binweb/bin_temperature/logger.py



