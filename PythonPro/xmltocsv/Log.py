# encoding: utf-8
'''
@Author: liteng
@Contact: vnddllit@cn.ibm.com
@File: Log
@Time: 2018/11/15 15:26
'''

import logging.config
import configparser

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