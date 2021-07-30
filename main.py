import csv


with open('covid19casos short.csv') as csvfile:
     csv_reader = csv.reader(csvfile, delimiter=',')
     for row in csv_reader:
         print(row)
