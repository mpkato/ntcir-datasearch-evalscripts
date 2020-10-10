import sys
import numpy as np
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description="Compute the relevance grade.")
    parser.add_argument('input_filepath',
                        help="File including scores for "
                        "each query-document pairs")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    with open(args.input_filepath) as f:
        for line in f:
            values = line.split(" ")
            qid = values[0]
            did = values[1]
            scores = sorted(list(map(int, values[2:])))
            m = np.median(scores)
            m = "L{}".format(int(m))
            print(" ".join((qid, did, m)))


if __name__ == '__main__':
    main()
