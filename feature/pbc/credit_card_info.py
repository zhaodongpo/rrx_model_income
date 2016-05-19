# -*- coding: utf-8 -*-
'''
提取用户信用卡特征:
币种:currency
授信额度均值:mean
授信额度中位值:median
授信额度最大值:max
授信额度最小值:min

'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from utils import mongo_connect
import pandas as pd
import numpy as np

SPACE='    '
def get_credit_card_info_feature(credit_card_detail):

    feature={
        'AmountMean':-99,
        'AmountMedian':-99,
        'AmountMax':-99,
        'AmountMin':-99
        }

    amount_list = []
    if credit_card_detail:
        for k,v in credit_card_detail.items():
            card_detail = v
            if card_detail['CURRENCY'] == '人民币' and  card_detail['STATUS']=='1':
                amount_list.append(int(card_detail['AMOUNT']))

        myarray = np.array(amount_list)
        if len(amount_list):
            feature['AmountMean'] = np.mean(myarray)
            feature['AmountMedian'] = np.median(myarray)
            feature['AmountMax'] = np.max(myarray)
            feature['AmountMin'] = np.min(myarray)
    #print feature

    return feature


if __name__ == '__main__':

    db=mongo_connect.get_mongo_db('rrx_xwdb', '10.10.159.15', 27017, 'rrx_xw', 'rrx_xw_pass')
    collection = db['xw_users']

    applycode_list=['M20160411054092','M20160321045256']

    #apply_file = open('/Users/liben/PycharmProjects/Model_Analysis/My_Data_Analysis/datas/','r')

    pbc_info = {}

    for user in collection.find({'_id':{'$in':applycode_list}}):

        if 'PBC' in user:
            pbc_info=user['PBC']
            credit_card_detail_info = {}
            if 'AP_PBC_CREDIT_CARD_DETAIL' in pbc_info:
                credit_card_detail_info=pbc_info['AP_PBC_CREDIT_CARD_DETAIL']
                feature = get_credit_card_info_feature(credit_card_detail_info)

        print user['_id'],feature
        #break