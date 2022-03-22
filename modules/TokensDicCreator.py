import csv

def dicCreator():
    tokens = {}
    with open('../externals/tokens_db.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            tokens[row[1]] = row[2]
            print(tokens)
    return tokens

