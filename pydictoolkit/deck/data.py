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
                        self.data_folder = self.doc["Data"]["Folder"]
                        
                if not "Plots" in self.doc:
                    print("YamlTagError: Plots tag is a mandatory tag")
                    sys.exit(1)                    
                else:
                    if not "Target Plot" in self.doc["Plots"]:
                        print("YamlTagError: Target Plot within Plots tag is a mandatory tag")
                        sys.exit(1)
                    else:
                        self.targetplot = self.doc["Plots"]["Target Plot"]

                    if not "Heatmaps" in self.doc["Plots"]:
                        print("YamlTagError: Heatmaps within Plots tag is a mandatory tag")
                        sys.exit(1)
                    else:
                        if not "Plot_it" in self.doc["Plots"]["Heatmaps"]:
                            print("YamlTagError: Plot_it within Plots-Heatmaps tag is a mandatory tag")
                            sys.exit(1)
                        else: 
                            self.plot_heatmaps = self.doc["Plots"]["Heatmaps"]["Plot_it"]
                            if self.plot_heatmaps  == "true":
                                if not "Region" in self.doc["Plots"]["Heatmaps"]:
                                    print("YamlTagError: Region within Plots-Heatmaps tag is a mandatory tag")
                                    sys.exit(1) 
                                else:
                                    self.heatmaps_sample_size = self.doc["Plots"]["Heatmaps"]["Region"]
                                if not "Gif_it" in self.doc["Plots"]["Heatmaps"]:
                                    print("YamlTagWarning: Gif_it tag within Plots-Heatmaps tag was not provided and is not mandatory tag:")
                                    print("The default value `Gif_it = False` was chosen.")
                                    self.doc["Plots"]["Heatmaps"]["Gif_it"] = False                         

                    if not "Contour Plots" in self.doc["Plots"]:
                        print("YamlTagError: Contour Plots within Plots tag is a mandatory tag")
                        sys.exit(1)
                    else:
                        if not "Linear" in self.doc["Plots"]["Contour Plots"]:
                            print ("YamlTagError: Linear within Plots-Contour Plots tag is a mandatory tag")
                            sys.exit(1)
                        else:
                            if not "Plot_it" in self.doc["Plots"]["Contour Plots"]["Linear"]:
                                print ("YamlTagError: Plot_it within Plots-Contour Plots-Linear tag is a mandatory tag")
                                sys.exit(1)

                        if not "Log" in self.doc["Plots"]["Contour Plots"]:
                            print ("YamlTagError: Log within Plots-Contour Plots tag is a mandatory tag")
                            sys.exit(1)
                        else:
                            if not "Plot_it" in self.doc["Plots"]["Contour Plots"]["Log"]:
                                print ("YamlTagError: Plot_it within Plots-Contour Plots-Log tag is a mandatory tag")
                                sys.exit(1)
                                      
                    if not "Quiver" in self.doc["Plots"]:
                        print ("YamlTagError: Quiver within Plots tag is a mandatory tag")
                        sys.exit(1)
                    else:
                        if not "Plot_it" in self.doc["Plots"]["Quiver"]:
                            print ("YamlTagError: Plot_it within Plots-Quiver tag is a mandatory tag")
                            sys.exit(1)

                    if not "Streamplots" in self.doc["Plots"]:
                        print ("YamlTagError: Streamplots within Plots tag is a mandatory tag")
                        sys.exit(1)
                    else:
                        if not "Plot_it" in self.doc["Plots"]["Streamplots"]:
                            print ("YamlTagError: Plot_it within Plots-Streamplots tag is a mandatory tag")
                            sys.exit(1)

                    if not "Incremental Contour" in self.doc["Plots"]:
                        print ("YamlTagWarning: Incremental Contours within Plots tag is a mandatory tag")
                        sys.exit(1)
                    else:
                        if not "Plot_it" in self.doc["Plots"]["Incremental Contour"]:
                            print ("YamlTagError: Streamplots within Plots tag is a mandatory tag")
                            sys.exit(1)
                        else:
                            self.plot_inccontour = self.doc["Plots"]["Incremental Contour"]["Plot_it"]
                        if not "Target Plot" in self.doc["Plots"]["Incremental Contour"]:
                            print ("YamlTagError: Target Plot within Plots-Incremental Concours tag is a mandatory tag")
                            sys.exit(1)
                        else:
                            self.plot_inccontour_target = self.doc["Plots"]["Incremental Contour"]["Target Plot"]                    