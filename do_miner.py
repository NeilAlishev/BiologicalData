#!/usr/bin/env python
import requests
import json
import gzip
from tqdm import tqdm

# *** How can you find all articles associated to human proteins?

# Download all disease annotations from articles associated to human SwissProt entries
# The human_pubmed.tab.gz file can be created from the UniProt website by adding the Publications->PubMed ID
# column and downloading in "tab separated" format
if __name__ == '__main__':
    uniprot_pmid = {}  # { pmid : list_of_uniprot_ids }
    with gzip.open("res/human_pubmed.tab.gz") as f:
        for line in f:
            line = line.decode().strip().split("\t")
            if len(line) == 3:
                for pmid in line[2].split("; "):
                    uniprot_pmid.setdefault(pmid, []).append(line[0])

    inverted = {}
    for k, v in uniprot_pmid.items():
        if v[0] != 'Entry':
            for prot in v:
                inverted.setdefault(prot, []).append(k)

    # Parse the disease ontology
    do = {}  # { do_id : do_object }
    obj = {}  # { id: do_id, name: definition, xref: list_of_omim_ids, is_a: list_of_parents, is_obsolete: True }
    with open("res/doid.obo") as f:
        for line in f:
            line = line.strip().split(": ")
            if line and len(line) == 2:
                k, v = line
                if k == "id" and v.startswith("DOID:"):
                    obj["id"] = v.split(":")[1]
                elif k == "xref" and "OMIM" in v:
                    obj["omim"] = v.split(":")[1]
                elif k == "name":
                    obj["name"] = v
                elif k == "is_a":
                    obj.setdefault("is_a", []).append(v.split()[0].split(":")[1])
                elif k == "is_obsolete":
                    obj["is_obsolete"] = True
            else:
                if obj.get("id") and not obj.get("is_obsolete"):
                    do[obj["id"]] = obj
                obj = {}

    name_do = {}
    for k, v in do.items():
        name_do.setdefault(v['name'], k)

    # *** How can you find all disease annotations associated to human PubMed abstracts?

    diseases = {}  # { uniprot_id : list_of_diseases }
    pmids = list(uniprot_pmid.keys())
    URL = "https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds"
    for i in tqdm(range(0, len(pmids), 8)):
        params = {"articleIds": ",".join(["MED:{}".format(pmid) for pmid in pmids[i:i + 8]]), "type": "Diseases",
                  "section"   : "Abstract", "format": "JSON"}
        r = requests.get(URL, params=params)
        obj = json.loads(r.text)
        for ele in obj:
            for annotation in ele.get("annotations"):
                for uniprot_id in uniprot_pmid[ele["extId"]]:
                    if annotation["exact"] in name_do.keys():
                        DOID = name_do[annotation["exact"]]
                        diseases.setdefault(uniprot_id, set()).add(DOID)
    diseases = {k: list(v) for k, v in diseases.items()}
    json = json.dumps(diseases)
    f = open("datasets/uniprot_do.json", "w")
    f.write(json)
    f.close()
