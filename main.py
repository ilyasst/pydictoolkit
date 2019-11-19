from pydictoolkit import *

deck = Deck("deck.yaml")

dic_data = DIC_reader(deck.dic_path)

data_modes = DataMods(dic_data.dataframe, deck)

key = "teta_1"

plott = Plotter(
        key,
        dic_data, 
        deck, 
        data_modes,
        plot_grid = False, 
        plot_deltas = False,
        plot_heatmaps = False,
        plot_stream = True,
        create_gif= False
        )   