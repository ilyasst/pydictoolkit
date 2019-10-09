import matplotlib.pyplot as plt
import numpy as np

class Plotter():

    def __init__(self, dic_data):

        for dic_image in dic_data:
            dic_image.columns = dic_image.columns.str.strip()
            self.plot_dataset(dic_image)

    def plot_dataset(self, df):
        print(df.head())
        x = list(set( df['"x"'].values ))
        y = list(set( df['"y"'].values ))
        z = df['"e1"']
        zv = z.values
        zv = np.array(zv)
        zv = zv.reshape((len(y), len(x)))
        fig = plt.contour(x, y, zv, levels=8, linewidths=0.4, colors="black")

        plt.title(z.name)
        plt.clabel(fig, inline=0.1, fontsize=5)
        plt.legend()

        plt.show()