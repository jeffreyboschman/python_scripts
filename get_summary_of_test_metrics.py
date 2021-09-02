import os
import glob
import argparse

def main(input_dir, metric):
    all_results_list = []
    print('Results are from the following files in this order:')
    for file_idx, results_file in enumerate(sorted(glob.glob(os.path.join(input_dir, 'log_*')))):
        print(results_file)
        with open(results_file, 'r') as results_file: 
            lines = results_file.read().splitlines()
            metric_line = lines[-3]
            results_line = lines[-2]
            metric_list = filter(None, metric_line.split('||'))
            results_list = filter(None, results_line.split('|'))
            results_dict = dict(zip(metric_list, results_list))
            all_results_list += [results_dict[metric]]
    print_summary(metric, all_results_list)

def print_summary(metric, all_results_list):
    output = f'\n{metric}\n'
    for result in all_results_list:
        output += f'{result}  '
    print(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For easier copying and pasting of results''')

    parser.add_argument('--input_dir', type=str, help='the directory that contains the results files')
    parser.add_argument('--metric', type=str, default='AUC', help='Things like F1 score, AUC, etc')

    args = parser.parse_args()
    
    main(args.input_dir, args.metric)
