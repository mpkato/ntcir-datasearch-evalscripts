import csv
import sys
import numpy as np
from collections import defaultdict
from argparse import ArgumentParser

MAX_REQUEST_NUM = 10

def parse_amt_result(input_filepath):
    result = defaultdict(list)
    with open(input_filepath) as f:
        rows = csv.reader(f)
        header = None
        for row in rows:
            if header is None:
                header = row
            else:
                row_values = {key: value for key, value in zip(header, row)}
                res = parse_row(row_values)
                for r in res:
                    key = (r['qid'], r['did'])
                    result[key].append(r['rel'])
    return result

def parse_row(row_values):
    result = []
    for i in range(2, MAX_REQUEST_NUM+1):
        qid = row_values["Input.qid{}".format(i)]
        did = row_values["Input.did{}".format(i)]
        rel = None
        for score in range(3):
            score_bool = row_values["Answer.option{0}_{1}.{1}"
                                    .format(i, score)]
            if score_bool == 'true':
                rel = score
                break

        true_count = 0
        for score in range(3):
            score_bool = row_values["Answer.option{0}_{1}.{1}"
                                    .format(i, score)]
            if score_bool == 'true':
                true_count += 1
        assert true_count == 1

        result.append(dict(qid=qid, did=did, rel=rel))
    return result

def main():
    parser = ArgumentParser(description="Parse a CSV file downloaded "
                            "from AMT.")
    parser.add_argument('input_filepaths', nargs='+',
                        help="Files downloaded from Lancers")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    result = defaultdict(list)
    for input_filepath in args.input_filepaths:
        res = parse_amt_result(input_filepath)
        for key in res:
            result[key] += res[key]

    for key in sorted(result):
        scores = result[key]
        print(" ".join(map(str, list(key) + scores)))


if __name__ == '__main__':
    main()
