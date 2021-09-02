import os
import argparse
import numpy as np
from PIL import Image
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

def main(input_path, output_path, crop_size):
    for root, dirs, files, in os.walk(input_path):
        for patch in files:
            try:
                orig_patch_path = os.path.join(root, patch)
                orig_patch = np.asarray(Image.open(orig_patch_path))
                cropped_patch = crop_image_array(orig_patch, crop_size)

                cropped_patch_path = get_current_image_new_save_path(input_path, output_path, orig_patch_path)
                ensure_directory_exists(os.path.dirname(cropped_patch_path))

                cropped_patch_image = Image.fromarray(cropped_patch)
                cropped_patch_image.save(cropped_patch_path)
            except Exception as e:
                print(e)
                print("There was a problem cropping the patch id:", orig_patch_path, "\n")

def crop_image_array(input_image_array, crop_size):
    y_mid = int(input_image_array.shape[0]/2)
    print("ymid",y_mid)
    y1 = int(y_mid - crop_size/2.0)
    print(y1)
    y2 = int(y_mid + crop_size/2.0)
    print(y2)

    x_mid = int(input_image_array.shape[1]/2)
    x1 = int(x_mid - crop_size/2.0)
    x2 = int(x_mid + crop_size/2.0)
    print("xmid", x_mid)
    print(x1)
    print(x2)

    cropped_image_array = input_image_array[y1:y2, x1:x2, ...]
    return cropped_image_array

def get_current_image_new_save_path(input_dir, output_dir, current_image_path):
    relative_path = os.path.relpath(current_image_path, input_dir)
    new_save_path = os.path.join(output_dir, relative_path)
    return new_save_path

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        Path(directory_path).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True, default='/projects/ovcare/classification/jboschman/colour_norm/datasets/BH_dataset/40x_700_460')
    parser.add_argument('--output_dir', type=str, required=True, default='/projects/ovcare/classifiation/jboschman/colour_norm/datasets/BH_dataset/40x_460')
    parser.add_argument('--crop_size', type=int, required=True, default=460)

    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.crop_size)

