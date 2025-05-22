import os
import re
import sys

def print_help():
    """Print help information and exit."""
    print("""This script was designed to count the number of heme-binding motifs in protein sequences (in fasta format). It counts the number of heme-binding motifs in a non-overlapping manner and is able to count the canonical Cx2CH heme-binding motif and alternative variants:
CxCH
CxCK
Cx2CK
Cx3CH
Cx4CH
Cx11CH
Cx14CH
Cx15CH
Cx17CH
where "x" represents any given amino acid

⚙️ Usage: python heme_binding_motif_counter.py [path/to/file_or_folder]

📥 Input:
- A single .faa or .fasta file, or a directory containing such files.

📤 Output:
- Matched_positions.txt: Positions and motif types found in each sequence.
- Counts.txt: Number of heme-binding motifs found per protein sequence.

🔧 Example:
python heme_binding_motif_counter.py ./proteins/

If you experience any issue, please contact: ricardosoares@itqb.unl.pt or louro@itqb.unl.pt
""")
    sys.exit(0)

def process_protein_files(input_path):
    patterns = [
        r'C..CH',  # Cx2CH
        r'C..CK',  # Cx2CK
        r'C.C[HK]',    # CxCH or CxCK
        r'C.{3}CH',    # Cx3CH
        r'C.{4}CH',    # Cx4CH
        r'C.{11}CH',   # Cx11CH
        r'C.{14}CH',   # Cx14CH
        r'C.{15}CH',   # Cx15CH
        r'C.{17}CH'    # Cx17CH
    ]
    
    # Determine if input is a file or directory
    if os.path.isfile(input_path):
        files = [input_path]
        base_dir = os.path.dirname(input_path) or "."
    else:
        base_dir = input_path
        files = []
        for root, dirs, filenames in os.walk(base_dir):
            for filename in filenames:
                if filename.lower().endswith(('.fasta', '.faa')):
                    files.append(os.path.join(root, filename))
    
    if not files:
        print("No .fasta or .faa files found in the specified path.")
        sys.exit(1)
    
    output_file = os.path.join(base_dir, "Matched_positions.txt")
    counts_file = os.path.join(base_dir, "Counts.txt")
    
    with open(output_file, 'w') as output, open(counts_file, 'w') as counts_output:
        for file_path in files:
            with open(file_path, 'r') as f:
                seq_id = ""
                sequence = ""
                for line in f:
                    if line.startswith(">"):
                        # Process the previous sequence
                        if sequence:
                            total_matches = process_sequence(seq_id, sequence, patterns, output)
                            counts_output.write(f"{seq_id}: {total_matches}\n")
                        seq_id = line.strip()[1:].split()[0]  # Take only the first part of the header
                        sequence = ""
                    else:
                        sequence += line.strip()

                # Process the last sequence
                if sequence:
                    total_matches = process_sequence(seq_id, sequence, patterns, output)
                    counts_output.write(f"{seq_id}: {total_matches}\n")

def process_sequence(seq_id, sequence, patterns, output):
    """Find and write pattern matches for a given sequence and return total matches."""
    match_positions = {}  # Store positions of matches
    total_matches = 0
    
    # First find all matches and check for overlaps
    for pattern in patterns:
        matches = [(match.start(), match.end()) for match in re.finditer(pattern, sequence)]
        for start, end in matches:
            # Check if the match overlaps with any previous matches
            overlap = any(start < prev_end and end > prev_start for prev_start, prev_end in match_positions)
            if not overlap:
                match_positions[(start, end)] = pattern
                total_matches += 1
    
    # Write matched positions
    for (start, end), pattern in match_positions.items():
        output.write(f"Sequence ID: {seq_id}\tPattern: {pattern}\tMatch Position: {start}-{end}\n")
    
    return total_matches

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ['-h', '--help']:
        print_help()
    
    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Error: Path '{input_path}' does not exist.")
        sys.exit(1)
    
    process_protein_files(input_path)
    print("Processing completed. Results saved in Matched_positions.txt and Counts.txt")
