import sys
from operator import itemgetter

def count_words(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    allwords = {}
    for l in lines:
        for word in l.split():
            word = word.lower()
            if word in allwords:
                allwords[word] += 1
            else:
                allwords[word] = 1
    return allwords


def print_words(filename):
    allwords = count_words(filename)
    sortedallwords = sorted(allwords.keys())
    for word in sortedallwords:
        print(word + " " + str(allwords[word]))


def print_top(filename):
    allwords = count_words(filename)
    sortedallwords = sorted(allwords.items(), key=itemgetter(1), reverse=True)
    i = 0
    while i < 20:
        word = sortedallwords[i][0]
        print(word + " " + str(allwords[word]))
        i += 1


def main():

    option = input("count or topcount : ")
    filename = input("File name : ")

    if option == "count":
        print_words(filename)
    elif option == "topcount":
        print_top(filename)
    else:
        print("unknown option:" + option)
    sys.exit(1)


if __name__ == '__main__':
    main()



