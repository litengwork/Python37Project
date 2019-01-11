# encoding: utf-8
'''
@Author: liteng
@Contact: vnddllit@cn.ibm.com
@File: Common
@Time: 2018/11/15 15:24
'''

import configparser
import enum
import os
import shutil
import time
import pandas as pd
import xmltocsv.Log as Log


class FolderType(enum.Enum):
    Success = 0
    Fail = 1
    Skip = 2
    Temp = 3

class Common:
    # LOG
    share = Log.log()
    LOG = share.getLogger()

    def getConfValue(self,section,key):
        # CONFIG
        conf = configparser.ConfigParser()
        conf.read('Config.ini')
        value = conf.get(section,key)
        return value

    def log(self):
        # LOG
        share = Log.Share()
        LOG = share.getLogger()
        return LOG

    def removeAllFile(self):
        path = self.getConfValue('RESOURCE','template_folder_src')
        for i in os.listdir(path):
            path_file = os.path.join(path, i)
            if os.path.isfile(path_file):
                os.remove(path_file)

    def moveFile(self, filename, type):
        fromSrc = self.getConfValue('RESOURCE','filelist_folder_src') + filename
        toSrc = ''

        if not os.path.isfile(fromSrc):
            self.LOG.error("----------FILENAME: %s---------%s NOT EXIST!------------" % (filename, fromSrc))
            print("----------FILENAME: %s---------%s NOT EXIST!------------" % (filename, fromSrc))

        else:
            if type == FolderType.Success:
                toSrc = self.getConfValue('RESOURCE','success_folder_src') + filename
            if type == FolderType.Fail:
                toSrc = self.getConfValue('RESOURCE', 'fail_folder_src') + filename
            if type == FolderType.Skip:
                toSrc = self.getConfValue('RESOURCE', 'skip_folder_src') + filename

        try:
            fpath, fname = os.path.split(toSrc)
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            shutil.move(fromSrc, toSrc)
            shutil.copy(toSrc, fpath + '/' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + filename)
            self.LOG.info("------FILENAME: %s------MOVE DONE %s --- %s -> %s--------" % (filename, type, fromSrc, toSrc))
            print("------FILENAME: %s------MOVE DONE %s %s -> %s--------" % (filename, type, fromSrc, toSrc))
        except Exception as ex:
            self.LOG.error(
                "------FILENAME: %s------MOVE ERROR %s--------" % (filename, ex))


    def copyFile(self, filename):
        fromSrc = self.getConfValue('RESOURCE', 'filelist_folder_src') + filename
        toSrc = self.getConfValue('RESOURCE', 'template_folder_src') + filename

        if not os.path.isfile(fromSrc):
            self.LOG.error("----------FILENAME: %s---------%s NOT EXIST!------------" % (filename, fromSrc))
            print("----------FILENAME: %s---------%s NOT EXIST!------------" % (filename, fromSrc))
        else:
            try:
                fpath, fname = os.path.split(toSrc)
                if not os.path.exists(fpath):
                    os.makedirs(fpath)
                shutil.copy(fromSrc, toSrc)
                self.LOG.info(
                "------FILENAME: %s------COPY DONE %s -> %s--------" % (filename, fromSrc, toSrc))
                print("------FILENAME: %s------COPY DONE %s -> %s--------" % (filename, fromSrc, toSrc))
            except Exception as ex:
                self.LOG.error(
                    "------FILENAME: %s------COPY ERROR %s--------" % (filename, ex))

    # IS HAS DATA
    def isHasData(self,filename) -> bool:
        # CSV DATA
        try:
            filesrc = self.getConfValue('RESOURCE', 'filelist_folder_src') + filename
            data = pd.read_csv(filesrc, sep=';', dtype='str', encoding='utf-8')
            if data.empty:
                # MOVE SKIP FLODER
                self.moveFile(filename, FolderType.Skip)
                return False
            else:
                self.LOG.info('----------------- Data Not Empty -------------------')
                return True
        except Exception as ex:
            self.LOG.error('----------------- %s -------------------' % (ex))
            return False




