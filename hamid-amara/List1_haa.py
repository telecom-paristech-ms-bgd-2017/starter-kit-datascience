
# coding: utf-8

# In[35]:

def match_ends(words):
  # +++your code here+++
    n=0
    for num in words:
        if (len(num)>2 and num[0]==num[-1]):
            n+=1
    return(n)

anim=["chat","choc","bob","il","dilid"]
nb=match_ends(anim)
print ("nb de mots avec premières lettre et dernière id :",nb)
              
    


# In[39]:

anim=["chat","choc","bob","il","dilid"]
nb=match_ends(anim)
print ("nb de mots avec premières lettre et dernière id :",nb)


# In[ ]:



