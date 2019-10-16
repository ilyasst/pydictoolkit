import matplotlib.pyplot as plt
import numpy as np

class Plotter():

    def __init__(self, dic_data, deck):

        for dic_image in dic_data:
            dic_image.columns = dic_image.columns.str.strip()
            self.plot_dataset(dic_image, deck)
            
    def plot_dataset(self, df,deck, plot_grid = True):
        print(df.head())
        x = list(set( df['"x"'].values ))
        y = list(set( df['"y"'].values ))
        z = df['"e1"']
        zv = z.values
        zv = np.array(zv)
        zv = zv.reshape((len(y), len(x)))
        fig = plt.contour(x, y, zv, levels=8, linewidths=0.4, colors="black")
        if plot_grid == True:
            for i in range(0,max(df['"x"']), int(deck.sample_size["i"])):
                plt.axvline(i,color='red') 
            for j in range(0, max(df['"y"']), int(deck.sample_size["j"])):
                plt.axhline(j,color='red')
        plt.title(z.name)
        plt.clabel(fig, inline=0.1, fontsize=5)
        plt.legend()

        plt.show()
    
