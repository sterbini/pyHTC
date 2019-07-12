import re
import numpy as np
import os

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
    return np.unique(myList);

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
