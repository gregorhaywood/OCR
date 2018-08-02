#! /usr/bin/env python3

import viterbi as vb



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Print a codec in human readable form")
    parser.add_argument("codec", type=str, nargs=1, metavar="CODEC",
                        help="The CODEC.csv file to print")
    args = parser.parse_args()
    vb.printCodec(args.codec)
    
    
    