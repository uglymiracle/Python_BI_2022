# Python_BI_2022

## Homework #2

The program can:
1. Filter reads by GC composition
2. Filter reads by quality
3. Filter reads by length

Arguments:
1. **input_fastq** - path to your file
2. **output_file_prefix** - prefix for filtered data
-- Satisfy the condition - 'prefix_passed.fastq'
-- Unfiltered sequences - 'prefix_failed.fastq'
3. **gc_bounds** - GC composition interval (in percent) for filtering (default is (0, 100), i.e. all reads are saved). If a single number is passed to the argument, then it is considered to be the upper bound.
4. **length_bounds** - length interval for filtering, default is (0, 2^32). If a single number is passed to the argument, then it is considered to be the upper bound.
5. **quality_threshold** - average read quality threshold for filtering, by default equals 0 (phred33 scale). Sequences with average quality below the threshold are discarded
6. **save_filtered** - whether to save filtered reads, default is False.

