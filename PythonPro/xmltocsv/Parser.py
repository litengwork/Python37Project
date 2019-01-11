# encoding: utf-8
'''
@Author: liteng
@Contact: vnddllit@cn.ibm.com
@File: ParseringXML
@Time: 2018/11/26 15:02
'''
import pandas as pd
# from xmltocsv import DBConnect
from lxml import etree
import configparser
import ibm_db
import re

import logging.config

class log:
    # create logger
    logger = logging.getLogger("PROCESSING")
    logger.setLevel(logging.DEBUG)

    # CONFIG
    conf = configparser.ConfigParser()
    conf.read('Config.ini')
    logsrc = conf.get('RESOURCE','log_folder_src')

    infolog = logging.FileHandler('%s/Info.log'%logsrc)
    infolog.setLevel(logging.INFO)

    errorlog = logging.FileHandler('%s/Error.log'%(logsrc))
    errorlog.setLevel(logging.ERROR)

    infoFormatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
    errorFormatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')

    infolog.setFormatter(infoFormatter)
    errorlog.setFormatter(errorFormatter)

    logger.addHandler(infolog)
    logger.addHandler(errorlog)

    def getLogger(self):
        return self.logger


class Parser:
    filesrc = ''
    #CSVNAME
    ryudai1_anony_ehr_info_detail = ''
    ryudai2_anony_ehr_info_detail = ''
    ryudai3_anony_ehr_info_detail = ''
    ryudai1_anony_activity = ''
    ryudai3_anony_urination = ''
    # SQL
    selectSql = ''

    schema = ''
    sep = ''
    sqlList = []
    dict = {}
    # dbConnect = DBConnect.DBConnect()
    # conn = dbConnect.connect()
    data = pd.DataFrame()
    LOG = log().getLogger()
    file1 = ''
    database = 'SAMPLE'
    table = 'T_EHR_DETAIL_INFO_MASTER'
    host = '9.112.89.62'
    port = '50000'
    protrol = 'tcpip'
    uid = 'db2inst1'
    pwd = '123456'
    schema = 'DB2INST1'
    dburl = 'database=%s;hostname=%s;port=%s;protocol=%s;uid=%s;pwd=%s' % (database, host, port, protrol, uid, pwd)

    conn = ibm_db.connect(dburl, "", "")

    file = None

    def getConfValue(self,section,key):
        # CONFIG
        conf = configparser.ConfigParser()
        conf.read('Config.ini')
        value = conf.get(section,key)
        return value

    def __init__(self):
        self.filesrc = self.getConfValue('RESOURCE','xml_folder_src')
        # WRITE TO CSV WITH TOTALLIST
        self.file1 = open(self.filesrc + 'aaa.txt', 'w+')
        # SQL
        self.selectSql = self.getConfValue('SQL', 'select')
        header = self.getConfValue('OUTPUTCSV', 'ehr_info_header')
        header = str(header).replace('\n','')
        for item in header.split(','):
            self.dict[item] = ''
        self.file1.write(header + '\n')
        print(self.dict)
        # CSVNAME
        self.ryudai1_anony_ehr_info_detail = self.getConfValue('CSVNAME', 'ryudai1_anony_ehr_info_detail')
        self.ryudai2_anony_ehr_info_detail = self.getConfValue('CSVNAME', 'ryudai2_anony_ehr_info_detail')
        self.ryudai3_anony_ehr_info_detail = self.getConfValue('CSVNAME', 'ryudai3_anony_ehr_info_detail')
        self.ryudai1_anony_activity = self.getConfValue('CSVNAME', 'ryudai1_anony_activity')
        self.ryudai3_anony_urination = self.getConfValue('CSVNAME', 'ryudai3_anony_urination')

        self.formatFile('')


    # FORMATFILE
    def formatFile(self,filename):
        try:
            self.file = pd.read_csv(self.filesrc + self.ryudai3_anony_ehr_info_detail,sep=';', dtype='str', encoding='utf-8')
            for index in range(self.file['result_medical_xml'].count()):
                self.writebase(index)
                # print(list(self.dict.values()))
                xmlline = str(self.file['result_medical_xml'][index]).replace('=1.0\"', '=\"1.0\"')
                xmlline = xmlline.strip('\"')
                xmlline = xmlline.replace('encoding=\"UTF-8\" standalone=\"no\"','')
                html = etree.XML(xmlline)
                self.formatXmlStr(html)
                # self.writebase(index)
                # print(xmlline)
            self.LOG.info('------------------ FORMAT SUCCESS -----------------------')
        except Exception as ex:
            self.LOG.error('----------------- FORMAT FAIL -----------%s------------' % (ex))

    def formatXmlStr(self, xmlstr):
        result = xmlstr.xpath('//meditems/meditem/@branch | //meditems/meditem/@code | //meditems/meditem/@name | //meditems/meditem/text()')
        result = [result[i:i + 4] for i in range(0, len(result), 4)]
        self.getItem(result)
        # print(result)

    def getItem(self, res):
        for array in res:
            sql = "SELECT LTRIM(RTRIM(COLUMN_NAME)) FROM %s.%s WHERE branch = '%s' AND code = '%s' AND name = '%s'"%(self.schema, self.table, array[0], array[1],array[2])
            # print(sql)
            stmt = ibm_db.exec_immediate(self.conn, sql)
            result = ibm_db.fetch_both(stmt)

            self.dict[str(result[0])] = array[3]
            # print(array[3])
            # print(result[0])
        # print(self.dict.values())
        # print(list(self.dict.values()))
        # self.dict['encrypt_ehr_id_base64'] =

        # print(len(list(self.dict.values())))
        # print("key:",len(list(self.dict.keys())))
        # print(list(self.dict.keys()))

        self.file1.write(','.join(list(self.dict.values())) + '\n')

        # self.file1.write(str(list(self.dict.keys())).strip('[]')+ '\n')
    def writebase(self, index):
        self.dict['encrypt_ehr_id_base64'] = self.file['encrypt_ehr_id_base64'][index]
        self.dict['delete_flg'] = self.file['delete_flg'][index]
        self.dict['update_virsion'] = self.file['update_virsion'][index]
        self.dict['created_dt'] = self.file['created_dt'][index]
        self.dict['update_virsion_dt'] = (self.file['update_virsion_dt'].fillna('NULL'))[index]
        # print()
        # self.file1.write(','.join(list(self.dict.values())) + '\n')

if __name__ == '__main__':
    Parser()