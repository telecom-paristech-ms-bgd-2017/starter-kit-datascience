#!/usr/bin/env python3

# standard library imports
import re
import unicodedata
import string

# related third party imports
import pandas as pd


def normalize(s):
    string_normalized = s.strip().replace(' ', '-')
    return ''.join(x for x in unicodedata.normalize('NFKD', string_normalized)\
                   if x in string.ascii_letters + '-').upper()


def get_number(s):
    return float(s.replace('.', '').replace(',', '.'))


def get_specialties():
    def normalize_specialty(specialty):
        return normalize(specialty[3:].replace('TOTAL', ''))
    xls = pd.ExcelFile('./data/descriptif_table_R.xls')
    df = xls.parse('exe_spe')
    df.rename(columns={'exe_spe': 'id', 'l_exe_spe': 'label'}, inplace=True)
    df['id'] = df['id'].astype(int)
    df.set_index(['id'], inplace=True)
    df['n_label'] = df['label'].apply(normalize_specialty)
    return df


def get_sub_areas():
    def normalize_area(area):
        return normalize(area[3:])
    xls = pd.ExcelFile('./data/descriptif_table_R.xls')
    df = xls.parse('region')
    df.rename(columns={'region': 'id', 'l_region': 'label'}, inplace=True)
    df['id'] = df['id'].astype(int)
    df.set_index(['id'], inplace=True)
    df['n_label'] = df['label'].apply(normalize_area)
    return df


def get_sub_areas():
    def normalize_sub_area(area):
        return normalize(re.sub(r'\d+-', '', area))
    xls = pd.ExcelFile('./data/descriptif_table_R.xls')
    df = xls.parse('dpt')
    df.rename(columns={'dpt': 'id', 'l_dpt': 'label'}, inplace=True)
    df['id'] = df['id'].astype(str)
    df.set_index(['id'], inplace=True)
    df['n_label'] = df['label'].apply(normalize_sub_area)
    return df


def get_match_rpps_with_specialities():
    return pd.read_csv('./data/correspondance_rpps_damir_r_l_exe_spe.csv',
                       index_col=[0])


def get_density_health_professionals():
    def normalize_sub_area(sub_area):
        return normalize(sub_area)
    df = pd.read_csv('./data/rpps_tab3.csv').query('annee == 2014')
    df['zone_inscription'] = df['zone_inscription'].apply(normalize)
    return df


