
# coding: utf-8

# In[ ]:




# In[12]:

def string_times(string, n):
    return (n*string)

a=string_times("damien",2)
print ('nouvelle chaine : ' + a)


# In[13]:

import unittest
# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )
        

def main():
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

if __name__ == '__main__':
    main()


# In[ ]:



