import matplotlib.pyplot as plt
import numpy as np
import os

class Plotter():

    def __init__(self, zz, dic_data, deck, 
                plot_grid = False, 
                plot_deltas = False,
                plot_heatmaps = False):

        self.zz = zz
        self.plot_grid = plot_grid

        for index, dic_image in enumerate(dic_data.dataframe):
            self.plot_dataset(dic_data.dic_paths[index], dic_image, deck)
            if plot_deltas == True:
                self.plot_deltas(dic_data.dic_paths[index], dic_image, deck)
            if plot_heatmaps == True:
                self.build_deltaheatmaps(dic_data.dic_paths[index], dic_image, deck)
            
            
    def plot_dataset(self, file_name, df, deck):
        print(df.head())
        x = list(set( df['"x"'].values ))
        y = list(set( df['"y"'].values ))
        z = df[self.zz]
        zv = z.values
        zv = np.array(zv)
        zv = zv.reshape((len(y), len(x)))
        fig = plt.contour(x, y, zv, levels=8, linewidths=0.4, colors="black")
        if self.plot_grid == True:
            for i in range(0,max(df['"x"']), int(deck.sample_size["i"])):
                plt.axvline(i,color='red', linewidth=0.1) 
            for j in range(0, max(df['"y"']), int(deck.sample_size["j"])):
                plt.axhline(j,color='red', linewidth=0.1)
        plt.title(z.name)
        plt.clabel(fig, inline=0.1, fontsize=5)
        plt.legend()
        
        plot_dir = "./plots/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
            os.makedirs(plot_dir)
        plt.savefig("./plots/"+self.zz.strip('"')+"-"+file_name[:-3]+"png")
        plt.close()

    
    def plot_deltas(self, file_name, df, deck):

        x = list(set( df['"x"'].values ))
        y = list(set( df['"y"'].values ))
        z = df[self.zz.strip("'").strip('"')+"_delta"]
        zv = z.values
        zv = np.array(zv)
        zv = zv.reshape((len(y), len(x)))
        fig = plt.contour(x, y, zv, levels=8, linewidths=0.4, colors="black")
        if self.plot_grid == True:
            for i in range(0,max(df['"x"']), int(deck.sample_size["i"])):
                plt.axvline(i,color='red', linewidth=0.1) 
            for j in range(0, max(df['"y"']), int(deck.sample_size["j"])):
                plt.axhline(j,color='red', linewidth=0.1)
        plt.title(z.name)
        plt.clabel(fig, inline=0.1, fontsize=5)
        plt.legend()

        plot_dir = "./plots/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
            os.makedirs(plot_dir)
        plt.savefig("./plots/"+self.zz.strip('"')+"-"+file_name[:-4]+"_deltas"+".png")
        plt.close()

    
    def build_deltaheatmaps(self, file_name, df, deck):
       print("hi")
       # import pdb; pdb.set_trace()