from tqdm import tqdm
import os
import random
import pathlib
import argparse
import shutil
import glob
import json

def main(input_dir, output_dir, string_to_replace, colour_norm_methods_used, new_filename_string, seed):
    ensure_directory_exists(output_dir)
    print(f'In the files, {string_to_replace} is replaced with one of {colour_norm_methods_used}')
    for input_file in sorted(glob.glob(os.path.join(input_dir, '*.json'))): 
        random.seed(seed)
        input_filename, input_file_extension = get_filename_and_extension(input_file)
        new_filename = input_filename.replace(string_to_replace, new_filename_string) + input_file_extension
        output_file = os.path.join(output_dir, new_filename)
        shutil.copyfile(input_file, output_file)
        print(output_file)
        augment_with_random_colour_norm(output_file, string_to_replace, colour_norm_methods_used)

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)

def get_filename_and_extension(filepath):
    filename, file_extension = os.path.splitext(filepath.split('/')[-1])
    return filename, file_extension

def augment_with_random_colour_norm(json_file, string_to_replace, colour_norm_methods_list):
    with open(json_file, 'r') as temp_file:
        file_data = json.load(temp_file)
    for chunk in file_data["chunks"]:
        for idx, patch_path in enumerate(chunk["imgs"]):
            new_colour_norm_method_string = random.choice(colour_norm_methods_list)
            chunk["imgs"][idx] = patch_path.replace(string_to_replace, new_colour_norm_method_string)
    with open(json_file, 'w') as final_file:
        json.dump(file_data, final_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Makes copies of cross validation split json files, replacing the colour norm method in the patch paths with a random colour norm method specified in "colour_norm_methods_used"''')

    parser.add_argument('--input_dir', type=str, required=True, 
            help='the path to the directory that contains the cross validation split json files you want to make copies of with edited directory structures.')
    parser.add_argument('--output_dir', type=str, required=True,
            help='the path to the directory where you want the new json files to be written')
    parser.add_argument('--string_to_replace', type=str, required=True,
            help='the string (typically a method name) that will be replaced by the random method names')
    parser.add_argument('--colour_norm_methods_used', nargs='+', type=str, required=True, help='ex. vahadane macenko reinhard zanjani_100')
    parser.add_argument('--new_filename_string', type=str, default = 'augment_with_random_colour_norm', help='what the "string_to_replace" will be replaced with in the new filenames')
    parser.add_argument('--seed', type=int, default=256, help='optional seed')

    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.string_to_replace, args.colour_norm_methods_used, args.new_filename_string, args.seed)
