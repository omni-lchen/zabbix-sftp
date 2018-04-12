# zabbix-sftp

SFTP monitoring with python sftp in zabbix.

# Metrics

* Response Code: 0=OK, 1=Fail
* Response Time (second)

# Prerequisites

  * python
  * cryptography
  * pysftp
  * zabbix user ssh key
  * jq
  * zabbix sender

# Installation

Install cryptography and pysftp modules in python on zabbix server or zabbix proxy, below are the installation commands on ubuntu: 

  * apt-get install python-pip
  * pip install --upgrade pip
  * apt-get install build-essential libssl-dev libffi-dev python-dev
  * pip install cryptography
  * pip install pysftp

Generate zabbix user ssh key on zabbix server or zabbix proxy, ssh key password is required.

    # chmod g+w <zabbix_user_homepath>
    # mkdir <zabbix_user_homepath>/.ssh
    # chown zabbix. <zabbix_user_homepath>/.ssh
    # sudo -u zabbix ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (<zabbix_user_homepath>/.ssh/id_rsa): 
    Created directory '<zabbix_user_homepath>/.ssh'.
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in <zabbix_user_homepath>/.ssh/id_rsa.
    Your public key has been saved in <zabbix_user_homepath>/.ssh/id_rsa.pub.

Add zabbix user ssh public key to the remote sftp user home authorized keys.

    <sftp_user_homepath>/.ssh/authorized_keys

Upload an empty file called "test" in the sftp user home directory.

Copy the scripts to zabbix server external scripts directory, normally /usr/lib/zabbix/externalscripts.

  * /usr/lib/zabbix/externalscripts# chmod +x sftpCheck.py
  * /usr/lib/zabbix/externalscripts# chmod +x sftpCheck.sh

Import the sftp check template and create a new host in zabbix, link the template to the new host, set the value of the following macros on the template,
 
  * {$SFTP_KEY_FILE} - <zabbix_user_homepath>/.ssh/id_rsa
  * {$SFTP_KEY_PASS} - password of zabbix user private key

and add the value of sftp server hostname and login user macros on the new host.

  * {$SFTP_HOST} - sftp server hostname
  * {$SFTP_USER} - sftp login user
