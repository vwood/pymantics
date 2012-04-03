#!/usr/bin/python

import bayes
import csv

# I fix the dataset by turning the continous variables into descrete by multiplying by 100

b = bayes.Bayes()
b.set_absent_is_missing(False)

test = []

spamdataset = csv.reader(open("spambase.data", 'rb'))
for i, row in enumerate(spamdataset):
    label = row[-1]
    data = [str(j) for j, item in enumerate(row[:-4]) if float(item) > 0]
    if i % 4 == 0:
        test.append((data, label))
    else:
        b.train(data, label)

print b.test(test)
    
