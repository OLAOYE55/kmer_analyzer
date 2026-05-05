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
    # Check if sequence is long enough to contain at least one kmer
    if len(sequence) < k:
        return False
    # Check each character to ensure it is a valid nucleotide
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
    # If this kmer hasn't been seen before, initialize its entry
    if kmer not in kmer_data:
        kmer_data[kmer] = {'count': 1, 'next_chars': {}}
    
    # Increment the total count for this kmer
    kmer_data[kmer]['count'] += 1
    
    # If this next character hasn't been seen after this kmer, initialize it
    if next_char not in kmer_data[kmer]['next_chars']:
        kmer_data[kmer]['next_chars'][next_char] = 0
    # Increment the count for this next character
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
    # Initialize empty dictionary to store kmer data
    kmer_data = {}
    
    # Loop through sequence, stopping before the last kmer (no next char after it)
    for i in range(len(sequence) - k):
        # Extract kmer of length k starting at position i
        kmer = sequence[i:i+k]
        # Get the character immediately following the kmer
        next_char = sequence[i+k]
        
        # Update the kmer dictionary with this kmer and its next character
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
    # Sort kmers alphabetically for consistent output
    sorted_kmers = sorted(kmer_data.keys())
    
    # Open output file for writing
    with open(output_filename, 'w') as f:
        for kmer in sorted_kmers:
            next_chars = kmer_data[kmer]['next_chars']
            
            # Format next character frequencies as "char:freq" pairs
            next_char_str = " ".join(
                f"{char}:{freq}" 
                for char, freq in sorted(next_chars.items())
            )
            
            # Write kmer and its next character frequencies to file
            f.write(f"{kmer} {next_char_str}\n")

def main():
    """
    Main function that reads sequences from a file and writes kmer analysis to output file.
    
    Parameters:
        None
    
    Returns:
        None
    """
    # Get command line arguments
    sequence_file = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]
    
    print(f"Reading sequences from {sequence_file}...")

    # Open and read each sequence from the input file
    with open(sequence_file, 'r') as f:
        for sequence in f:
            # Remove whitespace and newline characters
            sequence = sequence.strip()

            # Skip invalid sequences
            if not validate_sequence(sequence, k):
                print(f"  Warning: Skipping sequence")
                continue
            
            # Count kmers and their following characters
            kmer_data = count_kmers_with_context(sequence, k) 
            
            # Write results to output file
            write_results_to_file(kmer_data, output_file)

if __name__ == '__main__':
    main()
