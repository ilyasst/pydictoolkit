# -*- coding: utf-8 -*-
#@author: ilyass.tabiai@polymtl.ca
import csv, os
import glob
import pandas as pd

class DIC_reader():

    def __init__(self, relpath):

        cwd = os.getcwd()
        os.chdir(relpath)

        dic_paths = glob.glob('*.{}'.format("csv"))
        dic_paths.sort()
        
        #os.chdir(cwd)
        self.dic_paths = dic_paths

        self.load_data()
    
    def load_data(self):
        dataframe = []
        for csv_name in self.dic_paths:
            pd_data = pd.read_csv(csv_name)
            pd_data.columns = pd_data.columns.str.strip()
            print("File ", csv_name)
            print("Your keys are: ", pd_data.columns.str.strip())
            dataframe.append( pd_data )

        self.dataframe = dataframe