import matplotlib.pyplot as plt
import matplotlib
from matplotlib import animation
import seaborn as sns
import numpy as np
import cmocean
import os
from mpl_toolkits.axes_grid1 import AxesGrid
from mpl_toolkits.axes_grid1 import make_axes_locatable
import scipy
import scipy.ndimage
from scipy.stats import norm
import matplotlib.image as mpimg

class Plotter():

    def __init__(self, dic_data, deck, data_modes,
                plot_grid = False, 
                plot_deltas = False,
                plot_heatmaps = False,
                plot_stream = False,
                create_gif = False):
        self.zz = deck.doc["Plots"]['Target Plot']
        self.plot_grid = plot_grid
        
        for index, dic_image in enumerate(dic_data.dataframe):
            self.plot_dataset(dic_data.dic_paths[index], dic_image, deck)

            if plot_deltas == True:
                if index == 0:
                    pass
                else:
                    self.plot_deltas(dic_data.dic_paths[index], dic_image, deck)
            
            if plot_heatmaps == True:
                for index2, gdf in enumerate(data_modes.grouped):
                    if index == index2:
                        self.build_deltaheatmaps(dic_data.dic_paths[index], gdf, deck, data_modes.scale_min, data_modes.scale_max)
            
            if plot_stream == True:
                self.create_contourplot_log(dic_data.dic_paths[index], dic_image, deck, data_modes)
                self.create_contourplot_linear(dic_data.dic_paths[index], dic_image, deck, data_modes)
                self.create_quiver(dic_data.dic_paths[index], dic_image)
                self.create_streamplot(dic_data.dic_paths[index], dic_image)

        if create_gif == True:
            self.create_gif(data_modes.grouped, deck, data_modes.scale_min, data_modes.scale_max)

    def filter_NaN_Matrix(self, U, sigVal):  
        #Fonction pour limiter la propagation des NaNs dans le filtre gaussien lissant l'image,
        V=U.copy()
        V[np.isnan(U)]=0
        VV=scipy.ndimage.gaussian_filter(V,sigma=sigVal)

        W=0*U.copy()+1
        W[np.isnan(U)]=0
        WW=scipy.ndimage.gaussian_filter(W,sigma=sigVal)

        np.seterr(divide='ignore', invalid='ignore') #enleve le pb de division /0
        Z=VV/WW
        return Z 

    def create_contourplot_log(self, file_name, df, deck, data_modes): 
        x = list(sorted(set( df["x"].values )))
        y = list(sorted(set( df["y"].values )))
        
        
        img_name = file_name[0 : len(file_name) -10] + '.tif'
        img = plt.imread(img_name)
        fig, ax = plt.subplots(dpi=300)
        ax.imshow(img, alpha = 1, cmap = 'gray')
        
        df.loc[df["sigma"] == -1, deck.doc["Plots"]['Target Plot'] ] = np.nan
        e1 = np.array(df[deck.doc["Plots"]['Target Plot']].values)
        e1 = e1.reshape(len(y), len(x))

        levels = np.sort(np.append( np.append( -np.logspace(0.1, abs(data_modes.vmin_0),10) , np.linspace(-0.01,0.01,5) ), np.logspace(0.1,data_modes.vmax_0,15)))
        ax.contour(x, y, e1, colors = 'k', linewidths = 0.5, levels = levels) 
        pcm = ax.pcolormesh(x,y,e1,norm=matplotlib.colors.SymLogNorm(linthresh=0.001, linscale=0.1, vmin=data_modes.vmin_0, vmax=data_modes.vmax_0),
             cmap='plasma')
        fig.colorbar(pcm, ax=ax, extend = 'both')

        plot_dir = "./plots/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
              os.makedirs(plot_dir)
        plt.savefig("./plots/"+self.zz.strip('"')+"-"+file_name[:-4]+"-contourplot-log"+".png")
        plt.close()

    def create_contourplot_linear(self, file_name, df, deck, data_modes): 
        x = list(sorted(set( df["x"].values )))
        y = list(sorted(set( df["y"].values )))
                                
        img_name = file_name[0 : len(file_name) -10] + '.tif'
        img = plt.imread(img_name)
        fig, ax = plt.subplots(dpi=300)
        ax.imshow(img, alpha = 1, cmap = 'gray')

        df.loc[df["sigma"] == -1, deck.doc["Plots"]['Target Plot'] ] = np.nan  
        e1 = np.array(df["e1"].values)
        e1 = e1.reshape(len(y), len(x))
        levels = np.linspace(data_modes.vmin_0, data_modes.vmax_0,10) 
        cs = plt.contourf(x, y, e1, origin = 'lower', extend = 'both', cmap = 'plasma', alpha = 0.5) 
        plt.contour(x, y, e1, levels = levels, colors = 'k', linewidths = 0.5) 
        fig.colorbar(cs)

        plot_dir = "./plots/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
            os.makedirs(plot_dir)
        plt.savefig("./plots/"+self.zz.strip('"')+"-"+file_name[:-4]+"-contourplot-linear"+".png")
        plt.close()

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
    
        img_name = file_name[0 : len(file_name) -10] + '.tif'
        img = plt.imread(img_name)
        fig, ax = plt.subplots(dpi=300)
        ax.imshow(img, cmap = plt.get_cmap('gray'), alpha = 1)

        skip1 = ( slice(None, None, 20))
        skip2 = ( slice(None, None, 20), slice(None, None,20) )

        tf1 = self.filter_NaN_Matrix(np.array(self.teta_1),7)
        tf2 = self.filter_NaN_Matrix(np.array(self.teta_2),7)
        contourf = self.filter_NaN_Matrix(np.array(self.contour_),7)

        plt.quiver(np.array(x[skip1]),np.array(y[skip1]),tf1[skip2], tf2[skip2], contourf[skip2], cmap='plasma', scale = 50)
        plt.colorbar()

        plot_dir = "./plots/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
              os.makedirs(plot_dir)
        plt.savefig("./plots/"+self.zz.strip('"')+"-"+file_name[:-4]+"-quiver"+".png")
        plt.close()

    def create_streamplot(self, file_name, df):       
        x = list(sorted(set( df["x"].values )))
        y = list(sorted(set( df["y"].values )))

        img_name = file_name[0 : len(file_name) -10] + '.tif'
        img = plt.imread(img_name)
        
        fig, ax = plt.subplots(dpi=300)
        ax.imshow(img, cmap = plt.get_cmap('gray'), alpha = 1)

        tf1 = self.filter_NaN_Matrix(np.array(self.teta_1),7)
        tf2 = self.filter_NaN_Matrix(np.array(self.teta_2),7)
        contourf = self.filter_NaN_Matrix(np.array(self.contour_),7)
        
        fig = plt.streamplot(np.array(x), np.array(y), tf1, tf2, 
                    color=contourf, 
                    linewidth=1, 
                    cmap='plasma', 
                    density=1.3, 
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
         x = list(sorted(set( df["x"].values )))
         y = list(sorted(set( df["y"].values )))
         
         df.loc[df["sigma"] == -1, deck.doc["Plots"]['Target Plot'] ] = np.nan
         zv = 100*(df[deck.doc["Plots"]['Target Plot']].values)
         zv = zv.reshape((len(y), len(x)))
         
         fig = plt.contour(x, y, zv, levels=8, linewidths=0.4, colors="black")
         cs = plt.contourf(x, y, zv, origin = 'lower', extend = 'both', cmap = 'plasma', alpha = 0.5)
         cbar = plt.colorbar(cs)
         cbar.ax.set_xlabel('Strain (%)')

         if self.plot_grid == True:
             for i in range(0,max(df["x"]), int(deck.sample_size["i"])):
                 plt.axvline(i,color='red', linewidth=0.1) 
             for j in range(0, max(df["y"]), int(deck.sample_size["j"])):
                 plt.axhline(j,color='red', linewidth=0.1)
         plt.title(deck.doc["Plots"]['Target Plot'])
         plt.clabel(fig, inline=0.1, fontsize=5)
         plt.legend()
        
         plot_dir = "./plots/"
         check_folder = os.path.isdir(plot_dir)
         if not check_folder:
             os.makedirs(plot_dir)
         plt.savefig("./plots/"+self.zz.strip('"')+"-"+file_name[:-3]+"png")
         plt.close()
    
    def plot_deltas(self, file_name, df, deck):
        df = df.sort_index(axis=1, level='"x"', ascending=False)
        x = list(sorted(set( df["x"].values )))
        y = list(sorted(set( df["y"].values )))
        
        df.loc[df["sigma"] == -1, deck.doc["Plots"]['Target Column'] ] = np.nan
        zv = 100*(df[deck.doc["Plots"]['Target Column']].values)
        
        z1 = df['e1'].values
        z2 = df['e2'].values
        zv = abs(np.divide(-z2, z1))
        mu, std = norm.fit(zv)
        plt.hist(zv, bins = 3, density = True, alpha=0.6, color='g')
        amin, amax = np.nanmin(zv), np.nanmax(zv)
        a = np.linspace(amin, amax, 100)
        p = norm.pdf(a, mu, std)
        plt.plot(a, p, 'k', linewidth=2)
        title = "Fit results e1 percent mu = %.2f,  std = %.2f" % (mu, std)
        plt.title(title)
        plot_dir = "./plots/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
            os.makedirs(plot_dir)
        plt.savefig("./plots/"+self.zz.strip('"')+"-"+file_name[:-4]+"_gauss"+".png")
        plt.close()

        # test pour calcul de nu
        z1 = df['e1'].values
        z1[abs(z1)<0.00001]=np.nan
        z1 = z1.reshape((len(y), len(x)))
        z2 = df['e2'].values
        z2[abs(z2)<0.00001]=np.nan
        z2 = z2.reshape((len(y), len(x)))
        zv = abs(np.divide(-z2, z1))
        #zv = df[deck.doc['Target Column']].values
        #zv = zv.reshape((len(y), len(x)))
        fig = plt.contour(x, y, zv, levels=8, linewidths=0.4, colors="black")
        cs = plt.contourf(x, y, zv, origin = 'lower', extend = 'both', cmap = 'plasma', alpha = 0.5)
        cbar = plt.colorbar(cs)
        cbar.ax.set_xlabel('Strain (%)')
        if self.plot_grid == True:
            for i in range(0,max(df["x"]), int(deck.sample_size["i"])):
                plt.axvline(i,color='red', linewidth=0.1) 
            for j in range(0, max(df["y"]), int(deck.sample_size["j"])):
                plt.axhline(j,color='red', linewidth=0.1)
        plt.title(deck.doc["Plots"]['Target Column'])
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