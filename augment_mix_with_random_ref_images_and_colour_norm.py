from tqdm import tqdm
import os
import random
import pathlib
import argparse
import shutil
import glob
import json

def main(input_file, output_file, colour_norm_string_to_replace, colour_norm_methods_used, ref_images_string_to_replace, ref_images_used, seed):
    ensure_directory_exists(os.path.dirname(output_file))
    print(f'A copy of {input_file} will be made as {output_file}, where each instance of {colour_norm_string_to_replace} is replaced with one of {colour_norm_methods_used} and each instance of {ref_images_string_to_replace} is replaced by one of {ref_images_used}')
    shutil.copyfile(input_file, output_file)
    augment_with_random_string(output_file, colour_norm_string_to_replace, colour_norm_methods_used, seed)
    augment_with_random_string(output_file, ref_images_string_to_replace, ref_images_used, seed)

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)

def augment_with_random_string(json_file, string_to_replace, list_of_replacements, seed):
    random.seed(seed)
    with open(json_file, 'r') as temp_file:
        file_data = json.load(temp_file)
    for chunk in file_data["chunks"]:
        for idx, patch_path in enumerate(chunk["imgs"]):
            new_string = random.choice(list_of_replacements)
            chunk["imgs"][idx] = patch_path.replace(string_to_replace, new_string, 1)
    with open(json_file, 'w') as final_file:
        json.dump(file_data, final_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Makes copies of a json file, replacing the colour norm method in the patch paths (specified with "colour_norm_string_to_replace" with a random colour norm method specified in "colour_norm_methods_used", and also replacing the ref image string (specified with "ref_images_string_to_replace" with a random reference image specified in "ref_images_used"''')

    parser.add_argument('--input_file', type=str, required=True, 
            help='the fullpath to a json file that you want to copy and edit')
    parser.add_argument('--output_file', type=str, required=True,
            help='the path to the new json file you want to be written')
    parser.add_argument('--colour_norm_string_to_replace', type=str, required=True,
            help='the string (typically a method name) that will be replaced by the random colour norm method names')
    parser.add_argument('--colour_norm_methods_used', nargs='+', type=str, required=True, help='ex. vahadane macenko reinhard zanjani_100')
    parser.add_argument('--ref_images_string_to_replace', type=str, required=True,
            help='the string (typically reference image ID) that will be replaced by the random ref image names')
    parser.add_argument('--ref_images_used', nargs='+', type=str, required=True, help='ex. EC+OOU-6+92672_69632 "HGSC+VOA-1785A(Has Mark)+54784_31744"')
    parser.add_argument('--seed', type=int, default=256, help='optional seed')

    args = parser.parse_args()

    main(args.input_file, args.output_file, args.colour_norm_string_to_replace, args.colour_norm_methods_used, args.ref_images_string_to_replace, args.ref_images_used, args.seed)
