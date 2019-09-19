# pyHTC

pyHTC is a python package to ease the submission of jobs to the HTCondor cluster. It also provides functions to help in the organization of the parameters of each job, storing the data in convinient pandas DataFrames, allowing the user to find out which job corresponds to what study. 

## Installation

To install the package, you might use the command: 
```
pip install --user git+https://github.com/sterbini/pyHTC.git
```

If you want to upgrade it, please issue the following command: 
```
pip install --upgrade --user git+https://github.com/sterbini/pyHTC.git
```


## Contribute 

For any question or suggestion please contact me : axel.poyet@cern.ch, or simply fork the project and feel free to contribute! 

## pyHTC and a simple example (https://codimd.web.cern.ch/s/BJHLg2lDH)

If you have a python script that you want to run for multiple inputs on CERN HTCondor (HTC) batch system, have a look on our suggested approach described in the following. 

We are using Python 3.


Let's start with a simple example containting all the  needed ingredients.
Our trivial case is: use HTC to double N numbers.
You can set up one study containing N jobs.

The first step is to ensure that HTC is using the correct python stack (this can be critical for certain data format).

This can be done by adding to the HTC executable file the source of the correct python version and after that executing the python script you need to run. Here you are an example of myScript.**sh** bash executable.
``` bash 
#!/bin/bash
source  /cvmfs/sft.cern.ch/lcg/views/LCG_95apython3/x86_64-centos7-gcc7-opt/setup.sh
python /afs/cern.ch/user/s/sterbini/pyHTC/basicExample/myScript.py /afs/cern.ch/user/s/sterbini/pyHTC/basicExample/myDF.pkl $1
```

The last line has three arguments: 
1. the name of the script of the study
2. the pandas daframe that stores the data of the study (**each job is a row**)
3. the row number corresponding to the job to execute.

Given that approach, a possible code for the myScript.**py** is

``` python 
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
```

- In the **header part**, we just read the full pandas DF (corresponding to the study) and select the row corresponding to our specific job.
- In the **body part**, we program the interesting part of the script (algorithms and output handling).

It is importatant to observe that in the body part all job's dependent parameter (inputs and outputs) are **masked** by the value of *myRow* (e.g., *myRow['result']*, *myRow['number']* and *myRow['outFile']*).

The pandas DF could be something like
``` python
mypath=os.getcwd()
python_dataframe=mypath+'/myDF.pkl' 
python_distribution='/cvmfs/sft.cern.ch/lcg/views/LCG_95apython3/x86_64-centos7-gcc7-opt/setup.sh'

# A simple DataFrame
col = ['number']
data = np.random.randn(5)
df = pd.DataFrame(data, columns=col)
df['outFile']=[mypath+'/output/output_'+str(i)+'.pkl' for i in df.index]
df.to_pickle(python_dataframe)
```

Note that the *df* has the fields *number* and *outFile* used in the *myScript.**py*** as input.

You can already run locally a job to verify that all is working (clearly you have also to create the outFile folder if does not exist and *chmod +x* the myScript.**sh**).


``` bash
./myScript.sh 0
```

The previous command will launch 
- the setup of the python environment
- the python script taking the first row of the given dataframe.

Said that, you can now appreciate the [pyHTC](https://github.com/apoyet/pyHTC) package by A. Poyet to ease your working flow.

For instance you can use the following ipynb.

``` python
from pyHTC.Study import *
import pyHTC.toolkit as toolkit
import os

mypath=os.getcwd()
python_script=mypath+'/myScript.py' # please ensure that this file exists
python_dataframe=mypath+'/myDF.pkl' # please ensure the this df contatains the variables in myScript.py 
# it should correspond to the setup.sh of the STACK you want to use 
# (should correspond to the one used for running this ipnb (pickles format is STACK dependent))
python_distribution='/cvmfs/sft.cern.ch/lcg/views/LCG_95apython3/x86_64-centos7-gcc7-opt/setup.sh'

# A simple DataFrame
col = ['number']
data = np.random.randn(5)
df = pd.DataFrame(data, columns=col)
df['outFile']=[mypath+'/output/output_'+str(i)+'.pkl' for i in df.index]
df.to_pickle(python_dataframe)

myStudy = StudyObj(name='test',\
                   path=mypath,\
                   python_script=python_script,\
                   python_distribution=python_distribution,\
                   python_dataframe=python_dataframe,
                   arguments='$(ProcId)', queue=len(pd.read_pickle(python_dataframe)))
myStudy.describe()
```

When the myStudy is setup it can
1. setup the folder structure for HTCondor
2. write the myScript.**sh**
3. write the HTCondor submitting file.

For convenince you can run a jupyter session directly on lxplus (see http://bblumi.web.cern.ch/how-tos/#how-to-run-a-jupyter-notebook-from-lxplus) 

```python
# Preparation of the working directory
toolkit.prepare_work_dir()
# Preparation of the submit file
myStudy.submit2file(myStudy.submit2str())
# Preparation of the bash script
myStudy.script2file(myStudy.script2str())
```

Then you can launch the simulation with

```python
# Before submitting you should do a minimal check with
# chmod +x myScript.sh
# myScript.sh 0
myStudy.submit2HTCondor()
```

You can monitor the status of your job in python invoking the bash command
```python
!condor_q
```

And finally you can retrieve the results with 
``` python
# Postprocessing
myDF=pd.read_pickle(python_dataframe)

myList=[]
for i,row in myDF.iterrows():
    try: 
        myList.append(pd.read_pickle(row['outFile']))
    except:
        print(f'==>The {row["outFile"]} was not found')
pd.DataFrame(myList) 
```

For additional reading see http://bblumi.web.cern.ch/how-tos/pyHTC/pyHTC/.
