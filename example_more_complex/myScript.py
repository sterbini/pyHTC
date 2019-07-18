from cpymad.madx import Madx
madx = Madx()
import pandas as pd

# DF
myDF = pd.DataFrame(index = ['kf', 'kd'], columns=['before', 'after'])

# This is a very simple example : we will simply create a FODO cell and try to match it to a given tune 

myFODO = '''
/******* Definition of the elements *******/
qfType:QUADRUPOLE, L=1.5, K1:=kf;
qdType:QUADRUPOLE, L=1.5, K1:=kd;

/******* Definition of the sequence *******/
fodo:SEQUENCE, REFER=exit, L=10;
qf: qfType, at=5;
qd: qdType, at=10;
ENDSEQUENCE;

/******* Definition of the strengths *******/
kf=+0.2985;
kd=-0.2985;

/******* Definition of the beam *******/
beam, particle=proton, energy=7001;
'''

madx.input(myFODO);

myDF['before'].loc['kf'] = madx.eval('kf')
myDF['before'].loc['kd'] = madx.eval('kd')

myMatching = '''

/******* Activation of the sequence *******/
use, sequence=fodo;

/******* Operations *******/
twiss;

/******* Matching *******/
MATCH, sequence=fodo;
    GLOBAL, Q1=%MASKED_Q1;
    GLOBAL, Q2=%MASKED_Q2;
    VARY, NAME=kf, STEP=0.0001;
    VARY, NAME=kd, STEP=0.0001;
    LMDIF, CALLS=50, TOLERANCE=1E-8;
ENDMATCH;
'''
madx.input(myMatching);

myDF['after'].loc['kf'] = madx.eval('kf')
myDF['after'].loc['kd'] = madx.eval('kd')

myDF.to_pickle('%MASKED_output_file')
