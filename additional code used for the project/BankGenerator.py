import sys
import FeatureExtractor
import csv
from csv import reader

KEY = "key"
VALUES = "values"


def import_feature_to_bank():
    dict_map = FeatureExtractor.bins
    w = csv.writer(open("data/problemBank.csv", "w"))
    for key, val in dict_map.items():
        w.writerow([key, val])


def update_feature_metrics():
    # open file in read mode
    csv.field_size_limit(sys.maxsize)
    with open('data/problemBank.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            print(row[0])


def main():
    update_feature_metrics()


if __name__ == '__main__':
    main()
