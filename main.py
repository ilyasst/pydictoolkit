from pydictoolkit import *

deck = Deck("deck.yaml")

dic_data = DIC_reader(deck.dic_path)

data_modes = DataMods(dic_data.dataframe)

plott = Plotter(dic_data.dataframe, deck)