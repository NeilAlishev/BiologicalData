import json
import pandas as pd

from Bio import SeqIO
from scipy.stats import fisher_exact
from matplotlib import pyplot as plt
from wordcloud import WordCloud

with open('datasets/do_files/enriched_do.json', 'r') as f:
    enriched_do = json.load(f)

with open('datasets/do_files/do_name.json', 'r') as f:
    do_name = json.load(f)

with open('datasets/do_files/do_depth.json', 'r') as f:
    do_depth = json.load(f)

with open('datasets/original.txt', 'r') as f:
    dataset = []
    for line in f:
        dataset.append(line[:-1])


def enrichment(domain, uniprot_ids):
    def DO_counts(dataset):
        term_counts = {}
        for uniprot_id, do_ids in enriched_do.items():
            if uniprot_id in dataset:  # if the protein is in the dataset passed to the function
                for id in do_ids:
                    term_counts.setdefault(id, 0)
                    term_counts[id] += 1
        return term_counts

    term_counts_dataset = DO_counts(uniprot_ids)
    num_do_dataset = sum(term_counts_dataset.values())

    term_counts_reference = DO_counts(dataset)
    num_do_reference = sum(term_counts_reference.values())

    key_intersection = set(term_counts_dataset.keys()).intersection(term_counts_reference.keys())

    # Measure enrichment performing a Fisher’s exact test (hypergeometric test).
    def p_value(do_terms_counter_dataset, num_do_dataset, do_terms_counter_human, num_do_human):
        p_values = {}
        for key in key_intersection:
            n_term = do_terms_counter_dataset[key]
            human_num = do_terms_counter_human[key]
            not_dataset = num_do_dataset - n_term
            not_human = num_do_human - human_num
            p_value = fisher_exact([[n_term, human_num], [not_dataset, not_human]])[1]
            p_values.setdefault(key, p_value)
        return p_values

    do_p_values = p_value(term_counts_dataset, num_do_dataset, term_counts_reference, num_do_reference)
    do_p_values = {k: v for k, v in sorted(do_p_values.items(), key=lambda item: item[1], reverse=False)}
    do_p_values = dict(filter(lambda v: v[1] < 0.1, do_p_values.items()))

    import numpy as np

    for key in do_p_values.keys():
        if key != '4':
            do_p_values[key] = (do_p_values[key], do_depth[key])
        else:
            do_p_values[key] = (do_p_values[key], 0)

    mean = np.mean([v[1] for v in do_p_values.values()])

    # do_p_values = dict(filter(lambda v: v[1][1] <= mean, do_p_values.items()))

    do_labeled_enriched = {}
    for k, v in do_p_values.items():
        do_labeled_enriched.setdefault(do_name[k], int(np.log(1 / v[0])))

    if len(do_labeled_enriched) == 0:
        do_labeled_enriched.setdefault("None", 1)

    wordcloud = WordCloud(max_font_size=200, max_words=289, width=3000, height=3000, background_color="white", scale=4)
    wordcloud.generate_from_frequencies(do_labeled_enriched)
    plt.figure(figsize=(20, 20))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.xticks([], [])
    plt.yticks([], [])
    plt.savefig('plot/do/wordcloud_architecture_{}.pdf'.format(domain))
    plt.axis("off")
    plt.close()


# some JSON:
with open('datasets/architecture_datasets.json') as json_file:
    data: dict = json.loads(json_file.read())

for k, v in data.items():
    k = k.replace(', ', '\\')
    k = k.replace(' ', '_')
    enrichment(k, v)
