from __future__ import division
import pandas as pd
import numpy as np
from multiprocessing import Pool
from functools import partial
import re
import time
from matplotlib import pyplot as plt
from pprint import pprint

cpam = 'cpam'
departement = 'departement'
densite = 'densite'
specialite = 'exe_spe'
depassement = 'dep_mon'
spe = 'SPECIALITE'
spe_dpt = [specialite, departement]
spe_dpt_dep = [specialite, departement, depassement]
spe_dpt_dens = [specialite, departement, densite]


def str_to_float(s):
    s = s.replace(',', '.')
    return float(re.search('([-]?[0-9]*\.?[0-9]*)', s).group(0))


def extract_useful_cols(y, m):
    path = 'in/R' + str(y) + str(m).zfill(2) + '_sanslib.CSV'
    df = pd.read_csv(path, sep=';')
    df = df[[depassement, cpam, specialite]]
    df[depassement] = df[depassement].map(str_to_float)
    df[departement] = df[df[depassement] > 0][cpam].map(lambda x: str(x)[:-1])
    return df.drop(cpam, 1).groupby(spe_dpt, sort=False).count().reset_index()


def nettoyer_fichiers_R(years, nb_months):
    depassements = []
    months = [m for m in range(1, nb_months)]
    for year in years:
        with Pool() as pool:
            func = partial(extract_useful_cols, year)
            depassements.append(pd.concat(pool.map(func, months)))
    depassements = pd.concat(depassements)
    depassements = depassements.groupby(spe_dpt)[depassement].sum()
    depassements.to_csv('out/dep_par_spe_et_dpt.csv', header=True)


def parse_dpt(s):
    s = re.sub(r'A|B', '0', s)
    return re.search('\d\d', s).group(0)


def nettoyer_fichiers_rpps():
    read_options = {
        'sep': ';',
        'encoding': 'utf8',
        'skiprows': [i for i in range(1, 23)]
    }
    df = pd.read_csv('in/rpps-medecins.csv', **read_options)
    df[departement] = df[spe].map(parse_dpt)
    df = df.set_index(departement)
    cols = [0, 1, 2, 5, 21, 23, 24, 25, 26, 32, 39]
    df.drop(df.columns[cols], 1, inplace=True)

    # pour rassembler les 2 corses:
    df = df.groupby(level=0, sort=False).mean()

    corr_df = pd.read_csv('in/correspondance_rpps_r.csv')
    corr_map = [c['exe_spe'] for _, c in corr_df.iterrows()]

    i = 0
    c_dpt = pd.Series()
    c_spe = pd.Series()
    c_dens = pd.Series()
    for spe_idx, spe_label in enumerate(df.columns):
        for d in df.index.values:
            c_dpt.set_value(i, int(d))
            c_spe.set_value(i, corr_map[spe_idx])
            c_dens.set_value(i, df[spe_label][d])
            i += 1

    pieces = pd.DataFrame({
        departement: c_dpt, specialite: c_spe, densite: c_dens
    }).groupby(spe_dpt, sort=False)[densite].sum()
    pieces.to_csv('out/rpps-medecins-clean.csv', header=True)


def merge(depassements, densites):
    union = pd.merge(depassements, densites, on=spe_dpt, sort=False)
    union.to_csv('out/correlation_densite_depassement.csv', header=True)
    corr = float(np.corrcoef(union[densite], union[depassement])[0, 1])
    print("Correlation entre la densité de medecin par specialite et "
          "par departement et la pratique du dépassement d\'honoraires:", corr)

    if True:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(union[densite], union[depassement])
        ax.set_ylim(ymin=0)
        ax.set_xlim(xmin=0)
        plt.show()


def main():
    t_start = time.time()
    print("Nettoyage des fichiers contenant les données de soin...")
    nettoyer_fichiers_R([2015], 12)
    print("Terminé en", (time.time()-t_start), 's\n')

    t_start = time.time()
    print("Nettoyage des fichiers contenant les densités des médecins...")
    nettoyer_fichiers_rpps()
    print("Terminé en", (time.time()-t_start), 's\n')

    print("Merge des données et calcul de la corrélation...")
    depassements = pd.read_csv('out/dep_par_spe_et_dpt.csv')
    densites = pd.read_csv('out/rpps-medecins-clean.csv')
    merge(depassements, densites)

main()
