#!/bin/bash
Year=$1
Month=$2
Day=$3
Hour=$4
curl 'http://192.168.X.XXX/cgi-bin/api.cgi?cmd=Search&token=1910cde8f7ee7e8' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Origin: http://192.168.X.XXX' \
  -H 'Referer: http://192.168.X.XXX/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw '[{"cmd":"Search","action":1,"param":{"Search":{"channel":0,"onlyStatus":0,"streamType":"main","StartTime":{"year":'"$Year"',"mon":'"$Month"',"day":'"$Day"',"hour":'"$Hour"',"min":0,"sec":0},"EndTime":{"year":'"$Year"',"mon":'"$Month"',"day":'"$Day"',"hour":'"$Hour"',"min":59,"sec":59}}}}]' \
  --compressed \
  --insecure
