import pandas as pd
import pickle

working_dir = '/afs/cern.ch/user/a/apoyet/public/pyHTC/the_simplest_example/'

# read the pickle

df = pd.read_pickle(working_dir+'input/input.pkl')

# function to apply

def times2(df):
    df['result'] = df['number']*2
    return df

# apply the function 

df = times2(df)

# save the output

df.to_pickle(working_dir+'output/output.pkl')