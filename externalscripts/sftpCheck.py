#!/usr/bin/env python

# Date:                 09/04/2018
# Author:               Long Chen
# Description:          A script to test sftp connection and file download and output response code and response time.
# Requires:             cryptography, pysftp

import sys
import time
import json
import pysftp
import warnings
import logging

class sftpCheck(object):
    def __init__(self):
        self.start_time = time.time()
        self.end_time = time.time()
        self.__conn = None
        self.__status = 0
        self.__duration = 0
        self.__metrics = []

    # Add each mectrics to the metrics list
    def addMetrics(self, k, v):
        dict = {}
        dict['key'] = k
        dict['value'] = v
        self.__metrics.append(dict)

    # Connect to sftp server with private key
    def connect(self, h, u, k, kp):
        # Workaround for: UserWarning: Failed to load HostKeys from /root/.ssh/known_hosts.
        # You will need to explicitly load HostKeys (cnopts.hostkeys.load(filename)) or disableHostKey checking (cnopts.hostkeys = None).
        warnings.filterwarnings('ignore', '.*hostkeys = None*',)
        # Workaround for: No handlers could be found for logger "paramiko.transport"
        # (see https://github.com/fabric/fabric/issues/51#issuecomment-96341022)
        logging.basicConfig()
        paramiko_logger = logging.getLogger("paramiko.transport")
        paramiko_logger.disabled = True
        if self.__conn is None:
            try:
                cnopts = pysftp.CnOpts()
                # disable host key checking
                cnopts.hostkeys = None
                self.start_time = time.time()
                self.__conn = pysftp.Connection(host=h, username=u, private_key=k, private_key_pass=kp, cnopts=cnopts)
                self.__conn.timeout = 15
            except Exception as e:
                #print 'Error in sftp connection: %s' % str(e)
                self.__status = 1

    # Check file exists on sftp server
    def verifyFileExists(self, f):
        if self.__conn is None:
            self.__status = 1
        else:
            try:
                file = self.__conn.isfile(f)
                if not file:
                    self.__status = 1
            except Exception as e:
                #print 'Error in sftp connection: %s' % str(e)
                self.__status = 1

    # Close sftp connection
    def close(self):
        if self.__conn is not None:
            self.__conn.close()
            self.end_time = time.time()

    # Get sftp download duration
    def getDuration(self):
        self.__duration = float("{0:.3f}".format(self.end_time - self.start_time))
        self.addMetrics('sftp.responsetime', self.__duration)
        self.addMetrics('sftp.responsecode', self.__status)

    def printMetrics(self):
        print str(json.dumps(self.__metrics))

if __name__ == '__main__':
    sftp_host = sys.argv[1]
    sftp_user = sys.argv[2]
    sftp_key_file = sys.argv[3]
    sftp_key_pass = sys.argv[4]
    remote_file = 'test'
    sftpCheck = sftpCheck()
    sftpCheck.connect(sftp_host, sftp_user, sftp_key_file, sftp_key_pass)
    sftpCheck.verifyFileExists(remote_file)
    sftpCheck.close()
    sftpCheck.getDuration()
    sftpCheck.printMetrics()