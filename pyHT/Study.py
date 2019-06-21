import subprocess
import numpy as np
import pandas as pd
import itertools
from Job import JobObj

class StudyObj():
    '''
    This class is used to define a study to be submitted to HTCondor. This particularly useful in the case of multiple jobs submissions. 
    A study will be defined by an executable, a submission file and a set of parameters, corresponding to a single job. Each job is instantiated from the Job class.
    '''

    def __init__(self, name, executable, submit_file, input_dir = "", arguments = "$(ClusterId) $(ProcId)", 
                 output_dir = "", error_dir = "", log_dir = "", job_flavour = "", universe = "vanilla",
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

    
    def define_study(self, **kwargs):
        '''
        This method will define the list of jobs of the study. It therefore takes as arguments the parameters to vary in the study amongs the different jobs. 
        'paramaters' is a multi-dimensionnal array containing the values of the different paramaters. 

        **** EXAMPLE ****
        The study is called 'myScan'. And it will scan two parameters Temp and Press from 0 to 10 for Temp and 50 to 60 for Press.

        define_study(np.array([[0, 2, 4, 6, 8, 10], [50, 55, 60]]))
        >>> ['myScan_0_50', 'myScan_0_55', ...]
        '''
        myList = []
        self.parameters_keys = kwargs.keys()
        self.parameters_values = kwargs.values()
        for a in itertools.product(*self.parameters_values):
            myList.append((self.name+'_{}'*len(a)).format(*a))
        self.jobs_names = myList
        
    def get_studyDF(self):
        '''
        This method creates a pandas Dataframe containg the information of each job to be submitted
        '''
        myColumns = [param for param in myStudy.parameters_keys] + ['Input', 'Output', 'Error', 'Log']
        myDF = pd.DataFrame(index = self.jobs_names, columns=myColumns)
        myDF['Input'] = myDF.index + '.in'
        myDF['Output'] = self.name + '.$(ClusterId).$(ProcId).out'
        myDF['Error'] = self.name + '.$(ClusterId).$(ProcId).err'
        myDF['Log'] = self.name + '.$(ClusterId).$(ProcId).log'
        
        return myDF


        