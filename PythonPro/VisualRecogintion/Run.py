# encoding: utf-8
'''
@Author: liteng
@Contact: vnddllit@cn.ibm.com
@File: Run
@Time: 2018/12/28 14:29
'''
import configparser
import glob
import json

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
    # visual_recognition = None
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
        # self.visual_recognition = VisualRecognitionV3(
        #     version= self.conf.get('VISUAL', 'VERSION'),
        #     iam_apikey= self.conf.get('VISUAL', 'APIKEY')
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
                classes = {'images': [{'classifiers': [{'classifier_id': 'DefaultCustomModel_551605964', 'name': 'Default Custom Model', 'classes': [{'class': 'M00014', 'score': 0.981}, {'class': 'M00019', 'score': 0}, {'class': 'M00026', 'score': 0.003}, {'class': 'M00033', 'score': 0.003}, {'class': 'M00036', 'score': 0.001}, {'class': 'M00059', 'score': 0}, {'class': 'M00066', 'score': 0.004}, {'class': 'M00073', 'score': 0.003}, {'class': 'M00074', 'score': 0.002}, {'class': 'M00080', 'score': 0.056}, {'class': 'M00087', 'score': 0.002}, {'class': 'M00092', 'score': 0}, {'class': 'M00097', 'score': 0.001}, {'class': 'M00101', 'score': 0.001}, {'class': 'M00108', 'score': 0.064}, {'class': 'M00115', 'score': 0.002}, {'class': 'M00132', 'score': 0}, {'class': 'M00155', 'score': 0.021}, {'class': 'M00165', 'score': 0.016}, {'class': 'M00171', 'score': 0.001}, {'class': 'M00173', 'score': 0.001}, {'class': 'M00180', 'score': 0.002}, {'class': 'M00185', 'score': 0}, {'class': 'M00192', 'score': 0}, {'class': 'M00194', 'score': 0.004}, {'class': 'M00202', 'score': 0.004}, {'class': 'M00403', 'score': 0}, {'class': 'M00414', 'score': 0}, {'class': 'M00416', 'score': 0.019}, {'class': 'M00433', 'score': 0.003}, {'class': 'M00809', 'score': 0}, {'class': 'M00814', 'score': 0}, {'class': 'friedShrimp', 'score': 0.005}, {'class': 'misoSoup', 'score': 0.002}, {'class': 'rice', 'score': 0.008}, {'class': 'sengiriKyabetsu', 'score': 0.001}, {'class': 'shogaYaki', 'score': 0.007}, {'class': 'takuan', 'score': 0.002}]}], 'image': 'M00014_T_2.jpg'}], 'images_processed': 1, 'custom_classes': 38}
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
                # self.file.write(className + ',' + imgName + '\n')
                res['images'][0]['classifiers'][0]['classes'].sort(key=lambda k: (k.get('score', 0)), reverse=True)
                tmp = {}
                tmp1 = []
                for score in res['images'][0]['classifiers'][0]['classes']:
                    # score = score['class']+ ','+ score['score']
                    # print(score)
                    tmp = {score['class']:score['score']}
                    tmp.s
                    tmp1.append(tmp)
                self.file.write(className + ',' + imgName + ',' + ','.join(str(e.ke) for e in tmp1[:10]) + '\n')
        except Exception as ex:
            self.log.error('--- WRITE CSV FAIL ---CLASSNAME : %s---IMGNAME : %s---%s--' % (className, imgName, ex))

# MAIN
def main():
    VisualRecogintion().run()

if __name__ == '__main__':
    main()