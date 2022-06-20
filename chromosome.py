from dataclasses import dataclass
from pandas import DataFrame

@dataclass
class Chromosome():
    name: str
    dataframe: DataFrame
    count_hi: int
    count_fi: int
    length: int
    max_consecutives: int
    shared_segments: list
    cleaned_shared_segments: list


