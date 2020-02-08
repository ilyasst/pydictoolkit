# -*- coding: utf-8 -*-
#@author: ilyass.tabiai@polymtl.ca
# Heavily inspired from
# https://raw.githubusercontent.com/lm2-poly/PeriPyDIC/master/peripydic/IO/deck.py
import yaml, sys
import os.path

class Deck():

    def __init__(self, inputhpath):
        if not os.path.exists(inputhpath):
            print("File " + inputhpath)
            sys.exit(1)
        else:
            with open(inputhpath,'r') as f:
                ## Container of the tags parsed from the yaml file
                self.doc = yaml.load(f, Loader=yaml.BaseLoader)

                if not "Data" in self.doc:
                    print ("YamlTagError: Data tag is a mandatory tag")
                    sys.exit(1)
                else:
                    if not "Folder" in self.doc["Data"]:
                        print ("YamlTagError: Folder within Data tag is a mandatory tag")
                        sys.exit(1)
                        
                if not "Plots" in self.doc:
                    print ("YamlTagError: Plots tag is a mandatory tag")
                    sys.exit(1)                    
                else:
                    if not "Target Plot" in self.doc["Plots"]:
                        print ("YamlTagError: Target Plot within Plots tag is a mandatory tag")
                        sys.exit(1)
                    if not "Groups" in self.doc["Plots"]:
                        print ("YamlTagError: Groups within Plots tag is a mandatory tag")
                        sys.exit(1)
                    else:
                        if not "Region" in self.doc["Plots"]["Groups"]:
                            print ("YamlTagError: Region within Plots-Groups tag is a mandatory tag")
                            sys.exit(1)   
                    if not "Target Column" in self.doc["Plots"]:
                        print ("YamlTagError: Target Column within Plots tag is a mandatory tag")
                        sys.exit(1)  
                                      
        self.dic_path = self.doc["Data"]["Folder"]
        self.sample_size = self.doc["Plots"]["Groups"]["Region"]
        self.target = self.doc["Plots"]["Target Column"]
                