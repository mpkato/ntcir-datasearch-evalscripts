import csv
import sys
import numpy as np
from collections import defaultdict
from argparse import ArgumentParser

def parse_lancers_result(input_filepath):
    result = defaultdict(list)
    with open(input_filepath, encoding="utf-16") as f:
        rows = csv.reader(f, delimiter="\t")
        header = None
        for row in rows:
            if header is None:
                header = row
            else:
                values = {key: value for key, value in zip(header, row)}
                for i in range(2, 11):
                    qid = values["qid{}".format(i)]
                    did = values["did{}".format(i)]
                    rel = int(values["task{}".format(i)])
                    key = (qid, did)
                    result[key].append(rel)
    return result


def main():
    parser = ArgumentParser(description="Parse a CSV file downloaded "
                            "from Lancers.")
    parser.add_argument('input_filepaths', nargs='+',
                        help="Files downloaded from Lancers")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    result = defaultdict(list)
    for input_filepath in args.input_filepaths:
        res = parse_lancers_result(input_filepath)
        for key in res:
            result[key] += res[key]

    for key in sorted(result):
        scores = result[key]
        print(" ".join(map(str, list(key) + scores)))


if __name__ == '__main__':
    main()
