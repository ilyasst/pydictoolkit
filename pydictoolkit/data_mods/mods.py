import pandas as pd

class DataMods():
    def __init__(self, dfs):
        self.create_grids(dfs)

    def create_grids(self, dfs, grid_x = 200, grid_y = 200):
        
        for df in dfs:
            x = df['  "x"'] 
            y = df['  "y"']
            df['region_x']= x//grid_x
            df['region_y'] = y//grid_y
        return dfs

        
