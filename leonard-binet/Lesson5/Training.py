
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:

df = pd.read_csv("rpps_tab3.csv", encoding="utf-8")


# In[3]:

df.head(5)


# In[4]:

df.mode_exercice.unique()


# In[5]:

df.shape


# In[6]:

# on va prendre uniquement les informations par région, c'est à dire les lignes pour
# lesquelles la zone d'inscription commence par une lettre maj puis une
# lettre min
df_clean = df[df.zone_inscription.str.match("^[A-Z][a-z]")]


# In[7]:

df_clean.zone_inscription.unique()


# In[8]:

groupby_region = df_clean.groupby("zone_inscription").effectifs.sum()
print(groupby_region)


# In[9]:
plt.figure()
plt.plot(groupby_region)
# groupby_region.plot.bar()
plt.show()

# In[10]:

df_pop = pd.read_csv("CLEAN_pop.csv", delimiter=";", encoding="utf-8")
print(df_pop.head(5))
print(df_pop.shape)


# In[11]:

long_pop = pd.melt(df_pop, id_vars=["REGION"])
print(long_pop.shape)
# on a s'intéresser pour l'instant uniquement à la population totale par région, on verra ensuite si cela a un
# intérêt de voir par sexe et par tranche d'âge
long_total_pop = long_pop[long_pop.variable == "Total"][["REGION", "value"]]
print(long_total_pop)


# In[12]:


# on met les régions en lower case et on enlève les accents
long_total_pop.REGION = long_total_pop.REGION.str.title()
long_total_pop.REGION = long_total_pop.REGION.str.strip()
long_total_pop.REGION = long_total_pop.REGION.str.replace("'", "")
long_total_pop.REGION = long_total_pop.REGION.str.replace("", "")
long_total_pop.REGION = long_total_pop.REGION.str.replace("ô", "o")
long_total_pop.REGION = long_total_pop.REGION.str.replace("Î", "I")
long_total_pop.REGION = long_total_pop.REGION.str.replace(" - ", "-")
long_total_pop.REGION = long_total_pop.REGION.str.replace("  ", "-")
long_total_pop.REGION = long_total_pop.REGION.str.replace(" ", "-")
long_total_pop.value = long_total_pop.value.str.replace('\xa0', '')

groupby_region.index = groupby_region.index.str.title()
groupby_region.index = groupby_region.index.str.strip()
groupby_region.index = groupby_region.index.str.replace("\u0092", "")
groupby_region.index = groupby_region.index.str.replace("ô", "o")
groupby_region.index = groupby_region.index.str.replace("’", "")
groupby_region.index = groupby_region.index.str.replace(" - ", "-")
groupby_region.index = groupby_region.index.str.replace("  ", "-")
groupby_region.index = groupby_region.index.str.replace(" ", "-")

long_total_pop = long_total_pop.set_index("REGION")
print(long_total_pop)
print(groupby_region)


# In[13]:

long_total_pop.value[0]


# In[14]:

long_total_pop["Medecins"] = groupby_region.astype(int)
print(long_total_pop)


# In[15]:

# print(long_total_pop.index.values[20].encode("utf-8"))
print(groupby_region.index.values[25])
print(groupby_region.index.values[25].replace("\u0092", "").encode("utf-8"))
print(groupby_region.index.values[25].encode("utf-8"))


# In[16]:

clean_data = long_total_pop.dropna()


# In[17]:

print(clean_data)


# In[30]:

clean_data.columns = ["Population", "Médecins", "Ratio"]
clean_data.Population.astype(int)
clean_data["Ratio"] = clean_data.apply(
    lambda x: x.Médecins / x.Population * 100, axis=1)
print(clean_data.Population.dtype)


# In[31]:

print(clean_data)


# In[41]:

test = pd.qcut(clean_data.Ratio, 5)
print(test)
print(test.values.unique)


# In[ ]:
