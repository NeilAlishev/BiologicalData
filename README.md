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

#### 5) "Evaluate your model against human proteins available in SwissProt (accuracy, precision, sensitivity, specificity, MCC)."

##### a) Define you ground truth/reference by finding all human proteins in SwissProt annotated (and not annotated) with the assigned Pfam ID (provided). Pfam annotations are available from UniProt.

To obtain all human proteins containing our domain we have searched Uniprot with query:
```
pf00018 AND reviewed:yes AND organism:"Homo sapiens (Human) [9606]"
```
and found out that there are 101 proteins.

**OUTPUT:** Point5/PF00018_human.fasta

We then downloaded all human protein from SwissProt:
```
reviewed:yes AND organism:"Homo sapiens (Human) [9606]"
```
**OUTPUT:** Point5/Swiss_human.fasta

##### b) "Find significant hits using HMM-SEARCH and PSI-BLAST respectively for the HMM and PSSM model"

We have then created the database with the following command
```
makeblastdb -dbtype prot -in Point5/Swiss_human.fasta -parse_seqids
```

Search with psiblast using the previously generated PSSM
```
psiblast -in_pssm MSA_uniprot_model.pssm -db Point5/Swiss_human.fasta  -num_iterations 3 -evalue 0.001 > psiblast_out.txt
```

Search with hmmsearch using the previously generated HMM
```
hmmsearch --domtblout hmmsearch.hmmer_domtblout MSA_uniprot_model.hmm Point5/Swiss_human.fasta > hmmsearch_out.hmmer_align
```

##### c) "Evaluate the ability of retrieving proteins with that domain"
