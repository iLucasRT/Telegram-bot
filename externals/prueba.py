import csv

tokensid = {}
tokens = {}
with open('tokens_db.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        tokensid[row[1]] = row[0]
        tokens[row[1]] = row[2]
a = 'btc'
if a in tokensid:
    token = tokensid.get(a)
    token = token.lower()
    print(token)