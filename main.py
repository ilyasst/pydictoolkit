from pydictoolkit import *

deck = Deck("deck.yaml")

dic_data = DIC_reader(deck.dic_path)
dic_report = DIC_measurements(dic_data)

data_modes = DataMods(dic_data.dataframe, deck)

key = "U"

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