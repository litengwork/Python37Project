# encoding: utf-8
'''
@Author: liteng
@Contact: vnddllit@cn.ibm.com
@File: Log
@Time: 2018/12/28 14:12
'''

import logging.config
import configparser

class log:
    # create logger
    logger = logging.getLogger("VISUAL-RECOGNITION")
    logger.setLevel(logging.DEBUG)

    # CONFIG
    conf = configparser.ConfigParser()
    conf.read('Common/Config.ini')
    logsrc = conf.get('LOG','LOGSRC')

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