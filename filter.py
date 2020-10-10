import sys
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser(description="Filter out judged query-document "
                            "pairs.")
    parser.add_argument("qrel_filepath",
                        help="File including qrels")
    parser.add_argument("input_filepath",
                        help="File including query document pairs")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    qid_did_pairs = set()
    with open(args.qrel_filepath) as f:
        for line in f:
            qid, did, _ = line.strip().split(" ")
            qid_did_pairs.add((qid, did))

    with open(args.input_filepath) as f:
        for line in f:
            qid, did = line.strip().split("\t")
            if not (qid, did) in qid_did_pairs:
                print(line.strip())
