import os
import glob
import argparse

def main(input_dir, line, method):
    allResults_list = []
    print('Results are from the following files in this order:')
    for file_idx, results_file in enumerate(sorted(glob.glob(os.path.join(input_dir, 'log_*')))):
        print(results_file)
        with open(results_file, 'r') as results_file: 
            lines = results_file.read().splitlines()
            results_line = lines[line]
            results_line = results_line.replace('X', method)
            allResults_list.append(results_line)
            previousLine = lines[line-1]
    print(f'\n{previousLine}')
    print(*allResults_list, sep='\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For easier copying and pasting of results''')

    parser.add_argument('--input_dir', type=str, help='the directory that contains the results files')
    parser.add_argument('--line', type=int, default=923, help='Line where the results we want are')
    parser.add_argument('--method', type=str, help='the name of the method')

    args = parser.parse_args()
    
    main(args.input_dir, args.line, args.method)
