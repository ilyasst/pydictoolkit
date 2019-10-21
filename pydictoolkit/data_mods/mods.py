import pandas as pd

class DataMods():
    def __init__(self, dfs, deck):
        self.create_grids(dfs, deck)
        self.compute_deltas(dfs)
        self.group_dfs(dfs)
    # Adds a grid to the data
    def create_grids(self, dfs, deck):
        grid_x = int(deck.sample_size["i"])
        grid_y = int(deck.sample_size["j"])
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

    #group dataframes base don regions
    def group_dfs(self, dfs):
        grouped = []
        f = lambda x: x.mean()
        for df in dfs:
            df_grouped = df.groupby(["region_x", "region_y"]).apply(f)
            grouped.append(df_grouped)
        self.grouped = grouped