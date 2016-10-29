import pandas as pd
from os import listdir
from os.path import isfile, join
import re
import numpy as np

INSURANCE_DATA_PATH = "/home/nicolas/Documents/Tmp/Exo_Dom_5/CSV/R2015_sans_lib"
LEXIQUE_PATH = "/home/nicolas/Documents/Tmp/Exo_Dom_5/CSV/Lexique tables R"
RPPS_PATH = "/home/nicolas/Documents/Tmp/Exo_Dom_5/CSV/rpps_2015.csv"
MAPPING_SPECIALTIES_PATH = '/home/nicolas/Documents/Tmp/Exo_Dom_5/CSV/Mapping/correspondance_rpps_damir_r_l_exe_spe.csv'

DEBUG = True

def extract_dept_R(str_dept):
    pattern_rgx_dept = '([0-9{1-3}]+-)'
    return extract_dept(str_dept, pattern_rgx_dept)


def extract_dept_RPPS(str_dept):
    pattern_rgx_dept = '([0-9{1-3}]+\s-\s)'
    return extract_dept(str_dept, pattern_rgx_dept)


def extract_dept(str_dept, rgx_pattern):
    rgx = re.compile(rgx_pattern, re.IGNORECASE)
    try:
        res = rgx.findall(str_dept)[0]
        return str_dept.replace(res, "")
    except:
        return str_dept

def load_insurance_data(file_number):
    if file_number < 10:
        str_file_number = "0" + str(file_number)
    else:
        str_file_number = str(file_number)
    file_name = "R2015{0}_sanslib.CSV".format(str_file_number)
    full_path = "{0}/{1}".format(INSURANCE_DATA_PATH, file_name)
    return pd.read_csv(full_path, sep=';', converters={"cpam": int})


def clean_insurance_data(df_):

    # transform into float
    df_['dep_mon'] = df_['dep_mon'].str.replace(".", "")
    df_['dep_mon'] = df_['dep_mon'].str.replace(",", ".")
    df_['dep_mon'] = df_['dep_mon'].astype(float)

    # Remove useless columns
    df_ = df_[["cpam", "exe_spe", "dep_mon"]]

    # Do the column name mapping
    mapping = {'cpam': 'cpam.csv', 'exe_spe': 'lib_n_exe_spe.csv'}

    df_ = join_data_with_labels(df_, lexiques, mapping)
    df_ = df_[['cpam', 'exe_spe', 'l_dpt', 'dep_mon']]

    df_['l_dpt'] = df_['l_dpt'].map(extract_dept_R)
    return df_


def load_lexiques():
    files = [f for f in listdir(LEXIQUE_PATH) if isfile(join(LEXIQUE_PATH, f))]
    res = {}
    for csv in files:
        df = pd.read_csv("{0}/{1}".format(LEXIQUE_PATH, csv), sep=';', encoding="latin 1")
        res[csv] = df
    return res


def join_data_with_labels(data, lexiques, mapping):
    for k in mapping.keys():
        file_name = mapping[k]
        df_lexique = lexiques[file_name]
        data = data.merge(right=df_lexique, how='inner', on=k)
    return data


def clean_rpps(df_):
    df_.dropna(inplace=True)
    df_.drop(df_.index[range(21)], inplace=True)
    del df_["Médecine générale"]
    del df_["Ensemble des spécialités d'exercice"]
    del df_["Spécialistes"]
    df_ = pd.melt(df_, id_vars=['SPECIALITE'], var_name='SPEC_TMP')
    df_.columns = ['DEPT', 'SPECIALITE', 'DENSITE']
    df_['DEPT'] = df_['DEPT'].map(extract_dept_RPPS)
    return df_


# Main script

lexiques = load_lexiques()
specialties = pd.read_csv(MAPPING_SPECIALTIES_PATH, sep=',')

df_R = load_insurance_data(1)
if DEBUG:
    df_R = df_R[0:10]

df_R = clean_insurance_data(df_R)
df_rpps = pd.read_csv(RPPS_PATH, sep=',', skiprows=4, encoding="latin 1")
df_rpps = clean_rpps(df_rpps)

print(df_R)
print(df_rpps)
# print(df_rpps.columns)
# print(df_rpps)
#

# pd.DataFrame(unique_dept_R).to_csv("/home/nicolas/Documents/Tmp/Exo_Dom_5/CSV/dept_R_New.csv")
# pd.DataFrame(unique_dept_rpps).to_csv("/home/nicolas/Documents/Tmp/Exo_Dom_5/CSV/dept_RPPS_New.csv")

# join :
# df_R : [exe_spe, l_exe_spe]
# df_rpps : [specialite_rpps, exe_spe]

# df_rpps join mapping on exe_spe join df_R specialite_rpps join df_r on exe_spe and dept
df_tmp = df_R.merge(specialties, how='inner', left_on='exe_spe', right_on='l_exe_spe')
df_joined = df_tmp.merge(df_rpps, how='inner', left_on='col_rpps', right_on='SPECIALITE')
print(len(df_R.index))
print(len(df_rpps.index))
print(len(df_tmp.index))
print(len(df_joined.index))

df_joined[0:1000].to_csv("/home/nicolas/Documents/Tmp/Exo_Dom_5/CSV/temp.csv")
