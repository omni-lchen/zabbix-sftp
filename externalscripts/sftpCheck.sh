#!/bin/bash

# Date:                 09/04/2018
# Author:               Long Chen
# Description:          A script to send sftp check stats to zabbix server by using zabbix sender
# Requires:             sftpcheck.py, jq, zabbix sender

SFTP_HOST=$1
SFTP_USER=$2
SFTP_KEY_FILE=$3
SFTP_KEY_PASS=$4
ZABBIX_HOST=$5
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

getSftpCheckResults(){
  sftp_check_results=$(python $SCRIPT_DIR/sftpCheck.py "$SFTP_HOST" "$SFTP_USER" "$SFTP_KEY_FILE" "$SFTP_KEY_PASS")
  echo $sftp_check_results | jq -c .[] | while read i; do echo $ZABBIX_HOST `echo $i | jq -r '.|"\(.key) \(.value)"'`; done
}

# Send the results to zabbix server by using zabbix sender
result=$(getSftpCheckResults | /usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -i - 2>&1)
response=$(echo "$result" | awk -F ';' '$1 ~ /^info/ && match($1,/[0-9].*$/) {sum+=substr($1,RSTART,RLENGTH)} END {print sum}')
if [ -n "$response" ]; then
        echo "$response"
else
        echo "$result"
fi