import pandas as pd
import numpy as np

#Patientele_des_medecins_APE_en_2014.xls
#Effectif_et_densite_par_departement_en_2014.xls

listCol = ("Généralistes", "MEP", "Omnipraticiens","Anesthésistes",
           "Cardiologues","Chirurgiens","Dermatologues","Radiologues",
           "Gynécologues","Gastro-entérologues","ORL","Pédiatres",
           "Rhumatologues","Ophtalmologues","Stomatologues",
           "Psychiatres")
arrayCol = ["Généralistes", "MEP", "Omnipraticiens","Anesthésistes",
           "Cardiologues","Chirurgiens","Dermatologues","Radiologues",
           "Gynécologues","Gastro-entérologues","ORL","Pédiatres",
           "Rhumatologues","Ophtalmologues","Stomatologues",
           "Psychiatres"]

def cleanData(df):
    
    for col in listCol:
        df[col] = df[col].replace("nc", 0)  
       
    df = df[df.Département  != 'France métropolitaine']
    df = df[df.Département  != 'France entière']
    df.fillna(0, inplace=True)
    #print(df.tail(2)) 
    return df

# On s'intéresse aux données des médecins à part entière (APE)
# On renvoie les dépassements d'honoraires et d'autres données pour les métrics
def genererDonnesMedecinsAPE():
    
    # densité des médecins
    df_DensiteMedecinsParDept = pd.read_excel("Patientele_des_medecins_APE_en_2014.xls",\
                       sheetname=2, skiprows=3)
                           # on enlève les lignes qui calculent les sous-totaux
    df_DensiteMedecinsParDept = cleanData(df_DensiteMedecinsParDept)
    df_DensiteMedecinsParDept.to_csv("df_DensiteMedecinsParDept.csv")
    
    # densité des patients
    df_PatienteleAPE = pd.read_excel("Patientele_des_medecins_APE_en_2014.xls",sheetname="Patientèle", skiprows=3)
    df_PatienteleAPE = cleanData(df_PatienteleAPE)
     
    # honoraires totaux
    df_HonorairesTotaux = pd.read_excel("Patientele_des_medecins_APE_en_2014.xls",sheetname="Honoraires totaux par patient", skiprows=3)
    df_HonorairesTotaux = cleanData(df_HonorairesTotaux) 
    df_HonorairesTotaux.to_csv("df_HonorairesTotaux.csv")                   

    # honoraires sans dépassement
    df_HonorSansDepass = pd.read_excel("Patientele_des_medecins_APE_en_2014.xls",sheetname="HSD par patient", skiprows=3)
    df_HonorSansDepass = cleanData(df_HonorSansDepass)
    df_HonorSansDepass.to_csv("df_HonorSansDepass.csv")

    df_NombreActesPatients = pd.read_excel("Patientele_des_medecins_APE_en_2014.xls",sheetname="Nombre d'acte par patient", skiprows=3)
    df_NombreActesPatients = cleanData(df_NombreActesPatients)

    #return df_HonorAvecDepass, df_MedecinsAPE, df_PatienteleAPE, df_HonorairesTotaux, df_HonorSansDepass, df_NombreActesPatients
    return  df_DensiteMedecinsParDept, df_PatienteleAPE, df_HonorairesTotaux, df_HonorSansDepass, df_NombreActesPatients
  
     
df_MedecinsAPE, df_PatienteleAPE, df_HonorairesTotaux, df_HonorairesSansDepassement, df_NombreActesPatients \
= genererDonnesMedecinsAPE()

def calculerDepassHonoraires(df1, df2):
        # calcul des dépassements d'honoraires
    df = df1
    for col in listCol:
        df[col] =  df1[col] - df2[col]
    df.to_csv("df_DepassHonorairesParDeptParSpecialite.csv")
    return df
    
df_HonorAvecDepass = calculerDepassHonoraires(df_HonorairesTotaux, df_HonorairesSansDepassement)

def genererDensityPopulation():
    
    # on enlève les lignes d'en-tête du fichier
    df = pd.read_excel("Effectif_et_densite_par_departement_en_2014.xls", sheetname=3)
    # on enlève les lignes qui calculent les sous-totaux
    df = df[df.DEPARTEMENT != 'TOTAL FRANCE METROPOLITAINE']
    df = df[df.DEPARTEMENT != 'TOTAL OUTRE-MER']
   
    return df
  
df_DensitePop = genererDensityPopulation()   
# on enlève les doublons
df_DensitePop =  df_DensitePop[["DEPARTEMENT", "POPULATION FRANCAISE"]].drop_duplicates()

# renommage de la colonne pour un merge
df_DensitePop.rename(columns={"DEPARTEMENT":"Département"}, inplace=True) 

#metrics
df_merge_metrics = df_DensitePop.merge(df_HonorAvecDepass)
df_merge_metrics.to_csv("DfDepassementHonorairesPourMetrics.csv")


# Quelle spécialité fait le plus de dépassement ?
print(df_merge_metrics.describe())
# Réponse : "Psychiatrie"

# Dans quel département y a-t-il le plus de dépassements ?
dep_par_dep = df_merge_metrics.groupby("Département")[arrayCol].sum()
print(dep_par_dep)