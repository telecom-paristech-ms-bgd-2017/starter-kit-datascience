import pandas as pd

data_medecins = pd.read_csv('rpps-medecins-tab3_31025177929301.csv', encoding='latin-1')
df = data_medecins.loc[lambda df:df.INSCRIPT.str.contains("nsemble"), :]
df.__delitem__('INSCRIPT')

