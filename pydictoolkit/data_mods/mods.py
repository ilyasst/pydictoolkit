import pandas as pd

class DataMods():
    def __init__(self, dfs):
        self.create_grids(dfs)
        import pdb; pdb.set_trace()
        self.compute_deltas(dfs)
        import pdb; pdb.set_trace()

    # Adds a grid to the data
    def create_grids(self, dfs, grid_x = 200, grid_y = 200):
        
        for df in dfs:
            x = df['"x"'] 
            y = df['"y"']
            df['region_x']= x//grid_x
            df['region_y'] = y//grid_y

    # Computes the delta between consecutive images
    def compute_deltas(self, dfs):
        for index, df in enumerate(dfs):
            for column in df:
                if index == 0:
                    df[column.strip('"').strip("'")+"_delta"] = df[column]
                else:
                    df[column.strip('"').strip("'")+"_delta"] = df[column]-dfs[index-1][column]