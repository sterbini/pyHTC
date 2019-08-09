import re
import numpy as np
import pandas as pd
import os
import itertools

def prepare_work_dir(input_dir = 'input', output_dir = 'output', log_dir = 'log', error_dir = 'error'):
    '''
    This simple creates the different folder necessary to the submission to HTCondor. 
    Default values are given so the user can simply proceed with the submission process.
    Those defaut values are consistent with the rest of the pyHTC package. 
    '''
    if input_dir and os.path.exists(input_dir)==False:
        os.mkdir(input_dir)
    if output_dir and os.path.exists(output_dir)==False:
        os.mkdir(output_dir)
    if log_dir and os.path.exists(log_dir)==False:
        os.mkdir(log_dir)
    if error_dir and os.path.exists(error_dir)==False:
        os.mkdir(error_dir)

def getMaskedParameterList(myFile, tag='MASKED_', printLine=False):
    '''
    It returns the words strarting with tag='MASKED_' in myFile.
    If printLine then the full line contained a masked parameters is printed.
    '''
    searchfile = open(myFile, "r")
    myList=[]
    for line in searchfile:
        aux=re.findall('\\'+ tag + '\w+', line)
        for i in (aux):
            if printLine: print(line)
            myList.append(i)
    searchfile.close()
    return np.unique(myList)

def unmask(myFile, myMaskedParam, myParams, myOutMask_path):
    searchFile = open(myFile, 'r')
    myUnmaskedFile = ''
    for line in searchFile:
        for param in myMaskedParam:
            line = line.replace(param, str(myParams[param]))
        myUnmaskedFile = myUnmaskedFile+line
    text_file = open(myOutMask_path,"w")
    text_file.write(myUnmaskedFile)
    text_file.close()

def cross_studies(newDF, oldDF):
    x = pd.concat([oldDF,newDF])
    y = x.drop_duplicates(keep=False, inplace=False)
    myFilteredDF = newDF.filter(items=y.index, axis=0)
    myElimDF = newDF.loc[~newDF.index.isin(y.index)]
    myElimDF = myElimDF.assign(Old_Index = list(oldDF.index))
    return myFilteredDF, myElimDF

def combine_dict(name, myDict):
    myList = []
    myIndex = []
    for i in itertools.product(*myDict.values()):
        myList.append(i)
        myIndex.append((name+'_{}'*len(i)).format(*i))
    return pd.DataFrame(myList, columns=myDict.keys(), index=myIndex)