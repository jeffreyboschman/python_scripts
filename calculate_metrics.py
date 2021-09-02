import h5py
import numpy as np
from tqdm import tqdm
from PIL import Image
import json
import os
import random
import argparse
import tensorflow as tf
from sklearn.metrics.cluster import normalized_mutual_info_score
from skimage.color import rgb2hsv #also converts int (0-255) to float (0-1)
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_SSIM_Roy(orig_json_file, orig_path, color_norm_method, ref_images, new_paths):
    print('Metric: SSIM (as described by Roy) for intra-image variability ')
    print('Color normalization method:', color_norm_method) 
    fig, axes = plt.subplots(nrows=1, ncols=len(ref_images), sharey=True, figsize=(3*len(ref_images),10))
    for i, ref_image in enumerate(ref_images):
        print('\nReference image:', ref_image)
        SSIM_list = []
        norm_path = new_paths[i]
        image_object_name = color_norm_method + '_' + ref_image
        num = 0
        with open(orig_json_file, 'r') as jsonFile:
            jsonObject = json.load(jsonFile)
            for chunk in jsonObject["chunks"]:
                for img in tqdm(chunk['imgs']):
                    num += 1
                    orig_dir = img
                    relative_path = os.path.relpath(orig_dir, orig_path)
                    norm_dir = os.path.join(norm_path, relative_path)
                    orig_image = tf.convert_to_tensor(np.asarray(Image.open(orig_dir)))
                    norm_image = tf.convert_to_tensor(np.asarray(Image.open(norm_dir)))
                    SSIM_value = tf.image.ssim(orig_image, norm_image, max_val=255)
                    SSIM_list.append(SSIM_value)
            SSIM_mean = "{:.4f}".format(np.mean(np.array(SSIM_list)))
            SSIM_std = "{:.4f}".format(np.std(np.array(SSIM_list)))
            
            print("\tNumber of patches:", num)
            print("\tMean:", SSIM_mean)
            print("\tStandard deviation:", SSIM_std)

            axes[i].bar(0, float(SSIM_mean), yerr=float(SSIM_std), align='center', alpha=0.5, ecolor='black', capsize=10)
            axes[i].set_title(ref_image, fontsize=8)
    plt.ylim(0.0, 1.1)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(color_norm_method + ' SSIM (Roy)', fontsize=24) 
    plt.savefig('/projects/ovcare/classification/jboschman/colour_norm/methods_comparison/logs/images/bar_'+ color_norm_method +'_SSIM_Roy.png', dpi=fig.dpi)
    plt.close(fig)

def calculate_PCC_Roy(orig_json_file, orig_path, color_norm_method, ref_images, new_paths):
    print('Metric: PCC (as described by Roy) for intra-image variability ')
    print('Color normalization method:', color_norm_method) 
    fig, axes = plt.subplots(nrows=1, ncols=len(ref_images), sharey=True, figsize=(3*len(ref_images),10))
    for i, ref_image in enumerate(ref_images):
        print('\nReference image:', ref_image)
        PCC_list = []
        num = 0
        norm_path = new_paths[i]
        image_object_name = color_norm_method + '_' + ref_image
        with open(orig_json_file, 'r') as jsonFile:
            jsonObject = json.load(jsonFile)
            for chunk in jsonObject["chunks"]:
                for img in tqdm(chunk['imgs']):
                    orig_dir = img
                    relative_path = os.path.relpath(orig_dir, orig_path)
                    norm_dir = os.path.join(norm_path, relative_path)
                    orig_image = (np.asarray(Image.open(orig_dir)))
                    norm_image = (np.asarray(Image.open(norm_dir)))
                    PCC_value = np.corrcoef(orig_image.flat, norm_image.flat)[0,1]
                    PCC_list.append(PCC_value)
                    num += 1
            PCC_mean = "{:.4f}".format(np.mean(np.array(PCC_list)))
            PCC_std = "{:.4f}".format(np.std(np.array(PCC_list)))
            
            print("\tNumber of patches:", num)
            print("\tMean:", PCC_mean)
            print("\tStandard deviation:", PCC_std)

            axes[i].bar(0, float(PCC_mean), yerr=float(PCC_std), align='center', alpha=0.5, ecolor='black', capsize=10)
            axes[i].set_title(ref_image, fontsize=8)
    plt.ylim(0.0, 1.1)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(color_norm_method + ' PCC (Roy)', fontsize=24) 
    plt.savefig('/projects/ovcare/classification/jboschman/colour_norm/methods_comparison/logs/images/bar_'+ color_norm_method +'_PCC_Roy.png', dpi=fig.dpi)
    plt.close(fig)

def calculate_NormMedianIntensity(orig_json_file, orig_path, color_norm_method, ref_images, new_paths):
    print('Metric: Normalized median Intensity (as described by Zheng) for inter-image variability')
    print('Color normalization method:', color_norm_method) 
    fig, axes = plt.subplots(nrows=1, ncols=len(ref_images), sharey=True, figsize=(3*len(ref_images),10))
    for i, ref_image in enumerate(ref_images):
        print('\nReference image:', ref_image)
        num  =0 
        NMI_list = []
        norm_path = new_paths[i]
        image_object_name = color_norm_method + '_' + ref_image
        with open(orig_json_file, 'r') as jsonFile:
            jsonObject = json.load(jsonFile)
            for chunk in jsonObject["chunks"]:
                for img in tqdm(chunk['imgs']):
                    orig_dir = img
                    relative_path = os.path.relpath(orig_dir, orig_path)
                    norm_dir = os.path.join(norm_path, relative_path)
                    orig_image = (np.asarray(Image.open(orig_dir)))
                    norm_image = (np.asarray(Image.open(norm_dir)))
                    mean_values = np.mean(norm_image, axis=2)
                    median_intensity = np.median(mean_values)
                    percentile_95 = np.percentile(mean_values, 95)
                    NMI_value = median_intensity/percentile_95 
                    NMI_list.append(NMI_value)
                    num += 1
            NMI_mean = "{:.4f}".format(np.mean(np.array(NMI_list)))
            NMI_std = "{:.4f}".format(np.std(np.array(NMI_list)))
            NMI_cov = "{:.4f}".format((np.std(np.array(NMI_list)))/(np.mean(np.array(NMI_list))))
            print("\tNumber of patches:", num)
            print("\tMean:", NMI_mean)
            print("\tStandard deviation:", NMI_std)
            print("\tCoefficient of variation:", NMI_cov)
            sns.violinplot(y=NMI_list, ax=axes[i])
            axes[i].text(0,0.55, "std:"+NMI_std, fontsize=12)
            axes[i].text(0,0.52, "cov:"+NMI_cov, fontsize=12)
            axes[i].set_title(ref_image, fontsize=8)
    plt.ylim(0.5, 1.1)
    fig.suptitle(color_norm_method + ' Normalized Median Intensity (Zheng)', fontsize=24) 
    plt.savefig('/projects/ovcare/classification/jboschman/colour_norm/methods_comparison/logs/images/bar_'+ color_norm_method +'_Normalized_median_intensity_zheng.png', dpi=fig.dpi)
    plt.close(fig)

def seed_torch(seed=1234):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
#    torch.manual_seed(seed)
#    torch.cuda.manual_seed(seed)
#    torch.cuda.manual_seed_all(seed) # if you are using multi-GPU.
#    torch.backends.cudnn.benchmark = False
#    torch.backends.cudnn.deterministic = True





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''For calculating the average metric for a colour normalization method''')

    parser.add_argument('--orig_path', type=str, required=True,
            help='the path to where patches are saved in orig_json_file that will be replaced by th paths in new_paths')
    parser.add_argument('--orig_json_file', type=str, required=True,
            help='the path to a json file with path ids')
    parser.add_argument('--color_norm_method', type=str, required=True, 
            help='ex. vahdane, macenko, reinhard, etc')
    parser.add_argument('--ref_images', nargs='+', type=str, required=True, help='Reference images used for colour normalization')
    parser.add_argument('--new_paths', nargs='+', type=str, required=True, help='the paths to color normalized pathes that will replace the orig_path string')

    parser.add_argument('--SSIM_Roy', action='store_true', help='For calculating the Structural Singularity Index Measurement as described by Roy')
    parser.add_argument('--PCC_Roy', action='store_true', help='For calcuating the Pearson Correlation Coefficient as described by Roy')
    parser.add_argument('--Normalized_Median_Intensity_Zheng', action='store_true', help='For calculating the Normalized Median Intensity as described by Zheng to quantify inter-image color variability reduction')

    args = parser.parse_args()

    if args.SSIM_Roy:
        calculate_SSIM_Roy(args.orig_json_file, args.orig_path, args.color_norm_method, args.ref_images, args.new_paths)
        print("--------------------------------------\n\n")

    if args.PCC_Roy:
        calculate_PCC_Roy(args.orig_json_file, args.orig_path, args.color_norm_method, args.ref_images, args.new_paths)
        print("--------------------------------------\n\n")

    if args.Normalized_Median_Intensity_Zheng:
        calculate_NormMedianIntensity(args.orig_json_file, args.orig_path, args.color_norm_method, args.ref_images, args.new_paths)
