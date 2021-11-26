import argparse
import os
import sys

from .mapping import AttackMapping

def parse_args():
    args = argparse.ArgumentParser(prog="attack-lookup", description="MITRE ATT&CK Lookup Tool", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args.add_argument("-v", "--version", default="v10.1", help="ATT&CK matrix version to use")
    args.add_argument("-m", "--matrix", choices=["enterprise", "ics", "mobile"], default="enterprise", help="ATT&CK matrix to use")
    args.add_argument("-O", "--offline", action="store_true", help="Run in offline mode")

    args.add_argument("-i", "--input", help="Path to input file (one lookup value per line)")
    args.add_argument("-o", "--output", default="-", help="Path to output file")
    args.add_argument("--output-mode", choices=["results", "csv"], default="results", help="Mode for output file (\"result\" only has the lookup results, \"csv\" outputs a CSV with the lookup and result values")

    return args.parse_args()

def do_interactive(mapping: AttackMapping):
    print("Running attack-lookup in interactive mode, exit with (q)uit. Enter one or more values to lookup, separated by a comma.")

    while True:
        # get input
        try:
            in_str = input("ATT&CK> ")
        except (EOFError, KeyboardInterrupt):
            print("") # this adds a newline and makes the CLI prompt cleaner when exiting
            break

        # check if we are quitting
        if in_str.lower() in ("q", "quit"):
            break

        # not quitting, do the lookups
        for x in in_str.split(","):
            print(mapping.lookup(x))

def do_batch(mapping: AttackMapping, input_file: str, output_file: str, output_mode: str) -> bool:
    # read in the input file
    try:
        with open(input_file, "r") as f:
            input_data = [x.strip() for x in f.readlines()]
    except FileNotFoundError:
        print(f"Failed to open {input_file}, is the path/permissions correct?")
        return False

    # do the item lookups
    output_items = []
    for i in input_data:
        output_items.append(mapping.lookup(i))

    # prepare the output data
    output_data = ""
    if output_mode == "results":
        # no input data needed in the output
        output_data = os.linesep.join(output_items)
    elif output_mode == "csv":
        # output data should be a CSV, each line with the input and output values
        data = []

        # make sure input and output data is the same length (this should always pass)
        assert len(input_data) == len(output_items)

        # build the csv lines
        for i in range(len(input_data)):
            data.append(",".join([input_data[i], output_items[i]]))

        # make the file contents
        output_data = os.linesep.join(data)

    if output_file == "-":
        # output should just go to stdout
        print(output_data)
    else:
        # output to file path
        try:
            with open(output_file, "w") as f:
                f.write(output_data)
                f.write(os.linesep)

            print(f"Wrote output data to {output_file}")
        except PermissionError:
            print(f"Failed to write to {output_file}, bad path/permissions?")
            return False

    return True

def main():
    args = parse_args()

    # load the proper att&ck mapping
    mapping = AttackMapping(args.matrix, args.version, args.offline)
    if not mapping.load_data():
        return

    # do interactive mode if no input file was specified
    if not args.input:
        do_interactive(mapping)
        return
    
    # input file present, run in batch mode
    if not do_batch(mapping, args.input, args.output, args.output_mode):
        sys.exit(1)

if __name__ == "__main__":
    main()