#!/usr/bin/python -tt

import string
import sys

def countWord(filename):
    f = open(filename, 'rU')
    s = ''
    dico = {}
    for line in f:
        s +=line
    f.close()
    exclude = set(string.punctuation)
    cleaned = ''.join(ch for ch in s if ch not in exclude).lower().replace('\n', ' ').replace('\r', '').replace('\xc3\xa0','')
    s = cleaned.split(" ")
    s = [i for i in s if i != '']
    for word in s:
        if word not in dico:
            dico[word] = 1
        else :
            dico[word] += 1
    return dico

def print_words(dico):
    for word in dico.keys():
        print(word +" "+str(dico[word]))
def get_c(wordAndCount):
    return wordAndCount[1]

def print_top(dico):
    counts = sorted(dico.items(),key = get_c, reverse = True)
    for count in counts[:20]:
        print(count[0], count[1])

def main():
  if len(sys.argv) != 3:
     print ('usage: ./wordcount.py {--count | --topcount} file')
     sys.exit(1)

  option = sys.argv[1]
  filename = sys.argv[2]
  if option == '--count':
    dico = countWord(filename)
    print_words(dico)
  elif option == '--topcount':
    dico = countWord(filename)
    print_top(dico)
  else:
    print('unknown option: ' + option)
    sys.exit(1)

if __name__ == '__main__':
  main()
