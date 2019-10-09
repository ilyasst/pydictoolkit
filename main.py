from pydictoolkit import *

deck = Deck("deck.yaml")

dic_data = DIC_reader(deck.dic_path)

plott = Plotter(dic_data.dataframe)