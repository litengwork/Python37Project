# encoding: utf-8

import configparser
import glob
import json

from Visual.Common import Log
from watson_developer_cloud import VisualRecognitionV3

class VisualRecogintion:
    # BASE
    csvSrc = ''
    csvHeader = ''
    imgSrc = ''
    imgTypes = []
    file = ''
    # CONFIG
    conf = configparser.ConfigParser()
    conf.read('Common/Config.ini')
    # LOG
    share = Log.log()
    log = share.getLogger()
    #VISUAL
    visual_recognition = None
    threshold = ''
    classifier_ids = ''

    def __init__(self):
        self.csvSrc = self.conf.get('CSV', 'CSVSRC')
        self.csvHeader = self.conf.get('CSV', 'CSVHEADER')
        self.imgSrc = self.conf.get('IMG', 'IMGSRC')
        self.imgTypes = str(self.conf.get('IMG', 'IMGTYPE')).split(',')
        self.threshold = self.conf.get('VISUAL', 'THRESHOLD')
        self.classifier_ids = self.conf.get('VISUAL', 'CLASSIFIER_IDS')
        self.file = open(self.csvSrc, 'w+',encoding='utf-8')
        self.visual_recognition = VisualRecognitionV3(
            version= '2019-01-08',
            iam_apikey= 'OGhXl7PKa2_PKKlsZJatmsyz_zfCn5d6z_4yTrOjaHU0'
        )
        self.writeToCsv('','','',True)

    # RUN
    def run(self):
        self.getImgFile()

    # GETIMGFILE
    def getImgFile(self):
        for imgtype in self.imgTypes:
            list = glob.glob(self.imgSrc%(imgtype))
            for imgfile in list:
                imgname = imgfile.split('/')[len(imgfile.split('/'))-1]
                classname = imgfile.split('/')[len(imgfile.split('/'))-2]
                self.getVisualResult(imgfile,imgname,classname)

    # GETVISUALRESULT
    def getVisualResult(self,imgFile,imgName,className):
        with open(imgFile, 'rb') as images_file:
            try:
                classes = self.visual_recognition.classify(
                    images_file,
                    threshold= self.threshold,
                    classifier_ids= 'DefaultCustomModel_903850813').get_result()
                self.writeToCsv(classes,imgName,className,False)
                self.log.info('--- WRITE CSV SUCCESS ---CLASSNAME : %s---IMGNAME : %s-----'%(className,imgName))
            except Exception as ex:
                self.log.error('--- WRITE CSV FAIL ---CLASSNAME : %s---IMGNAME : %s---%s--'%(className,imgName,ex))

    # WRITETOCSV
    def writeToCsv(self,res,imgName,className,isWriteHeader):
        try:

            if isWriteHeader:
                # WRITE HEADER
                self.file.write(self.csvHeader + '\n')
                self.log.info('--- WRITE CSV HEADER SUCCESS---')
            else:
                res['images'][0]['classifiers'][0]['classes'].sort(key=lambda k: (k.get('score', 0)), reverse=True)
                tmpStr = ''
                for score in res['images'][0]['classifiers'][0]['classes'][:10]:
                    tmpStr = tmpStr + ',' + score['class'] + ',' + str(score['score'])
                self.file.write(className + ',' + imgName + tmpStr + '\n')
        except Exception as ex:
            self.log.error('--- WRITE CSV FAIL ---CLASSNAME : %s---IMGNAME : %s---%s--' % (className, imgName, ex))

# MAIN
def main():
    VisualRecogintion().run()

if __name__ == '__main__':
    main()