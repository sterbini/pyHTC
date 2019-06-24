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
        self.input_dir = input_dir
        self.arguments = arguments
        self.output_dir = output_dir
        self.error_dir = error_dir
        self.log_dir = log_dir
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
        self.parameters = kwargs
        for a in itertools.product(*self.parameters_values):
            myList.append((self.name+'_{}'*len(a)).format(*a))
        self.jobs_names = myList
        
    def get_studyDF(self):
        '''
        This method creates a pandas Dataframe containg the information of each job to be submitted
        '''
        # first to get the values of the parameters
        myArray = np.zeros([np.prod([len(e) for e in self.parameters_values]), len(self.parameters_keys)])
        flag = 0
        for a in itertools.product(*self.parameters_values):
            myArray[flag] = a
            flag+=1
            
        # df definition
        myColumns = [param for param in self.parameters_keys] + ['Input', 'Output', 'Error', 'Log']
        myDF = pd.DataFrame(index = self.jobs_names, columns=myColumns)
        
        # store the parameters values
        myDF[[param for param in self.parameters_keys]] = myArray
        
        # files paths
        myDF['Input'] = self.input_dir + myDF.index + '.in'
        myDF['Output'] = self.output_dir + self.name + '.$(ClusterId).$(ProcId).out'
        myDF['Error'] = self.error_dir + self.name + '.$(ClusterId).$(ProcId).err'
        myDF['Log'] = self.log_dir + self.name + '.$(ClusterId).$(ProcId).log'
        
        return myDF
    
    def submit2str(self):
        '''
        This methods creates the string that will be writen in a file afterwards. 
        '''
        
        myString = '''executable = {}\n'''.format(self.executable)
        if self.input_dir:
            myString += '''input = $(input_file)\n'''
        if self.arguments:
            myString += '''arguments = {}\n'''.format(self.arguments)
        if self.output_dir:
            myString += '''output = {}.$(ClusterId).$(ProcId).out\n'''.format(self.output_dir+self.name)
        if self.error_dir:
            myString += '''error = {}.$(ClusterId).$(ProcId).err\n'''.format(self.error_dir+self.name)
        if self.log_dir:
            myString += '''log = {}.$(ClusterId).log\n'''.format(self.log_dir+self.name)
        if self.universe:
            myString += '''universe = {}\n'''.format(self.universe)
        if self.job_flavour:
            myString += '''+JobFlavour = "{}"\n'''.format(self.job_flavour)
            
        myString += '''queue input_file matching files input/{}_*.in'''.format(self.name)
        return myString
    
    
    def submit2file(self, string):
        submit_file = open(self.submit_file, "w")
        submit_file.write(string)
        submit_file.close()
        
    def display_subfile(self):
        f = open(self.submit_file, 'r')
        text = f.read()
        print(text)
        
    def submit2HTCondor(self):
        print(subprocess.check_output(["condor_submit", self.submit_file]))
        
    def condor_q(self, nobatch=False, jobID=None):
        if nobatch: 
            print(subprocess.check_output(["condor_q","-nobatch"]))
        elif jobID: 
            print(subprocess.check_output(["condor_q", jobID]))
        else: 
            print(subprocess.check_output(["condor_q"]))

        