import pytest
from kmer_analyzer import validate_sequence, update_kmer_count, count_kmers_with_context, write_results_to_file

def test_validate_sequence():
    # Test 1: valid sequence should return True
    assert validate_sequence("ATGC", 2) == True
    
    # Test 2: sequence shorter than k should return False
    assert validate_sequence("AT", 5) == False
    
    # Test 3: sequence with numbers should return False
    assert validate_sequence("ATG123", 2) == False
    
    # Test 4: sequence with invalid letters should return False
    assert validate_sequence("ATGX", 2) == False

def test_update_kmer_count():
    # Test 1: new kmer should have count of 1
    kmer_data = {}
    kmer_data = update_kmer_count(kmer_data, "AT", "G")
    assert kmer_data["AT"]["count"] == 1

    # Test 2: seeing the same kmer twice should give count of 2
    kmer_data = update_kmer_count(kmer_data, "AT", "G")
    assert kmer_data["AT"]["count"] == 2

    # Test 3: next character should be recorded correctly
    assert kmer_data["AT"]["next_chars"]["G"] == 2

    # Test 4: different next character should be recorded separately
    kmer_data = update_kmer_count(kmer_data, "AT", "C")
    assert kmer_data["AT"]["next_chars"]["C"] == 1

def test_count_kmers_with_context():
    # Test 1: correct number of kmers extracted
    result = count_kmers_with_context("ATGT", 2)
    assert len(result) == 2

    # Test 2: correct kmers are found
    assert "AT" in result
    assert "TG" in result

    # Test 3: correct next characters recorded
    assert "G" in result["AT"]["next_chars"]
    assert "T" in result["TG"]["next_chars"]

def test_write_results_to_file():
    # Set up some test kmer data
    kmer_data = {
        "AT": {"count": 2, "next_chars": {"G": 2}},
        "TG": {"count": 1, "next_chars": {"T": 1}}
    }
    
    # Write to a test output file
    write_results_to_file(kmer_data, "test_output.txt")
    
    # Read the file and check the contents
    with open("test_output.txt", "r") as f:
        lines = f.readlines()
    
    # Test 1: correct number of lines
    assert len(lines) == 2
    
    # Test 2: total count is included in output
    assert "2" in lines[0]
    
    # Test 3: next character frequencies are included
    assert "G:2" in lines[0]
