import os
import argparse
import csv

def main(csv_file_1, csv_file_2):
    patch_set_1 = get_set_of_patch_ids(csv_file_1)
    patch_set_2 = get_set_of_patch_ids(csv_file_2)
    set_1_only = get_difference_between_sets(patch_set_1, patch_set_2)
    #print(set_1_only)
    print_fullpaths_of_difference(set_1_only, csv_file_1, csv_file_2)

    set_2_only = get_difference_between_sets(patch_set_2, patch_set_1)
    print_fullpaths_of_difference(set_2_only, csv_file_2, csv_file_1)
       

def get_set_of_patch_ids(csv_file):
    patch_id_set = set()
    for row in csv.reader(open(csv_file)):
        slide_name = row[0]
        patch_id_set.add(slide_name)
    return patch_id_set

def get_difference_between_sets(set_1, set_2):
    set_1_only = set_1.difference(set_2)
    return set_1_only

def print_fullpaths_of_difference(set_a_only, csv_1, csv_2):
    print(f'There are {len(set_a_only)} patches in {csv_1} that are not in {csv_2}:')
    sorted_list_1_only = sorted(set_a_only)
    print(sorted_list_1_only)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For getting a textfile containing patch ids from all the png files saved in the csv of the patch ids''')

    parser.add_argument('--csv_file_1', type=str, required=True, help='The full path to the first csv we want to compare with')
    parser.add_argument('--csv_file_2', type=str, required=True, help='The full path to the second csv we want to compare with')

    args = parser.parse_args()

    main(args.csv_file_1, args.csv_file_2)
