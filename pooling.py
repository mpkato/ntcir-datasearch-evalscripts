import os
import re
import sys
import zipfile
import ujson as json
from collections import defaultdict
from argparse import ArgumentParser

SYSDESC = re.compile("<SYSDESC>(.*)</SYSDESC>")
JFILENAME = re.compile("-J-[0-9]{1,2}$")
EFILENAME = re.compile("-E-[0-9]{1,2}$")

FILENAME = re.compile("/([a-zA-Z]+)-(E|J)-([0-9]{1,2})$")

def get_language(filepath):
    if JFILENAME.search(filepath):
        lang = "J"
    elif EFILENAME.search(filepath):
        lang = "E"
    return lang

def fetch_topk(filepath, topk):
    ranking_per_qid = defaultdict(list)
    with open(filepath) as f:
        for idx, line in enumerate(f):
            if idx == 0:
                assert SYSDESC.match(line)
                continue
            ls = line.split(" ")
            qid = ls[0]
            did = ls[2]
            if len(ranking_per_qid[qid]) < topk:
                ranking_per_qid[qid].append(did)
    return ranking_per_qid

def take_ranking_union(rankings_list):
    ranking_per_qid = defaultdict(set)
    for rankings in rankings_list:
        for qid in rankings:
            ranking_per_qid[qid].update(rankings[qid])
    return ranking_per_qid


if __name__ == '__main__':
    parser = ArgumentParser(description="Pooling top k documents per query.")
    parser.add_argument("k", type=int,
                        help="Depth for pooling. "
                             "Only the top k documents per query are used.")
    parser.add_argument("input_filepaths", nargs='+',
                        help="Run files")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    pooled_rankings = defaultdict(set)
    for input_filepath in args.input_filepaths:
        rankings = fetch_topk(input_filepath, args.k)
        pooled_rankings = take_ranking_union((pooled_rankings, rankings))

    for qid in pooled_rankings:
        for did in pooled_rankings[qid]:
            print("{}\t{}".format(qid, did))
