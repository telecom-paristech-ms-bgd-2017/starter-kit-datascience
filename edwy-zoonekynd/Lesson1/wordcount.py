def print_words(filename):
    f = open(filename)
    count = dict()
    lst = list()
    for line in f:
        line = line.lower()
        words = line.split()
        for word in words:
            if word not in count:
                count[word] = 1
            else:
                count[word] += 1
    for word, occ in count.items():
        lst.append((word, occ))

    return sorted(lst, key=lambda x: x[0])

f = print_words(
    "/Users/Edwy/GDrive/Telecom-Paristech/Kit Big Data INFMDI721/google-python-exercises/basic/small.txt")
print(f)

def print_top(filename):
    f = open(filename)
    count = dict()
    lst = list()
    for line in f:
        line = line.lower()
        words = line.split()
        for word in words:
            if word not in count:
                count[word] = 1
            else:
                count[word] += 1
    for word, occ in count.items():
        lst.append((word, occ))

    return sorted(lst, key=lambda x: x[1], reverse = True)[:5]

g = print_top(
    "/Users/Edwy/GDrive/Telecom-Paristech/Kit Big Data INFMDI721/google-python-exercises/basic/small.txt")
print(g)
