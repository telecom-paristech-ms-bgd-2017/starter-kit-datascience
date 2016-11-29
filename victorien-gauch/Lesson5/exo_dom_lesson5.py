import pandas as pd

url = 'https://raw.githubusercontent.com/SGMAP-AGD/densite_medecins/master/data/rpps_tab3.csv'

content = pd.read_csv(url, sep=',', names=['mode_exercice', 'zone_inscription', 'annee', 'specialite', 'effectifs'], skiprows=1, header=None)
df_rpps_tab3 = content.dropna()

#print(df_rpps_tab3)


content2 = pd.read_csv('damir1.csv', sep=';')
df_damir1 = content2.dropna()
#print(df_damir1)

content3 = pd.read_csv('damir2.csv', sep=';')
df_damir2 = content2.dropna()

print(df_damir2)



