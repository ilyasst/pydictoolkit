from pydictoolkit import *
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="python main.py -d './mydata/deck.yaml'")

    parser.add_argument("-d", "--mydeck", 
                    action="store",
                    dest="deck",
                    type=str,
                    help="provide the path to your deck file (please see README.md)",
                    default="./deck.yaml",
                    required=True)

    args = parser.parse_args()

    if args.deck:
        try:
            f = open(args.deck)
        except IOError:
            print("The provided path does not seem to exist.")
            sys.exit(1)
        finally:
            f.close()

    deck = Deck(args.deck)

    dic_data = DIC_reader(deck.data_folder)
    dic_report = DIC_measurements(dic_data, deck)

    data_modes = DataMods(dic_data.dataframe, deck)

    plott = Plotter(
            dic_data, 
            deck, 
            data_modes,
            plot_deltas = False,
            )   