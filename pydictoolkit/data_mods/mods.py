import pandas as pd
import numpy as np

class DataMods():
    def __init__(self, dfs, deck):
        self.create_grids(dfs, deck)
        self.compute_deltas(dfs)
        self.group_dfs(dfs, deck)
        #self.compute_shifted_cmap(dfs, deck)
        
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
                        df[column.strip('"').strip("'")+"_delta"] = df[column]-dfs[index-1][column]
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

    # def compute_shifted_cmap(self, dfs, deck):
    #     midpoint_f = 1
    #     for df in dfs:
    #         midpoint = 1 - df["e1"].max()  / ( df["e1"].max() + abs(df["e1"].min() ) )# between 0 and 1
    #         if midpoint < midpoint_f:
    #             midpoint_f = midpoint
    #         else:
    #             pass
    #     import pdb; pdb.set_trace()
    #     return midpoint_f
        # start = 0, stop = 1
    