import os
import argparse

def main(input_dir_1, input_dir_2):
    patch_set_1 = get_set_of_patch_ids(input_dir_1)
    patch_set_2 = get_set_of_patch_ids(input_dir_2)
    set_1_only = get_difference_between_sets(patch_set_1, patch_set_2)
    print_fullpaths_of_difference(set_1_only, input_dir_1, input_dir_2)

    set_2_only = get_difference_between_sets(patch_set_2, patch_set_1)
    print_fullpaths_of_difference(set_2_only, input_dir_2, input_dir_1)
        

def get_set_of_patch_ids(input_dir):
    patch_id_set = set()
    for root, dirs, name in os.walk(input_dir):
        for filename in name:
            if '.png' in filename:
                relative_dir = os.path.relpath(root, input_dir)
                relative_file = os.path.join(relative_dir, filename)
                patch_id_set.add(relative_file)
    return patch_id_set

def get_difference_between_sets(set_1, set_2):
    set_1_only = set_1 - set_2
    return set_1_only

def print_fullpaths_of_difference(set_a_only, dir_1, dir_2):
    print(f'There are {len(set_a_only)} patches in {dir_1} that are not in {dir_2}:')
    sorted_list_1_only = sorted(set_a_only)
    for relative_file in sorted_list_1_only:
        full_path = os.path.join(dir_1, relative_file)
        print(f'{full_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For getting a textfile containing patch ids from all the png files saved in the directory tree format of the patch ids''')

    parser.add_argument('--input_dir_1', type=str, required=True, help='The full path to the first directory we want to compare with')
    parser.add_argument('--input_dir_2', type=str, required=True, help='The full path to the second directory we want to compare with')

    args = parser.parse_args()

    main(args.input_dir_1, args.input_dir_2)
