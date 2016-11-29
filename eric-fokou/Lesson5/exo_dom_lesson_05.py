

import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



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


        ax = plt.gca()
        ax.legend_ = None
        #DONNEES - Densite de medecins pour 100.000 habitants
        plt.xlabel('densite de medecins pour 100.000 habitants'), plt.ylabel('depassement/(sans depass + depass)')
        plt.tight_layout()
        plt.show()


