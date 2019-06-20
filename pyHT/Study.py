import subprocess
import numpy as np
import pandas as pd
import itertools

class Study():
    '''
    This class is used to define a study to be submitted to HTCondor. This particularly useful in the case of multiple jobs submissions. 
    A study will be defined by an executable, a submission file and a set of parameters, corresponding to a single job. Each job is instantiated for the Job class.
    '''

    def __init__(self, name, executable, submit_file, input_file = "", arguments = "$(ClusterId) $(ProcId)", 
                 output = "", error = "", log = "", job_flavour = "", universe = "vanilla",
                 queue = ""):
        self.name = name
        self.executable = executable
        self.submit_file = submit_file
        self.input_file = input_file
        self.arguments = arguments
        self.output = output
        self.error = error
        self.log = log
        self.job_flavour = job_flavour
        self.universe = universe
        self.queue = queue

    
    def define_study(self, *args):
        '''
        This method will define the list of jobs of the study. It therefore takes as arguments the parameters to vary in the study amongs the different jobs. 
        'paramaters' is a multi-dimensionnal array containing the values of the different paramaters. 

        **** EXAMPLE ****
        The study is called 'myScan'. And it will scan two parameters Temp and Press from 0 to 10 for Temp and 50 to 60 for Press.

        define_study(np.array([[0, 2, 4, 6, 8, 10], [50, 55, 60]]))
        >>> ['myScan_0_50', 'myScan_0_55', ...]
        '''
        myList = []
        for a in itertools.product(*args):
            myList.append((self.name+'_{}'*len(a)).format(*a))
        return myList

        