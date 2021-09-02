import os
import argparse
import numpy as np
from PIL import Image
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

def main(input_path, output_path):
    for root, dirs, files, in os.walk(input_path):
        for patch in files:
            try:
                orig_patch_path = os.path.join(root, patch)
                orig_patch = np.asarray(Image.open(orig_patch_path))
                grey_patch = perform_greyscale(orig_patch)

                grey_patch_path = get_current_image_new_save_path(input_path, output_path, orig_patch_path)
                ensure_directory_exists(os.path.dirname(grey_patch_path))

                grey_patch_image = Image.fromarray(grey_patch)
                grey_patch_image.save(grey_patch_path)
            except Exception as e:
                print(e)
                print("There was a problem performing greyscale on the patch id:", orig_patch_path, "\n")

def perform_greyscale(input_image):
    image_copy = input_image.copy()
    grey_image = np.array(Image.fromarray(image_copy).convert('L')) #has shape, for example, (256,256)
    grey_image = np.stack((grey_image,)*3, axis=-1) #to make shape, for example,  (256,256,3)
    return grey_image

def get_current_image_new_save_path(input_dir, output_dir, current_image_path):
    relative_path = os.path.relpath(current_image_path, input_dir)
    new_save_path = os.path.join(output_dir, relative_path)
    return new_save_path

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        Path(directory_path).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True, default='/projects/ovcare/classification/jboschman/colour_norm/datasets/300_dataset/150_ppp_20x_256_vahadane')
    parser.add_argument('--output_dir', type=str, required=True, default='/projects/ovcare/classifiation/jboschman/colour_norm/datasets/300_dataset/150_ppp_20x_256_vahadane_grey')

    args = parser.parse_args()

    main(args.input_dir, args.output_dir)

