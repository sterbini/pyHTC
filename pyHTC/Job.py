import numpy as np
import pandas as pd
import subprocess

class JobObj():
    '''
    This is a class to define a single job.
    '''
    
    def __init__(self, executable, submitFile_name, input_file = "", arguments = "$(ClusterId) $(ProcId)", 
                 output = "", error = "", log = "", job_flavour = "", universe = "vanilla",
                 queue = ""):
        self.executable = executable
        self.submitFile_name = submitFile_name
        self.input_file = input_file
        self.arguments = arguments
        self.output = output
        self.error = error
        self.log = log
        self.job_flavour = job_flavour
        self.universe = universe
        self.queue = queue
        
    def submit2str(self):
        myString = '''executable = {}\n'''.format(self.executable)
        if self.input_file:
            myString += '''input = {}\n'''.format(self.input_file)
        if self.arguments:
            myString += '''arguments = {}\n'''.format(self.arguments)
        if self.output:
            myString += '''output = {}.$(ClusterId).$(ProcId).out\n'''.format(self.output)
        if self.error:
            myString += '''error = {}.$(ClusterId).$(ProcId).err\n'''.format(self.error)
        if self.log:
            myString += '''log = {}.$(ClusterId).log\n'''.format(self.log)
        if self.universe:
            myString += '''universe = {}\n'''.format(self.universe)
        if self.job_flavour:
            myString += '''+JobFlavour = "{}"\n'''.format(self.job_flavour)
            
        myString += '''queue {}'''.format(self.queue)
    
        return myString
    
    def submit2file(self, string):
        submit_file = open(self.submitFile_name, "w")
        submit_file.write(string)
        submit_file.close()
    
    def add_line(self, command, input_file):
        f = open(input_file, 'r+b')
        content = f.readlines()
        f.close()
        content.insert(len(content)-1, command+'\n')
        f = open(input_file, 'w')
        f.writelines(content)
        f.close()
        
    def display_subfile(self):
        f = open(self.submitFile_name, 'r')
        text = f.read()
        print(text)
        
    def submit2HTCondor(self):
        print(subprocess.check_output(["condor_submit", self.submitFile_name]))
        
    def condor_q(self, nobatch=False, jobID=None):
        if nobatch: 
            print(subprocess.check_output(["condor_q","-nobatch"]))
        elif jobID: 
            print(subprocess.check_output(["condor_q", jobID]))
        else: 
            print(subprocess.check_output(["condor_q"]))
