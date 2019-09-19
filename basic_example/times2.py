
import pandas as pd
import sys
import os

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
myIndex=int(sys.argv[1])

# read the pickle
working_dir = '/afs/cern.ch/user/s/sterbini/pyHTC/'
df = pd.read_pickle(working_dir+'studyDF.pkl')

myRow=df.iloc[myIndex].copy()

print(os.environ["PATH"])
#print(os.environ["process"])

# ================================================

# Now the unmask variable will be done using the df
# function to apply
def times2(myRow):
    myRow['result'] = myRow['number']*2
    return myRow

# apply the function 
myRow = times2(myRow)

# save the output
df.to_pickle(working_dir+f'output/output_{myIndex}.pkl')