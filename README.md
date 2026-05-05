# kmer_analyzer

## Description
This script analyzes k-mers in DNA sequences. It reads sequence fragments 
from a file, counts the frequency of each k-mer, and records which character 
follows each k-mer.

## Usage
python kmer_analyzer.py <sequence_file> <k> <output_file>

## Arguments
- sequence_file: path to input file containing DNA sequences
- k: length of k-mer
- output_file: path to output file

## Requirements
- Python 3

## Example
python kmer_analyzer.py sequences.txt 2 output.txt

## Testing
Run tests using pytest:
pytest test_kmer_analyzer.py

## AI Use Statement
Claude (Anthropic) was used as an assistant during the development of this 
project. It helped explain confusing concepts and guide the work especially when I run into multiple errors in my code.
