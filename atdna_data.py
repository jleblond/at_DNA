from sheet_importer import file_importer

class AtDNAData():
    def __init__(self, file_path, csrc):
        self.file_path = file_path
        self.file_header = self.get_file_header_from_csrc(csrc)
        self.dataframe = file_importer.get_dataframe_from_csv(file_path, self.file_header)


    def get_file_header_from_csrc(self, csrc):
        if csrc == '23am':
            return ['# rsid', 'chromosome', 'position', 'genotype']
        elif csrc == '23mf':
            return ['#rsid', 'chromosome', 'position', 'genotype']
        else:
            pass
            #TODO: throw error
