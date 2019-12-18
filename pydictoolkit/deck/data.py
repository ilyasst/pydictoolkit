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
                    else:
                        self.dic_path = self.doc["Data"]["Folder"]
                        self.sample_size = self.doc["Region"]
                        self.target = self.doc["Target Column"]
                