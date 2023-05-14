import argparse
import sys
import parser
import utils


def parse_file(filename):
    with open(filename, 'r') as file:
        source_code = file.read()
        result = parser.parse(source_code)
        utils.save_ast_png(result)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Parsing files.')
    arg_parser.add_argument('files', metavar='file', type=str, nargs='+',
                            help='the files to parse')

    args = arg_parser.parse_args()

    if not args.files:
        print("No files provided. Exiting.")
        sys.exit()

    for file in args.files:
        parse_file(file)
