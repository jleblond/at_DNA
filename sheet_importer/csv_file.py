from pandas import pandas as pd
import csv


class CSVFile():
    def __init__(self, file_path, headers):
        self.file_path = file_path
        self.headers = headers
        self.errors = []
        self.dataframe = []
        self.header_number = 0
        self.valid = None


    def load(self):
        #TODO: check file name, file
        #TODO: check headers are set

        with open(self.file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                if row == self.headers:
                    self.header_number = reader.line_num - 1

        try:
            self.dataframe = pd.read_csv(self.file_path, sep='\t', header=self.header_number)
            self.valid = True
        except Exception as e:
            self.errors.append(e)
            self.valid = False