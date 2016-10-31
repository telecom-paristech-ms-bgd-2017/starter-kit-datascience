import pandas as pd

df1 = pd.read_csv(
    '/Users/Bense/Documents/Exercices/Charles/TP5/R2015_sans_lib/R201501_sanslib.CSV', delimiter=';')

cpam_variable = pd.read_excel('/Users/Bense/Documents/Exercices/Charles/TP5/R2015_sans_lib/descriptif_table_R.xls',sheetname=4)
cpam_variable.columns = ['cpam', 'region']
cpam_variable.set_index('cpam')

result = pd.merge(df, cpam_variable, on='cpam')

df.head(100)

df['region']

df.dtypes
