from pandas import pandas as pd
from atdna_data import AtDNAData
from chromosome import Chromosome

STANDARD_HEADER_LIST = ["rsid", "chromosome", "position", "genotype"]
MIN_SNP_CONSECUTIVES = 2
RATIO_REGROUP_SEGMENTS = 10


class AtDNAComp():
    def __init__(self, first_file_path, first_csrc, second_file_path, second_csrc):
        self.first_dna_data = AtDNAData(first_file_path, first_csrc)
        self.second_dna_data = AtDNAData(second_file_path, second_csrc)

        AtDNAComp.standardize_headers(self.first_dna_data)
        AtDNAComp.standardize_headers(self.second_dna_data)

        self.comparison_df = AtDNAComp.merge_dataframes(self.first_dna_data.dataframe, self.second_dna_data.dataframe)
        self.chromosomes = {}

    @classmethod
    def standardize_headers(cls, dna_data_obj):
        dna_data_obj.dataframe.rename(columns={dna_data_obj.file_header[0]: STANDARD_HEADER_LIST[0],
                                    dna_data_obj.file_header[1]: STANDARD_HEADER_LIST[1],
                                    dna_data_obj.file_header[2]: STANDARD_HEADER_LIST[2],
                                    dna_data_obj.file_header[3]: STANDARD_HEADER_LIST[3]
                                    }, inplace=True)
    @classmethod
    def merge_dataframes(cls, first_dataframe, second_dataframe):
        df_merged = pd.merge(first_dataframe, second_dataframe, how='inner', on=['rsid', 'chromosome', 'position'])
        df_merged.sort_values(by=['chromosome', 'position'], ascending=True)
        return df_merged.assign(hi=0, fi=0, consecutive=0)

    def mark_shared_alleles(self):
        df = self.comparison_df
        for i, row in df.iterrows():
            genotype_1 = row[3]
            genotype_2 = row[4]
            if genotype_1 != '--' and genotype_2 != '--':
                if genotype_1 == genotype_2:
                    df.at[i, 'fi'] = 1
                elif set(genotype_1) & set(genotype_2):
                    df.at[i, 'hi'] = 1

    def mark_consecutive_shared(self):
        for chromosome in self.list_chromosomes:
            df_chromo = self.comparison_df[(self.comparison_df.chromosome == chromosome)]

            counter = 0
            last_starting_position = 0
            list_shared_segments = []
            for i, row in df_chromo.iterrows():
                sharing_value = row[5] or row[6]
                if sharing_value == 1:
                    counter += 1
                else:
                    if i > 0 and counter >= MIN_SNP_CONSECUTIVES:
                        df_chromo.at[i - 1, 'consecutive'] = counter
                        list_shared_segments.append([last_starting_position, row[2]])
                    counter = 0  # reset counter

                if counter == 1:
                    last_starting_position = row[2]

            self.chromosomes[chromosome] = Chromosome(name=chromosome,
                                                      dataframe=df_chromo,
                                                      count_hi=len(df_chromo[(df_chromo.hi == 1)]),
                                                      count_fi=len(df_chromo[(df_chromo.fi == 1)]),
                                                      length=len(df_chromo.index),
                                                      max_consecutives=df_chromo['consecutive'].max(),
                                                      shared_segments = list_shared_segments,
                                                      cleaned_shared_segments=list_shared_segments.copy(),
                                                      )


    def regroup_shared_segments(self):
        for cname in self.list_chromosomes:
            chromo = self.chromosomes[cname]

            for i, [start_pos, end_pos] in enumerate(chromo.cleaned_shared_segments):
                if i >= 1:
                    segment_distance = start_pos - last_end_pos
                    if segment_distance < (end_pos - start_pos)/RATIO_REGROUP_SEGMENTS \
                            and segment_distance < (last_end_pos - last_start_pos)/RATIO_REGROUP_SEGMENTS:
                        chromo.cleaned_shared_segments[i] = [chromo.cleaned_shared_segments[i-1][0], end_pos]
                        chromo.cleaned_shared_segments[i - 1] = None

                last_start_pos = start_pos
                last_end_pos = end_pos

            chromo.cleaned_shared_segments = list(filter(None, chromo.cleaned_shared_segments))

        print(self.chromosomes, sep='\n')



    @property
    def total_snps(self):
        #TODO: throw error if not self.comparison_df
        return len(self.comparison_df.index)

    @property
    def list_chromosomes(self):
        #TODO: throw error if not self.comparison_df
        list_all_chrs = self.comparison_df['chromosome'].unique().tolist()
        return [x for x in list_all_chrs if x not in ('X', 'Y', 'MT')]
        # return ['21']
