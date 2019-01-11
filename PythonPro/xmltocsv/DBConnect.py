# encoding: utf-8
'''
@Author: liteng
@Contact: vnddllit@cn.ibm.com
@File: DBConnect
@Time: 2018/11/15 15:27
'''

import ibm_db
from xmltocsv import Common
from xmltocsv import Log

class DBConnect:

    # DBCONFIG
    database = ''
    host = ''
    port = ''
    protrol = ''
    uid = ''
    pwd = ''
    schema = ''
    conn_str = ''

    LOG = Log.log().getLogger()

    def __init__(self):
        # DBCONFIG
        common = Common.Common()
        self.database = common.getConfValue('DB', 'database')
        self.host = common.getConfValue('DB', 'host')
        self.port = common.getConfValue('DB', 'port')
        self.protrol = common.getConfValue('DB', 'protrol')
        self.uid = common.getConfValue('DB', 'uid')
        self.pwd = common.getConfValue('DB', 'pwd')
        self.schema = common.getConfValue('DB', 'schema')
        self.conn_str = 'database=%s;hostname=%s;port=%s;protocol=%s;uid=%s;pwd=%s' % (
            self.database, self.host, self.port, self.protrol, self.uid, self.pwd)
        print(self.conn_str)

    def connect(self):
        try:
            conn = ibm_db.connect(self.conn_str, '', '')
            ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
            self.LOG.info('--------Connect Success------%s---'%(self.conn_str))
            return conn
        except Exception as ex:
            self.LOG.error('--------Connect Fail------%s----%s-----' %(self.conn_str, ex))






