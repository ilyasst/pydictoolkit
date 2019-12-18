# -*- coding: utf-8 -*-
#@author: ilyass.tabiai@polymtl.ca
import csv, os
import glob
import pandas as pd

class DIC_reader():

    def __init__(self, relpath):
        #cwd = os.getcwd()
        os.chdir(relpath)
        
        dic_paths = glob.glob('*.{}'.format("csv"))
        dic_paths.sort()
        self.dic_paths = dic_paths

        self.preprocess_csv()
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

    def preprocess_csv(self):
        new_dic_paths = []
        for csv_name in self.dic_paths:
            new_csv = []
            if "_clean.csv" in csv_name:
                pass
            else:
                with open( csv_name ) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line = 0
                    for row in csv_reader:
                        new_row = []
                        if line == 0:
                            for header in row:
                                new_row.append( header.strip('"').strip(" ").strip('"') )
                            new_csv.append( new_row )
                            line += 1
                        else:
                            new_csv.append( row )
                            line += 1

                new_path = csv_name[:-4]+"_clean.csv"
                new_dic_paths.append( new_path )
                with open( new_path, "w" ) as new_csv_file:
                    wr = csv.writer(new_csv_file)
                    wr.writerows(new_csv)
        self.dic_paths = new_dic_paths
