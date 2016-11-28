# -*- coding: utf-8 -*-


# Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire et la pratique du dépassement d'honoraires ? 

# Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire et la pratique du dépassement d'honoraires ? Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent le moins les dépassement d'honoraires ? Est ce que la densité de certains médecins / praticiens est corrélé à la densité de population pour certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?

#lien entre la densité de médecins par spécialité  et par territoire et la pratique du dépassement d'honoraires

import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Recuperation des données du fichier csv R2015
#    '/Users/Bense/Documents/Exercices/Charles/TP5/R2015_sans_lib/R201501_sanslib.CSV', delimiter=';')
#dataFrame_final_r2015 = pd.read_csv('rpps-medecins-tab7_36171637131987.csv', delimiter=',')

if 1:
    dataFrame_final_r2015 = pd.read_csv('density.csv', delimiter=',',skiprows=3,header=1)
    print dataFrame_final_r2015
    print "dataFrame_final_r2015"
    #raw_input()

file_name_honoraires = 'depass.csv'
df_depass = pd.read_csv(file_name_honoraires, delimiter=',', header = 0)
print df_depass
print "df_depass"
#raw_input()


print list(df_depass.columns.values)
#raw_input()
print '\n\n'
print list(dataFrame_final_r2015.columns.values)

import Levenshtein
string1 = 'dsfjksdjs'
string2 = 'dsfiksjsd'
print Levenshtein.distance(string1, string2)

#speciality=


col_dens=list(dataFrame_final_r2015.columns.values)
print col_dens

#######################################################################
#extraction de chaque specialité
print '\n coltitle \n '
for col_title in col_dens:
    print col_title
print '\n coltitle \n'
#print df_depass['SpĂ©cialistes']
s = df_depass.ix[:,0]
print s

df_dens=dataFrame_final_r2015
grouped_by_specialty_depass=df_depass.groupby(s)

#     grouped = df.groupby(get_nb_type, axis=0)
print '\n trope lent'

for key, item in grouped_by_specialty_depass:
    densities_per_speciality=[]
    ratio_depass_per_speciality=[]
    
    #print key
    specialty_depass=key
    #print 'key \n'
    #print df_dens['SPECIALITE']
    #print col_dens
    

    dist_lev=[Levenshtein.distance(key, spec_dens) for spec_dens in col_dens]
    #print np.min(dist_lev)
    #print departmt_depass
    #, "\n\n"
    M=np.min(dist_lev)
    spec_de_df_dens_le_plus_proche=[string2 for string2 in col_dens if M==Levenshtein.distance(key, string2) ]
    #print spec_de_df_dens_le_plus_proche
    
    #raw_input()
    if len(spec_de_df_dens_le_plus_proche)==1:
        specialty_dens=spec_de_df_dens_le_plus_proche[0]
        #specialty_depass=key

        #specialty_dens=spec_de_df_dens_le_plus_proche[0]
        #specialty_depass=key

        #departmt_dens=lestr_de_df_dens_le_plus_proche[0]
        #departmt_depass

        
        
        #print grouped_by_specialty_depass.get_group(key), "\n\n"
        # print len(grouped_by_specialty_depass.get_group(key))
        # print len(df_dens)

        # print grouped_by_specialty_depass.get_group(key)['DEPARTEMENT']
        # print 'departements'
        for departmt_depass in grouped_by_specialty_depass.get_group(key)['DEPARTEMENT']:
            print specialty_depass+'        *******************    '+ departmt_depass

            #dist=
            dist_lev=[Levenshtein.distance(departmt_depass, string2) for string2 in df_dens['SPECIALITE']]
            # print np.min(dist_lev)
            # print departmt_depass
            #, "\n\n"
            M=np.min(dist_lev)
            lestr_de_df_dens_le_plus_proche=[string2 for string2 in df_dens['SPECIALITE'] if M==Levenshtein.distance(departmt_depass, string2) ]
            #print lestr_de_df_dens_le_plus_proche
            if len(lestr_de_df_dens_le_plus_proche)==1:
                #on a bien trouvé un seul champ departement qui matche ce qui existe dans density et depasssement
                departmt_dens=lestr_de_df_dens_le_plus_proche[0]
                #departmt_depass
                
                #print key
                # print "\n grouped_by_specialty_depass(key) \n"
                #print grouped_by_specialty_depass.get_group(key)
                gb=grouped_by_specialty_depass.get_group(key)
                # print gb.loc[gb['DEPARTEMENT']==departmt_depass]
                # print "print gb.loc[gb['DEPARTEMENT']==departmt_depass]"
                right_depart_right_spec_depass=gb.loc[gb['DEPARTEMENT']==departmt_depass]
                #new_dfa=df_triche_better.loc[df_triche_better['Elevation']==3394]
                # print '\n'
                # print right_depart_right_spec_depass['DEPASSEMENTS (Euros)'].replace(',','')
                
                #print str(right_depart_right_spec_depass['DEPASSEMENTS (Euros)'].replace(',',''))
                # print '\n ********* \n '
                # print right_depart_right_spec_depass['DEPASSEMENTS (Euros)']
                # print '\n ********* \n '
                #                print (right_depart_right_spec_depass['DEPASSEMENTS (Euros)']=='nc').all()
                #                if right_depart_right_spec_depass['DEPASSEMENTS (Euros)']!='nc':
                if (right_depart_right_spec_depass['DEPASSEMENTS (Euros)']!='nc').all() :
                    s = pd.to_numeric(right_depart_right_spec_depass['DEPASSEMENTS (Euros)'].str.replace(' ', '').str.replace(',', ''))



                    # print s
                    # print np.float(s)
                    depassement=np.float(s)
                    # print 'lalala'
                    #raw_input()

                    #print np.float(right_depart_right_spec_depass['DEPASSEMENTS (Euros)'].replace(',',''))
                    # print "right_depart_right_spec_depass['DEPASSEMENTS (Euros)']"
                    # print np.float(right_depart_right_spec_depass['HONORAIRES SANS DEPASSEMENT (Euros)'].replace(',',''))
                    # print "right_depart_right_spec_depass['HONORAIRES SANS DEPASSEMENT (Euros)']"
                    s = pd.to_numeric(right_depart_right_spec_depass['HONORAIRES SANS DEPASSEMENT (Euros)'].str.replace(' ', '').str.replace(',', ''))
                    hon_sans_depassement=np.float(s)
                    if hon_sans_depassement*1.0+depassement!=0.0:
                        taux=depassement/(hon_sans_depassement*1.0+depassement)
                        # print taux
                        # print "taux"
                        #print 'key'
                        #raw_input()
                        ########################## depassement on cherche le depassement correspondant fait au dessus
                        ##### ci dessous on cherche la densité correspondante!

                        # print df_dens.loc[ df_dens['SPECIALITE']==departmt_dens]
                        # print "df_dens.loc[ df_dens['SPECIALITE']==departmt_dens]"
                        ligne_correcte_dens=df_dens.loc[ df_dens['SPECIALITE']==departmt_dens]
                        # print specialty_dens
                        # print '\n'

                        # print ligne_correcte_dens[specialty_dens]
                        # print "ligne_correcte_dens[specialty_dens]"
                        # print np.float(pd.to_numeric(ligne_correcte_dens[specialty_dens]))
                        density=np.float(pd.to_numeric(ligne_correcte_dens[specialty_dens]))

                        densities_per_speciality.append(density)
                        ratio_depass_per_speciality.append(taux)
    if len(densities_per_speciality)>2:
        #and len(ratio_depass_per_speciality)>1:
        r_pears=scipy.stats.pearsonr(densities_per_speciality,ratio_depass_per_speciality)

        fig = plt.figure(figsize=(8, 6))
        #plt.hist(cinq_cent_samples, bins=25, normed=True, align='mid')
        plt.plot(densities_per_speciality,ratio_depass_per_speciality,linestyle='None',marker='*')
        #sns.kdeplot(cinq_cent_samples, shade=True, color="b")

        #sns.kdeplot(panda_array_meres, shade=True, color='#9932cc')


        data= specialty_dens
        udata=data.decode("utf-8")
        specialty_dens_asciidata=udata.encode("ascii","ignore")
        #print specialty_dens_asciidata

        data= specialty_depass
        udata=data.decode("utf-8")
        specialty_depass_asciidata=udata.encode("ascii","ignore")
        #print specialty_depass_asciidata

        #    plt.title(' taux de depassement VS densite \n autre lgne'+ ' \n dens spec: '+specialty_dens+' \n depass spec :' +specialty_depass )
        plt.title(' taux de depassement VS densite'+ ' \n dens spec: '+specialty_dens_asciidata+' \n depass spec :' +specialty_depass_asciidata+' \n Pearson R = '+np.round(r_pears[0],5).__str__() +\
                  '\n p_value = '+np.round(r_pears[1],5).__str__() + '\n R >80%  '+(r_pears[0]>0.8).__str__())

        print 'comparer aux valeurs critiques : http://www.life.illinois.edu/ib/203/Fall%2009/PEARSONS%20CORRELATION%20COEFFICIENT%20TABLE.pdf'

        #data="UTF-8 DATA"
        #udata=data.decode("utf-8")
        #asciidata=udata.encode("ascii","ignore")


        #specialty_dens=spec_de_df_dens_le_plus_proche[0]
        #specialty_depass=key

        #departmt_dens=lestr_de_df_dens_le_plus_proche[0]
        #departmt_depass

        ax = plt.gca()
        ax.legend_ = None
        #DONNEES - Densite de medecins pour 100.000 habitants
        plt.xlabel('densite de medecins pour 100.000 habitants'), plt.ylabel('depassement/(sans depass + depass)')
        plt.tight_layout()
        plt.show()


        #densities_per_speciality.append(density)
        #ratio_depass_per_speciality.append(taux)

        #        raw_input()
                
print '\n\n je suis ... tres lent hahaha'

