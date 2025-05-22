# heme_binding_motif_counter
Repository for storing heme-binding motif counter

This script was designed to count the number of heme-binding motifs in protein sequences (in fasta format)


This script counts the number of heme-binding motifs in a non-overlapping manner and is able to count the canonical Cx2CH heme-binding motif and alternative variants:
CxCH,
CxCK,
Cx2CK,
Cx3CH,
Cx4CH,
Cx11CH,
Cx14CH,
Cx15CH,
Cx17CH,
where "x" represents any given amino acid

-Usage-: python heme_binding_motif_counter.py [path/to/file_or_folder]

📥 Input:
- A single .faa or .fasta file, or a directory containing such files.

📤 Output:
- Matched_positions.txt: Positions and motif types found in each sequence.
- Counts.txt: Number of heme-binding motifs found per protein sequence.

🔧 Example:
python heme_binding_motif_counter.py ./proteins/

If you experience any issue, please contact: ricardosoares@itqb.unl.pt or louro@itqb.unl.pt
