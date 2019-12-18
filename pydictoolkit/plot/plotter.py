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
                plot_stream = False,
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
            
            if plot_stream == True:
                self.create_quiver(dic_data.dic_paths[index], dic_image)
                self.create_streamplot(dic_data.dic_paths[index], dic_image)

        if create_gif == True:
            self.create_gif(data_modes.grouped, deck, data_modes.scale_min, data_modes.scale_max)

    def create_quiver(self, file_name, df):  
        x = list(sorted(set( df["x"].values )))
        y = list(sorted(set( df["y"].values )))
                
        df.loc[df["sigma"] == -1, "gamma" ] = np.nan
        self.teta_ = np.array(df["gamma"].values)
        
        teta_1 = np.cos(self.teta_)
        self.teta_1 = teta_1.reshape(len(y), len(x))
        
        teta_2 = np.sin(self.teta_) 
        self.teta_2 = teta_2.reshape(len(y), len(x))
        
        contour_ = np.array(df[self.zz].values)
        self.contour_ = contour_.reshape((len(y), len(x)))
        
        # QUIVER
        #img_name = file_name[0 : len(file_name) -3] + 'tif'
        #img = plt.imread("/Users/benedictebonnet/pydictoolkit/pydictoolkit/" + img_name)

        fig, ax = plt.subplots(dpi=300)
        #ax.imshow(img, cmap = plt.get_cmap('gray'), alpha = 0.5)
        skip1 = ( slice(None, None, 20))
        skip2 = ( slice(None, None, 20), slice(None, None,20) )
        q = ax.quiver(np.array(x[skip1]), np.array(y[skip1]), np.array(self.teta_1[skip2]), np.array(self.teta_2[skip2]), np.array(self.contour_[skip2]), 
            cmap = 'plasma',
            scale = 50)
        ax.quiverkey(q, X=3, Y=3, U=1,
             label='Quiver key, length = 10', labelpos='N')
        plot_dir = "./plots/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
              os.makedirs(plot_dir)
        plt.savefig("./plots/"+self.zz.strip('"')+"-"+file_name[:-4]+"-quiver"+".png")
        plt.close()


    def create_streamplot(self, file_name, df):  

        def compute_step(point1, point2, point3, point4):
            step = 1+np.sqrt(pow(point2-point1,2)+pow(point4-point3,2))/18
            return step
        
        x = list(sorted(set( df["x"].values )))
        y = list(sorted(set( df["y"].values )))

        # STREAMLINES 
        #img_name = file_name[0 : len(file_name) -3] + 'tif'
        #img2 = plt.imread("/Users/benedictebonnet/pydictoolkit/pydictoolkit/" + img_name)
        fig2, ax = plt.subplots(dpi=300)
        #ax.imshow(img2, cmap = plt.get_cmap('gray'), alpha = 0.5)

        # Set points where you want a streamline
        # referencex = []
        # referencey = []

        # mypoints = [ [ (1530,1812,1003,866),(1530,1775,1033,1130),(1775,1951,1130,1054),(1530,1748,1003,1375),(1530,1221,1003,1421),(1530,530,1003,1488),(1530,636,1003,991)]] #pour une ligne (startx, endx, starty, endy)
        # for sline in mypoints : 
        #     for points in sline : 
        #         toto =  np.linspace(points[0], points[1], compute_step(points[0], points[1],points[2], points[3]), endpoint=True).tolist()
        #         tata = np.linspace(points[2], points[3],compute_step(points[0], points[1],points[2], points[3]), endpoint=True).tolist()
        #         referencex += toto
        #         referencey += tata      
        # seed_points = np.array([referencex,referencey])  
        
        #import pdb; pdb.set_trace()
       # ax.plot(seed_points[0], seed_points[1], 'wx', markersize=0.5)
        fig2 = plt.streamplot(np.array(x), np.array(y), np.array(self.teta_1),np.array(self.teta_2), 
                    #start_points=seed_points.T,
                    color=self.contour_, 
                    linewidth=0.5, 
                    cmap='plasma', 
                    density=5, 
                    arrowsize=0.5)
        plt.colorbar() 
        plot_dir = "./plots/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
             os.makedirs(plot_dir)
        plt.savefig("./plots/"+self.zz.strip('"')+"-"+file_name[:-4]+"-stream"+".png")
        plt.close()

    def plot_dataset(self, file_name, df, deck):
         df = df.sort_index(axis=1, level='"x"', ascending=False)
         x = list(set( df["x"].values ))
         y = list(set( df["y"].values ))
         z = df[self.zz]
         zv = z.values
         zv = np.array(zv)
         zv = zv.reshape((len(y), len(x)))
         fig = plt.contour(x, y, zv, levels=8, linewidths=0.4, colors="black")
         if self.plot_grid == True:
             for i in range(0,max(df["x"]), int(deck.sample_size["i"])):
                 plt.axvline(i,color='red', linewidth=0.1) 
             for j in range(0, max(df["y"]), int(deck.sample_size["j"])):
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

        x = list(set( df["x"].values ))
        y = list(set( df["y"].values ))
        z = df[self.zz.strip("'").strip('"')+"_delta"]
        zv = z.values
        zv = np.array(zv)
        zv = zv.reshape((len(y), len(x)))
        fig = plt.contour(x, y, zv, levels=8, linewidths=0.4, colors="black")
        if self.plot_grid == True:
            for i in range(0,max(df["x"]), int(deck.sample_size["i"])):
                plt.axvline(i,color='red', linewidth=0.1) 
            for j in range(0, max(df["y"]), int(deck.sample_size["j"])):
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
        writer='matplotlib.animation.PillowWriter'
        #'imagemagick'

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