# encoding: utf-8
import pandas as pd
from lxml import etree
import configparser


# CONFIG
# conf = configparser.ConfigParser()
# conf.read('Config.ini')
#
# header = conf.get('OUTPUTCSV', 't_ryudai1_anonymization_activity_header')
# header = str(header).replace('\n','')
#
#
# dict = {}
#
# for item in header.split(','):
#     dict['%s'%(item)] = ''
#
# print(header)



# file = pd.read_csv('/Users/liteng/litenggithub/Python37Project/PythonPro/xmltocsv/Resource/Xml/t_ryudai3_anonymization_urination.txt', sep=';', dtype='str', encoding='utf-8')

file = pd.read_excel('/Users/liteng/litenggithub/Python37Project/PythonPro/xmltocsv/Resource/Master/Master.xlsx',header=1, nrows=17, usecols=3)
print(file)
# firstline = str(file['result_medical_xml'][0]).replace('=1.0\"','=\"1.0\"')
# print(firstline)
#
# # text = '<?xml version="1.0"?><ehr xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><meditems><meditem name="基準日" code="F000" branch="20">20180829</meditem><meditem name="歩数" code="F000" branch="16">1265</meditem><meditem name="中強度運動" code="F000" branch="17">0.1</meditem><meditem name="総消費カロリー" code="F000" branch="18">0</meditem><meditem name="活動カロリー" code="F000" branch="19">NULL</meditem></meditems></ehr>'
#
# # text = '<?xml version="1.0"?><ehr xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"></meditems></ehr>'
# # html=etree.XML(text) #初始化生成一个XPath解析对象
# # result=etree.tostring(html,encoding='utf-8')   #解析对象输出代码
# # print(type(html))
# # print(type(result))
# # print(result.decode('utf-8'))
# list = []
# # str= 'asd'
# # list.append(str)
# # list.insert('hello',6)
# dic = {'ni':3,
#        'dsa':'dsa',
#        'hi':'hello',
#        'null':''}
# dic['ni']=7
#
#
# for item in dic.values():
#     print(item)
#     list.append(item)
#
# print(dic.values())
#
# header = 'encrypt_id_base64,anonymization_id,entry_date,medical_examinee_birthday,medical_examinee_age,medical_examinee_gender,E00001,E00002,E00003,E00004,E00005,measuring_dt,measuring_dt,controlled_flg,target_group_flg,delete_flg,update_virsion,created_dt,update_virsion_dt'
#
# for elem in range(4):
#     # print(elem)
#     print(html.xpath('//meditems/meditem'))
#
# pd.DataFrame()













def parserXml():
    file = pd.read_csv('/Users/liteng/litenggithub/Python37Project/PythonPro/xmltocsv/Resource/Xml/t_ryudai3_anonymization_urination.txt',sep=';', dtype='str', encoding='utf-8')
    firstline = str(file['result_medical_xml'][0]).replace('=1.0\"', '=\"1.0\"')
    print(firstline)
    html = etree.XML(firstline)













