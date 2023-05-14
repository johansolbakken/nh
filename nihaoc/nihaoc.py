import argparse
import sys
import parser
import tree
import python_generator


def parse_file(filename, output_filename):
    with open(filename, 'r') as file:
        source_code = file.read()
        result = parser.parse(source_code)
        result = tree.simplify_ast(result)
        python_generator.generate(result, output_filename)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Parsing files.')
    arg_parser.add_argument('files', metavar='file', type=str, nargs='+',
                            help='the files to parse')
    arg_parser.add_argument('-o', metavar='output', type=str, nargs=1,
                            help='the output file', default="a.py")

    args = arg_parser.parse_args()

    if not args.files:
        print("No files provided. Exiting.")
        sys.exit()

    for file in args.files:
        parse_file(file, args.o)
