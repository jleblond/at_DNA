from atdna_comp import AtDNAComp


dna_comparison = AtDNAComp('test_genome_1.txt', '23am', 'test_genome_2.txt', '23mf')
print(f"***** Total of SNPs is {dna_comparison.total_snps} *****")
result_df = dna_comparison.comparison_df
print(f"List of chromosomes: {dna_comparison.list_chromosomes}")
dna_comparison.mark_shared_alleles()
dna_comparison.mark_consecutive_shared()
dna_comparison.regroup_shared_segments()
