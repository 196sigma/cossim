#!/usr/bin/env python
import pickle
import os

INPUT_DIR = "/home/reggie/Dropbox/Research/Accounting Risk/data"

## remove small files
filenames_list = os.listdir(INPUT_DIR+'/SAPTextBlock')
s=0
for f in filenames_list:
    if os.path.getsize(INPUT_DIR+'/SAPTextBlock/'+f) < 1262.55:
        filenames_list.remove(f)
        s+=1

## compile parsed_db
parsed_db_1 = pickle.load(open(INPUT_DIR + "/parsed_db_17_114",'rb'))
parsed_db_2 = pickle.load(open(INPUT_DIR + "/parsed_db_17_116",'rb'))
parsed_db_3 = pickle.load(open(INPUT_DIR + "/parsed_db_16_200",'rb'))

def merge_dicts(*d):
    result = {}
    for dictionary in d:
        result.update(dictionary)
    return result

parsed_db = merge_dicts(parsed_db_1, parsed_db_2, parsed_db_3)
pickle.dump(parsed_db, open(INPUT_DIR + '/parsed_db','wb'))
parsed_db = pickle.load(open(INPUT_DIR + '/parsed_db', 'rb'))
