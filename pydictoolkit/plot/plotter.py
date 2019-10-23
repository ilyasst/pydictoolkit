import matplotlib.pyplot as plt
from matplotlib import animation
import seaborn as sns
import numpy as np
import cmocean
import os

class Plotter():

    def __init__(self, zz, dic_data, deck, data_modes,
                plot_grid = False, 
                plot_deltas = False,
                plot_heatmaps = False,
                create_gif = False):

        self.zz = zz
        self.plot_grid = plot_grid

        for index, dic_image in enumerate(dic_data.dataframe):
            self.plot_dataset(dic_data.dic_paths[index], dic_image, deck)
            if plot_deltas == True:
                self.plot_deltas(dic_data.dic_paths[index], dic_image, deck)
            
            if plot_heatmaps == True:
                for index2, gdf in enumerate(data_modes.grouped):
                    if index == index2:
                        self.build_deltaheatmaps(dic_data.dic_paths[index], gdf, deck, data_modes.scale_min, data_modes.scale_max)    
        if create_gif == True:
            self.create_gif(data_modes.grouped, deck, data_modes.scale_min, data_modes.scale_max)
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

    
    def build_deltaheatmaps(self, file_name, df, deck, vmin, vmax):
        ''' 
        Plots a heatmap for each image with delta variations over the x and y splitting regions 
        df = pandas data frame with set index, one column and target values.  
        '''   
        df = df.pivot('region_y', 'region_x', deck.target)
        #df = df.sort_index(ascending=False)
        
        fig, ax = plt.subplots(figsize=(9,6))
        sns.set()
        # bug of matplotlib 3.1 forces to manually set ylim to avoid cut-off top and bottom
        # might remove this later
        sns.heatmap(df, linewidths= .5, vmin = float(vmin), vmax = float(vmax), annot = True, annot_kws={"size": 9}, cmap = cmocean.cm.curl, ax = ax)
        ax.set_ylim(len(df), 0)
        plot_dir = "./plots/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
            os.makedirs(plot_dir)
        fig.savefig( "./plots/"+self.zz.strip('"')+"-"+file_name[:-4]+"_heatmap"+".png")
        plt.close()

    def create_gif(self, dfs, deck, vmin, vmax):
        #set base plotting space 
        fig = plt.figure(figsize=(9,6))
        fig.title = "how about now"

        # make global min/max for the whole array,
        # so colour scale will be consistent between the frames
        #data_min = vmin
        #data_max = vmax

        # create iterator
        data_frames_iterator = iter(dfs)

        # set up formatting of the gif later
        writer='imagemagick'

        def update_frame(i):
            plt.clf()
            heatmap_data = next(data_frames_iterator)
            heatmap_data = heatmap_data.pivot('region_y', 'region_x', deck.target)
            ax = sns.heatmap(heatmap_data,
                             linewidths= 0, 
                             vmin = float(vmin), 
                             vmax = float(vmax), 
                             annot = True, 
                             annot_kws={"size": 9}, 
                             cmap = "YlGnBu",
                            )
            #need to manually set y_lim to avoi cropping of top and bottom cells                
            ax.set_ylim(heatmap_data.shape[0], 0)

        animation.FuncAnimation(fig, update_frame, frames=len(dfs)-1, interval=400).save('heatmaps.gif', writer = writer)
            
    