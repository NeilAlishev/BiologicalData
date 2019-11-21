# Work progress

**Guys, please update this file with all the neccessary information (what you've done) after you do something new in the project. This will be useful for writing final report.**

1) "Retrieve homologous proteins in UniProt starting from the input sequence provided."

I've done BLAST search on this page (https://www.uniprot.org/blast/). I've provided our sequence (EAAYDFPGSGSSSELPLKKGDIVFISRDEPSGWSLAKLLDGSKEGWVPT) as an input for BLAST. I've used BLOSUM-62 substitution matrix and uniprotkb_human database. E-Threshold value was set to 10 (this value is relatively big, but we have a small target protein sequence, so it's acceptable).

I've got 190 sequences in the result and I've downloaded them as a FASTA file (BLAST_uniprot.fasta).

2) "Generate a multiple sequence alignment (MSA). If necessary, (manually) edit rows and columns."

I've generated MSA from BLAST_uniprot.fasta using Clustal Omega (https://www.uniprot.org/align/). I didn't manually edit anything.
I've downloaded MSA in FASTA format (MSA_uniprot.fasta) and in Jalview format (MSA_uniprot.jvl).

3) "Build a PSSM model starting from the MSA using BLAST."

I've used the following command:

```
# Create a PSSM from a Fasta MSA (the content of the file in the -subject option is irrelevant)
psiblast -subject BLAST_uniprot.fasta -in_msa MSA_uniprot.fasta -out_pssm MSA_uniprot_model.pssm
```

Resulting file is: MSA_uniprot_model.pssm

4) "Build a HMM model starting from the MSA using HMMER."

I've use the following command:

```
# Build a HMM from the MSA with hmmbuild
hmmbuild MSA_uniprot_model.hmm MSA_uniprot.fasta
```

Resulting file is: MSA_uniprot_model.hmm