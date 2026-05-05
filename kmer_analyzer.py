import sys
def validate_sequence(sequence, k):
    """
    Validates whether a DNA sequence is suitable for kmer analysis.
    
    Parameters:
        sequence (str): A string representing a DNA sequence
        k (int): The length of the kmer
    
    Returns:
        bool: True if the sequence is valid, False otherwise
    """
    if len(sequence) < k:
        return False
    for nucleotide in sequence:
        if nucleotide in '1234567890':
            return False
    return True

def update_kmer_count(kmer_data, kmer, next_char):
    """
    Updates the kmer dictionary with a new occurrence of a kmer and its following character.
    
    Parameters:
        kmer_data (dict): Dictionary storing kmer counts and next character frequencies
        kmer (str): The kmer string to update
        next_char (str): The character that follows the kmer in the sequence
    
    Returns:
        dict: Updated kmer_data dictionary
    """
    if kmer not in kmer_data:
        kmer_data[kmer] = {'count': 1, 'next_chars': {}}
    
    kmer_data[kmer]['count'] += 1
    
    if next_char not in kmer_data[kmer]['next_chars']:
        kmer_data[kmer]['next_chars'][next_char] = 0
    kmer_data[kmer]['next_chars'][next_char] += 1

    return kmer_data

def count_kmers_with_context(sequence, k):
    """
    Extracts all kmers and their following characters from a DNA sequence.
    
    Parameters:
        sequence (str): A valid DNA sequence string
        k (int): The length of each kmer
    
    Returns:
        dict: Dictionary containing kmer counts and next character frequencies
    """
    kmer_data = {}
    
    for i in range(len(sequence) - k):
        kmer = sequence[i:i+k]
        next_char = sequence[i+k]
        
        kmer_data = update_kmer_count(kmer_data, kmer, next_char)
    
    return kmer_data


def write_results_to_file(kmer_data, output_filename):
    """
    Writes kmer counts and next character frequencies to an output file.
    
    Parameters:
        kmer_data (dict): Dictionary containing kmer counts and next character frequencies
        output_filename (str): Path to the output file
    
    Returns:
        None
    """
    sorted_kmers = sorted(kmer_data.keys())
    
    with open(output_filename, 'w') as f:
        for kmer in sorted_kmers:
            next_chars = kmer_data[kmer]['next_chars']
            
            next_char_str = " ".join(
                f"{char}:{freq}" 
                for char, freq in sorted(next_chars.items())
            )
            
            f.write(f"{kmer} {next_char_str}\n")


def main():
    """
    Main function that reads sequences from a file and writes kmer analysis to output file.
    
    Parameters:
        None
    
    Returns:
        None
    """
    sequence_file = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]
    
    print(f"Reading sequences from {sequence_file}...")

    with open(sequence_file, 'r') as f:
        for sequence in f:
            sequence = sequence.strip()

            if not validate_sequence(sequence, k):
                print(f"  Warning: Skipping sequence")
                continue
            
            kmer_data = count_kmers_with_context(sequence, k) 
            
            write_results_to_file(kmer_data, output_file)

if __name__ == '__main__':
    main()
