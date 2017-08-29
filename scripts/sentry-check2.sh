source ./config.sh

ID=$1
echo $LINE
echo "SENTRY TEST"
echo $LINE
echo
CMD="dig +short myip.opendns.com @resolver1.opendns.com"
IP=`$CMD`
echo "MY IP: $IP"
echo
echo
#curl -s https://updates-autopush.stage.mozaws.net/v1/err/crit | python -mjson.tool
echo $HOST_UPDATES
#curl -s "https://$HOST_UPDATES/v1/err/crit" | python -mjson.tool
#curl -s "https://$HOST_UPDATES/v1/err/crit" | python -mjson.tool
curl -H "Content-Type: application/json" -H "Accept: application/json" -X PUT -d '{"status":"resolved"}' -i -u $SENTRY_TOKEN:  https://sentry.prod.mozaws.net/api/0/issues/$ID/
echo
echo
