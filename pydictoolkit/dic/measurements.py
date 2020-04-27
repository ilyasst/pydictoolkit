import csv

class DIC_measurements:
    def __init__(self, dfs, deck):
        self.report = []
        for index, df in enumerate(dfs.dataframe):
            temp = {}
            temp['filename'] = dfs.dic_paths[index]
            temp['index'] = index
            self.report.append(temp)

        for index, df in enumerate(dfs.dataframe):
            dfs.dataframe[index] = df.astype('float64')
        
        self.compute_measurements(dfs.dataframe)
        self.write_report(dfs.dataframe, deck)
        

    def compute_measurements(self,dfs):
        for index, df in enumerate(dfs):
            encr = df['sigma'] != -1.0
            df_encr = df[encr]
            
            # CALCUL DE LA SURFACE DE L'AOI DU SPECIMEN 
            AOI = len(df_encr['x'])

            # TAILLE DU PIXEL : LONGUEUR EN MM / NOMBRE DE PIXELS
            resolution_x = (df_encr['X'].max()-df_encr['X'].min()) / (df_encr['x'].max()-df_encr['x'].min())
            
            resolution_y = (df_encr['Y'].max()-df_encr['Y'].min()) / (df_encr['y'].max()-df_encr['y'].min())

            # CALCUL DE LA MAX des strains
            max_exx = max(df_encr['exx'].values)
            max_eyy = max(df_encr['eyy'].values)
            max_e1 = max(df_encr['e1'].values)
            max_e2 = max(df_encr['e2'].values)

            # ecriture dans le dictionnaire
            self.report[index]['AOI_px2'] = AOI
            self.report[index]['resolution_x'] = resolution_x
            self.report[index]['resolution_y'] = resolution_y
            self.report[index]['max_exx'] = max_exx
            self.report[index]['max_eyy'] = max_eyy
            self.report[index]['max_e1'] = max_e1
            self.report[index]['max_e2'] = max_e2


    def write_report(self, dfs, deck):
        csv_columns = []
        csv_file = "./plots/Report.csv"
        for key in self.report[0]:
             csv_columns.append(key)
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in self.report:
                    writer.writerow(data)
        except IOError:
            print("I/O error")






