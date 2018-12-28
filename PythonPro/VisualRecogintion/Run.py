# encoding: utf-8
'''
@Author: liteng
@Contact: vnddllit@cn.ibm.com
@File: Run
@Time: 2018/12/28 14:29
'''
import configparser
import glob
from VisualRecogintion.Common import Log
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
    # visual_recognition = VisualRecognitionV3()
    threshold = ''
    classifier_ids = ''

    def __init__(self):
        self.csvSrc = self.conf.get('CSV', 'CSVSRC')
        self.csvHeader = self.conf.get('CSV', 'CSVHEADER')
        self.imgSrc = self.conf.get('IMG', 'IMGSRC')
        self.imgTypes = str(self.conf.get('IMG', 'IMGTYPE')).split(',')
        self.threshold = self.conf.get('VISUAL', 'THRESHOLD')
        self.classifier_ids = self.conf.get('VISUAL', 'CLASSIFIER_IDS')
        self.file = open(self.csvSrc, 'w+')
        # self.visual_recognition = VisualRecognitionV3(
        #     version= conf.get('VISUAL', 'VERSION'),
        #     iam_apikey= conf.get('VISUAL', 'APIKEY')
        # )
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
                # classes = self.visual_recognition.classify(
                #     images_file,
                #     threshold= self.threshold,
                #     classifier_ids= self.classifier_ids).get_result()
                classes = ''
                self.writeToCsv(classes,imgName,className,False)
                # ???????????????
                print(className + '  :  ' + imgName)
                self.log.info('--- WRITE CSV SUCCESS ---CLASSNAME : %s---IMGNAME : %s-----'%(className,imgName))
            except Exception as ex:
                # ???????????????
                print(className + '  :  ' + imgName +'----CRASH---' + ex)
                self.log.error('--- WRITE CSV FAIL ---CLASSNAME : %s---IMGNAME : %s---%s--'%(className,imgName,ex))

    # WRITETOCSV
    def writeToCsv(self,res,imgName,className,isWriteHeader):
        try:

            if isWriteHeader:
                # WRITE HEADER
                self.file.write(self.csvHeader + '\n')
                self.log.info('--- WRITE CSV HEADER SUCCESS---')
            else:
                self.file.write(className + ',' + imgName + '\n')
                # res['images'][0]['classifiers'][0]['classes'].sort(key=lambda k: (k.get('class', 0)), reverse=False)
                # tmp = []
                # for score in res['images'][0]['classifiers'][0]['classes']:
                #     score = score['score']
                #     tmp.append(score)
                # file.write(imgName + ',' + ','.join(str(e) for e in tmp) + '\n')
        except Exception as ex:
            self.log.error('--- WRITE CSV FAIL ---CLASSNAME : %s---IMGNAME : %s---%s--' % (className, imgName, ex))

# MAIN
def main():
    VisualRecogintion().run()

if __name__ == '__main__':
    main()