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
psiblast -subject BLAST_uniprot.fasta -in_msa MSA_uniprot_edited.fasta -out_pssm models/MSA_uniprot_model.pssm
```

**OUTPUT:** MSA_uniprot_model.pssm


#### 4) "Build a HMM model starting from the MSA using HMMER."

I've use the following command:

```
# Build a HMM from the MSA with hmmbuild
hmmbuild models/MSA_uniprot_model.hmm MSA_uniprot_edited.fasta
```

**OUTPUT:** MSA_uniprot_model.hmm

#### 5) "Evaluate your model against human proteins available in SwissProt (accuracy, precision, sensitivity, specificity, MCC)."

##### a) Define you ground truth/reference by finding all human proteins in SwissProt annotated (and not annotated) with the assigned Pfam ID (provided). Pfam annotations are available from UniProt.

To obtain all human proteins containing our domain we have searched Uniprot with query:
```
pf00018 AND reviewed:yes AND organism:"Homo sapiens (Human) [9606]"
```
and found out that there are 101 proteins.

**OUTPUT:** Swiss_Human/PF00018_human.fasta

We then downloaded all human protein from SwissProt:
```
reviewed:yes AND organism:"Homo sapiens (Human) [9606]"
```
**OUTPUT:** Swiss_Human/Swiss_human.fasta

##### b) "Find significant hits using HMM-SEARCH and PSI-BLAST respectively for the HMM and PSSM model"

We have then created the database with the following command
```
makeblastdb -dbtype prot -in Swiss_Human/Swiss_human.fasta -parse_seqids
```

Search with psiblast using the previously generated PSSM
```
psiblast -in_pssm models/MSA_uniprot_model.pssm -db Swiss_Human/Swiss_human.fasta  -num_iterations 1 -evalue 0.001 > results/psiblast_out.txt
```

Search with hmmsearch using the previously generated HMM
```
hmmsearch --domtblout results/hmmsearch.hmmer_domtblout models/MSA_uniprot_model.hmm Swiss_Human/Swiss_human.fasta > results/hmmsearch_out.hmmer_align
```

##### c) "Evaluate the ability of retrieving proteins with that domain"


## Domain family characterization

### Dataset definitions

The results are in the folder `Dataset`

#### Original dataset

We used the HMM to retrieve the proteins from the SwissProt human database

#### Architecture dataset
We retrieved Pfam domains of all human proteins in SwissProt from Uniprot, we then filtered the proteins matching the ones in our original dataset and created, for each possible domains combination, a new dataset containing the proteins made up by that combination.

The code is in  `Architecture_datasets.ipynb`

#### PDB network

Starting from the original dataset we retrieved the PDB entries for each protein, we did the same thing for
all the proteins present in the SwissProt database. Not all the human proteins in Uniprot, because its rare to find
a protein which has a PDB entry and it's not in SwissProt.

We then added all the proteins not present in the original database which are found as other chains in the same PDB.

The code is in `PDB_dataset.ipynb`

#### STRING network

From **string-db.org** we chosen the multiple sequences mode, then copied all the Uniprot id of the proteins in the original dataset in the form.
Then we downloaded it in fasta format (`string_protein_sequences.fasta`), and then with `string_dataset.ipynb` we retrieved all the STRING ids and with `uniprot.org` we translated it into Uniprot ids.

From uniprot we downloaded the proteins in fasta format `string_converted.fasta`. Finally with python we added all the new proteins not
present in the original dataset that interact with one of the proteins in the original dataset.


## Structural classification

"Provide a statistics about the CATH architectures mapping to your domain."

We went to CATH db and searched for our domain - PF00018. We found out that our domain is formed by one architecture - Roll (CATH ID: 2.30). Apart from our domain, this acrhiteture is also present in 9827 other domains.

"Retrieve all PDBs covering your domain (if any) and evaluate their structural similarity."

We retrieved from PDB all structures that cover our domain (PF00018) and that belong to Homo Sapiens organism. 128 such structures were found and downloaded as .pdb files.
Then we've created a script which performs all-vs-all structural alignment using TM-align command line software.
This resulted in 8128 alignment files. Then, we retrieved TM-score (normalized by average length of chains) from each of these files and constructed 2D distance matrix for all pairs of structures.
From this 2D matrix we created 2 dendograms using 2 methods - Nearest point algorithm and UPGMA.
All results can be found in folder pdb_structural_similarity (file TMAlign.ipynb).