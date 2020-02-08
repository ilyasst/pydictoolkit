import pandas as pd
import numpy as np

class DataMods():
    def __init__(self, dfs, deck):
        self.create_grids(dfs, deck)
        self.compute_deltas(dfs)
        self.compute_relative_errors(dfs)
        self.group_dfs(dfs, deck)
        self.compute_shifted_cmap(dfs, deck)
        
    # Adds a grid to the data
    def create_grids(self, dfs, deck):
        grid_x = int(deck.sample_size["i"])
        grid_y = int(deck.sample_size["j"])
        for df in dfs:
            x = df["x"] 
            y = df["y"]
            df['region_x']= x//grid_x
            df['region_y'] = y//grid_y
        
    
    # Computes the delta between consecutive images
    def compute_deltas(self, dfs):
        for index, df in enumerate(dfs):
            for column in df:  
                if index == 0:
                    pass
                else:
                    try: 
                        df[column+"_delta"] = df[column]-dfs[0][column] #index-1
                    except KeyError: 
                        pass

    def compute_relative_errors(self, dfs):
        for index, df in enumerate(dfs):
            if index == 0:
                pass
            else:
                for column in df:                    
                    try: 
                        df[column+"_delta_relative"] = 100*(df[column+"_delta"].divide(df[column].max()))
                    except KeyError: 
                        pass

    #group dataframes based on regions
    def group_dfs(self, dfs, deck):
        grouped = []
        f = lambda x: x.mean()
        for index, df in enumerate(dfs):
            if index == 0:
                pass
            else:
                df_grouped = df.groupby(["region_x", "region_y"]).apply(f)
                grouped.append(df_grouped)
        
        heat_min = min([min(df[deck.target]) for df in grouped])
        heat_max = max([max(df[deck.target]) for df in grouped])
        self.scale_min = heat_min
        self.scale_max = heat_max
        self.grouped = grouped

    def compute_shifted_cmap(self, dfs, deck):
        vmax_0 = 0.
        vmin_0 = 0.
        for df in dfs:
            if df[deck.doc["Plots"]['Target Plot']].max() > vmax_0:
                vmax_0 = df[deck.doc["Plots"]['Target Plot']].max()
            elif df[deck.doc["Plots"]['Target Plot']].min() < vmin_0:
                vmin_0 = df[deck.doc["Plots"]['Target Plot']].min()
            else:
                pass
        self.vmin_0 = vmin_0
        self.vmax_0 = vmax_0


    