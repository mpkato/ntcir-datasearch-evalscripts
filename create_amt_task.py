import sys
import os
import csv
import json
import codecs
import random
from collections import defaultdict
from itertools import cycle
from more_itertools import chunked
from argparse import ArgumentParser
from create_lancers_task import (read_query_document_pairs, read_topics,
                                 read_gold_standard)

QUESTION_NUM = 9
CSV_HEADER = "known,qid1,did1,topic1,url1,qid2,did2,topic2,url2,qid3,did3,"\
             "topic3,url3,qid4,did4,topic4,url4,qid5,did5,topic5,url5,qid6,"\
             "did6,topic6,url6,qid7,did7,topic7,url7,qid8,did8,topic8,url8,"\
             "qid9,did9,topic9,url9,qid10,did10,topic10,url10"
AWS_URL = "https://ntcir-datasearch-en.s3-ap-northeast-1.amazonaws.com/{}.html#{}"


if __name__ == '__main__':
    parser = ArgumentParser(description="Create a CSV file for AMT.")
    parser.add_argument("input_filepath",
                        help="TSV file including query-document pairs")
    parser.add_argument("topic_filepath",
                        help="TSV file including the description "
                        "for each query")
    parser.add_argument("gold_standard_filepath",
                        help="TSV file including query-document pairs "
                        "for which the inter-rater agreement is high")
    parser.add_argument("output_filepath")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    qdpairs = read_query_document_pairs(args.input_filepath)
    qid_to_topics = read_topics(args.topic_filepath)
    gs = read_gold_standard(args.gold_standard_filepath)

    with open(args.output_filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER.split(","))
        for idx, qds in enumerate(chunked(qdpairs, QUESTION_NUM)):
            cy = cycle(qds)
            while len(qds) < QUESTION_NUM:
                qds += [next(cy)]

            known = 2 * (idx % 2)
            gold = next(gs[known])
            qds = [gold] + qds

            row = [known]
            for qid, did in qds:
                topic = qid_to_topics[qid]
                url = AWS_URL.format(did, idx)
                row += [qid, did, topic, url]
            writer.writerow(row)
