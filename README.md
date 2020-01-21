# Work progress

**Guys, please update this file with all the necessary information (what you've done) after you do something new in the project. This will be useful for writing final report.**

#### 1) "Retrieve homologous proteins in UniProt starting from the input sequence provided."

We've done BLAST search on this page (https://www.uniprot.org/blast/), providing our sequence (EAAYDFPGSGSSSELPLKKGDIVFISRDEPSGWSLAKLLDGSKEGWVPT) as input. We've used BLOSUM-62 substitution matrix and Uniref90 database. E-Threshold value was set to 0.01.

**OUTPUT:** BLAST_uniprot.fasta


#### 2) "Generate a multiple sequence alignment (MSA). If necessary, (manually) edit rows and columns."

I've generated MSA from BLAST_uniprot.fasta using Clustal Omega (https://www.uniprot.org/align/).

**OUTPUT:** MSA_uniprot.fasta

The MSA was then manually edited.

**OUTPUT:** MSA_uniprot_edited.fasta


#### 3) "Build a PSSM model starting from the MSA using BLAST."

I've used the following command:

```
# Create a PSSM from a Fasta MSA (the content of the file in the -subject option is irrelevant)
psiblast -subject BLAST_uniprot.fasta -in_msa MSA_uniprot_edited.fasta -out_pssm MSA_uniprot_model.pssm
```

**OUTPUT:** MSA_uniprot_model.pssm


#### 4) "Build a HMM model starting from the MSA using HMMER."

I've use the following command:

```
# Build a HMM from the MSA with hmmbuild
hmmbuild MSA_uniprot_model.hmm MSA_uniprot_edited.fasta
```

**OUTPUT:** MSA_uniprot_model.hmm
