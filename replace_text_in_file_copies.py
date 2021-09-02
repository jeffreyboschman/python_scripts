from tqdm import tqdm
import os
import pathlib
import argparse
import shutil

def main(input_files, output_file_dir, new_filename_suffixes, original_text, new_text):
    ensure_directory_exists(output_file_dir)
    for input_file in input_files:
        input_file_filename, input_file_extension = get_file_name_and_extension(input_file)
        for idx, new_filename_suffix in enumerate(new_filename_suffixes):
            new_filename = input_file_filename + new_filename_suffix + input_file_extension 
            current_output_file = os.path.join(output_file_dir, new_filename)
            shutil.copyfile(input_file, current_output_file)
            replace_text_in_file(original_text, new_text[idx], current_output_file)

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)

def get_file_name_and_extension(filepath):
    file_name, file_extension = os.path.splitext(filepath.split('/')[-1])
    return file_name, file_extension

def replace_text_in_file(old_text, new_text, filepath):
    with open(filepath, 'r') as temp_file:
        file_data = temp_file.read()
    file_data = file_data.replace(old_text, new_text)
    with open(filepath, 'w') as final_file:
        final_file.write(file_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Makes copies of json files (ex. with chunks) and then replaces the text of a directory structure in the new json files''')

    parser.add_argument('--input_files', nargs='+', type=str, 
            help='the paths to the json files you want to make copies of with an edited directory structure. You can do multiple json files at once, just write them separated. Ex. --input_files path/to/json_1.json path/to/json_2.json')
    parser.add_argument('--output_file_dir', type=str, required=True,
            help='the path to a directory where you want the output files to be saved')
    parser.add_argument('--new_filename_suffixes', nargs='+', type=str,
            help='the suffixes you want added to the end of the new json filenames. Please add one entry here for each new_text option added')
    parser.add_argument('--original_text', type=str, required=True,
            help='the original text you want to replace with something else. Ex --original_text "150_ppp_20x_256"')
    parser.add_argument('--new_text', nargs='+', type=str,
            help='the new text you want the original text to be replaced with. You can make multiples of the json files by adding more entries here. Ex --new_text "150_ppp_20x_256_vahadane/EC+VOA-101B+23456_11224" "150_ppp_20x_256_vahadane/MC+OOU-123+78900_98765"')

    args = parser.parse_args()

    main(args.input_files, args.output_file_dir, args.new_filename_suffixes, args.original_text, args.new_text)
