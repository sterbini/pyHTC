#############################
#         HEADER            #
#############################
import sys
import pandas as pd

df = pd.read_pickle(sys.argv[1])
myIndex=int(sys.argv[2])
myRow=df.iloc[myIndex].copy()

#############################
#           BODY            #
#############################

# apply the function 
myRow['result'] = myRow['number']*2
# save the output
myRow.to_pickle(myRow['outFile'])