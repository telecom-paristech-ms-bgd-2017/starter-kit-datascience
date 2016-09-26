def countMots():
    countWord = {}

    with open("./lesson1/DuTexte.txt", "r") as fichier:
        for line in fichier:
            listeMots = line.strip().split(" ")
            for mot in listeMots:
                if mot.lower() in countWord:
                    countWord[mot.lower()] += 1
                else:
                    countWord[mot.lower()] = 1

    motsTries = sorted(countWord.items(), key=lambda col: col[0])

    for mot in motsTries:
        print(mot[0] + " ! " + str(mot[1]))

    return countWord



def print_top():
    motsTriesParNombreApparitions = sorted(countMots().items(), key=lambda col: col[1], reverse=True)
    i = 0
    for mot in motsTriesParNombreApparitions:
        print(mot[0] + " ! " + str(mot[1]))
        i += 1
        if(i > 5):
            break


print_top()
