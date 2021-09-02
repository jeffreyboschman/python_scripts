from tqdm import tqdm
import os
import pathlib
import argparse
import shutil
import glob
import json

def main(input_json_file_dir, output_file_dir, new_filename_suffix, input_patch_list_file, input_patch_list_index):
    bad_patch_ids = get_list_of_file_lines(input_patch_list_file, input_patch_list_index)
    ensure_directory_exists(output_file_dir)
    for file_idx, input_file in enumerate(sorted(glob.glob(os.path.join(input_json_file_dir, 'split*')))): 
        input_filename, input_file_extension = get_filename_and_extension(input_file)
        new_filename = input_filename + new_filename_suffix + input_file_extension
        output_file = os.path.join(output_file_dir, new_filename)
        shutil.copyfile(input_file, output_file)
        print(output_file)
        remove_bad_patch_ids_from_file(bad_patch_ids, output_file)
#        with open(input_patch_list_file, 'r') as patch_file:
#            lines = patch_file.readlines()
#            print(lines)
#            for line in lines:
#                line = line.rstrip('\n')
#            print(lines)
#    new_file = shutil.copyfile(input_json_file, output_file)   


#
#
#    for input_file in input_json_file:
#        input_file_filename, input_file_extension = get_filename_and_extension(input_file)
#        for idx, new_filename_suffix in enumerate(new_filename_suffixes):
#            new_filename = input_file_filename + new_filename_suffix + input_file_extension 
#            current_output_file = os.path.join(output_file_dir, new_filename)
#            shutil.copyfile(input_file, current_output_file)
#            replace_text_in_file(original_text, new_text[idx], current_output_file)
#
def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)

def get_list_of_file_lines(input_file, start_index):
    with open(input_file, 'r') as f:
        lines = f.readlines()
        lines = lines[start_index:]
        lines = [line.strip() for line in lines]
    return lines


def get_filename_and_extension(filepath):
    filename, file_extension = os.path.splitext(filepath.split('/')[-1])
    return filename, file_extension

def remove_bad_patch_ids_from_file(bad_patch_ids_list, filepath):
    with open(filepath, 'r') as temp_file:
        file_data = json.load(temp_file) 
    for chunk in file_data["chunks"]:
        for bad_patch_id in bad_patch_ids_list:
            if bad_patch_id in chunk["imgs"]:
                chunk["imgs"].remove(bad_patch_id)
    with open(filepath, 'w') as final_file:
        json.dump(file_data, final_file)
#
#def replace_text_in_file(old_text, new_text, filepath):
#    with open(filepath, 'r') as temp_file:
#        file_data = temp_file.read()
#    file_data = file_data.replace(old_text, new_text)
#    with open(filepath, 'w') as final_file:
#        final_file.write(file_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Removes the patches specified in a text file from the json file''')

    parser.add_argument('--input_json_file_dir', type=str, required=True, 
            help='the path to the json file you want to make copies of with an edited directory structure.')
    parser.add_argument('--output_file_dir', type=str, required=True,
            help='the path to a new file you want to be created')
    parser.add_argument('--new_filename_suffix', type=str, default = '', help='The suffix to add to new filenames.')
    parser.add_argument('--input_patch_list_file', type=str, required=True,
            help='the path to a text file that contains the patches you want deleted from the json file')
    parser.add_argument('--input_patch_list_index', type=int, default=0, help='the index where the patch list begins in the input_path_list textfile')

    args = parser.parse_args()

    main(args.input_json_file_dir, args.output_file_dir, args.new_filename_suffix, args.input_patch_list_file, args.input_patch_list_index)
