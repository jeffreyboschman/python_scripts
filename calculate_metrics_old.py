import h5py
import numpy as np
from tqdm import tqdm
from PIL import Image
import os
import random
import argparse
import tensorflow as tf
from sklearn.metrics.cluster import normalized_mutual_info_score
from skimage.color import rgb2hsv #also converts int (0-255) to float (0-1)
import matplotlib.pyplot as plt
import seaborn as sns

def read_data_ids(data_id_path):
    """Function to read data ids (i.e., any *.txt contains row based information)

    Parameters
    ----------
    data_id_path : string
        Absoluate path to the *.txt contains data ids

    Returns
    -------
    data_ids : list
        List conntains data ids

    """
    with open(data_id_path) as file:
        data_ids = file.readlines()
        data_ids = [x.strip() for x in data_ids]
    return data_ids


def calculate_SSIM_Roy(h5py_file, patch_ids_file, color_norm_method, ref_images, filename_suffix):
    print('Metric: SSIM (as described by Roy) for intra-image variability '+filename_suffix)
    print('Color normalization method:', color_norm_method) 
    #set up graph
    fig, axes = plt.subplots(nrows=1, ncols=len(ref_images), sharey=True, figsize=(3*len(ref_images),10))
    for i, ref_image in enumerate(ref_images):
        print('\nReference image:', ref_image)
        patch_ids = read_data_ids(patch_ids_file)
        SSIM_list = []
        image_object_name = color_norm_method + '_' + ref_image
        if image_object_name == 'macenko_EC+OOU-6+92672_69632':
            print('N//A')
            axes[i].text(0.45,0.5, "N/A", fontsize=16)
            axes[i].set_title(ref_image, fontsize=8)
            axes[i].set_xticks([])
        else:
            with h5py.File(h5py_file,'r') as f:
                for patch_id in tqdm(patch_ids):
                    cur_image = tf.convert_to_tensor(np.asarray(f[patch_id]['image_data']))
                    norm_image = tf.convert_to_tensor(np.asarray(f[patch_id][image_object_name]))
                    SSIM_value = tf.image.ssim(cur_image, norm_image, max_val=255)
                    SSIM_list.append(SSIM_value)
            SSIM_mean = "{:.4f}".format(np.mean(np.array(SSIM_list)))
            SSIM_std = "{:.4f}".format(np.std(np.array(SSIM_list)))
            
            print("\tNumber of patches:", len(patch_ids))
            print("\tMean:", SSIM_mean)
            print("\tStandard deviation:", SSIM_std)

            axes[i].bar(0, float(SSIM_mean), yerr=float(SSIM_std), align='center', alpha=0.5, ecolor='black', capsize=10)
            axes[i].set_title(ref_image, fontsize=8)
    plt.ylim(0.0, 1.1)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(color_norm_method + ' SSIM (Roy) '+filename_suffix, fontsize=24) 
    plt.savefig('/projects/ovcare/classification/jboschman/colour_norm/logs/bar_'+ color_norm_method +'_SSIM_Roy_'+ filename_suffix +'.png', dpi=fig.dpi)
    plt.close(fig)

def calculate_PCC_Roy(h5py_file, patch_ids_file, color_norm_method, ref_images, filename_suffix):
    print('Metric: PCC (as described by Roy) for intra-image variability '+filename_suffix)
    print('Color normalization method:', color_norm_method) 
    #set up graph
    fig, axes = plt.subplots(nrows=1, ncols=len(ref_images), sharey=True, figsize=(3*len(ref_images),10))
    for i, ref_image in enumerate(ref_images):
        print('\nReference image:', ref_image)
        patch_ids = read_data_ids(patch_ids_file)
        PCC_list = []
        image_object_name = color_norm_method + '_' + ref_image
        if image_object_name == 'macenko_EC+OOU-6+92672_69632':
            print('N//A')
            axes[i].text(0.45,0.5, "N/A", fontsize=16)
            axes[i].set_title(ref_image, fontsize=8)
            axes[i].set_xticks([])
        else:
            with h5py.File(h5py_file,'r') as f:
                for patch_id in tqdm(patch_ids):
                    cur_image =(np.asarray(f[patch_id]['image_data'])) 
                    norm_image = (np.asarray(f[patch_id][image_object_name]))
                    PCC_value = np.corrcoef(cur_image.flat, norm_image.flat)[0,1] 
                    PCC_list.append(PCC_value)
            PCC_mean = "{:.4f}".format(np.mean(np.array(PCC_list)))
            PCC_std = "{:.4f}".format(np.std(np.array(PCC_list)))
            
            print("\tNumber of patches:", len(patch_ids))
            print("\tMean:", PCC_mean)
            print("\tStandard deviation:", PCC_std)

            axes[i].bar(0, float(PCC_mean), yerr=float(PCC_std), align='center', alpha=0.5, ecolor='black', capsize=10)
            axes[i].set_title(ref_image, fontsize=8)
    plt.ylim(0.0, 1.1)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(color_norm_method + ' PCC (Roy) '+filename_suffix, fontsize=24) 
    plt.savefig('/projects/ovcare/classification/jboschman/colour_norm/logs/bar_'+ color_norm_method +'_PCC_Roy_'+ filename_suffix +'.png', dpi=fig.dpi)
    plt.close(fig)

def calculate_NormMutInfo_Zarella(h5py_file, patch_ids_file, color_norm_method, ref_images, filename_suffix):
    print('Metric: Normalized Mutual Information (as described by Zarella) for intra-image variability '+filename_suffix)
    print('Color normalization method:', color_norm_method) 
    #set up graph
    fig, axes = plt.subplots(nrows=1, ncols=len(ref_images), sharey=True, figsize=(3*len(ref_images),10))
    for i, ref_image in enumerate(ref_images):
        print('\nReference image:', ref_image)
        patch_ids = read_data_ids(patch_ids_file)
        H_score_list = []
        S_score_list = []
        V_score_list = []
        image_object_name = color_norm_method + "_" + ref_image
        if image_object_name == 'macenko_EC+OOU-6+92672_69632':
            print('N//A')
            axes[i].text(0.45,0.5, "N/A", fontsize=16)
            axes[i].set_title(ref_image, fontsize=8)
            axes[i].set_xticks([])
        else:
            with h5py.File(h5py_file,'r') as f:
                for patch_id in tqdm(patch_ids):
                    cur_image =rgb2hsv(np.asarray(f[patch_id]['image_data']))
                    norm_image =rgb2hsv(np.asarray(f[patch_id][image_object_name]))
                    H_value = normalized_mutual_info_score(cur_image[:,:,0].flat, norm_image[:,:,0].flat)
                    S_value = normalized_mutual_info_score(cur_image[:,:,1].flat, norm_image[:,:,1].flat)
                    V_value = normalized_mutual_info_score(cur_image[:,:,2].flat, norm_image[:,:,2].flat)
                    H_score_list.append(H_value)
                    S_score_list.append(S_value)
                    V_score_list.append(V_value)
            H_mean = (np.mean(np.array(H_score_list)))
            S_mean = (np.mean(np.array(S_score_list)))
            V_mean = (np.mean(np.array(V_score_list)))
            H_std = (np.std(np.array(H_score_list)))
            S_std = (np.std(np.array(S_score_list)))
            V_std = (np.std(np.array(V_score_list)))

            print("\tNumber of patches:", len(patch_ids))
            print("\tH-channel Mean:", "{:.4f}".format(H_mean))
            print("\tS-channel Mean:", "{:.4f}".format(S_mean))
            print("\tV-channel Mean:", "{:.4f}".format(V_mean))
            print("\tH-channel Standard deviation:", "{:.4f}".format(H_std))
            print("\tS-channel Standard deviation:", "{:.4f}".format(S_std))
            print("\tV-channel Standard deviation:", "{:.4f}".format(V_std))

            axes[i].bar(['H','S','V'], [H_mean, S_mean, V_mean], yerr=[H_std, S_std, V_std], align='center', alpha=0.5, ecolor='black', capsize=10)
            axes[i].set_title(ref_image, fontsize=8)
 
    plt.ylim(0.0, 1.1)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(color_norm_method + ' Normalized Mutual Information (Zarella) '+filename_suffix, fontsize=24) 
    plt.savefig('/projects/ovcare/classification/jboschman/colour_norm/logs/bar_'+ color_norm_method +'_Normalized_Mutual_Information_Zarella_'+ filename_suffix +'.png', dpi=fig.dpi)
    plt.close(fig)

def calculate_NormMedianIntensity(h5py_file, patch_ids_file, color_norm_method, ref_images, filename_suffix):

    print('Metric: Normalized Median Intensity (as described by Zheng) for inter-image variability '+filename_suffix)
    print('Color normalization method:', color_norm_method) 
    #set up graph
    fig, axes = plt.subplots(nrows=1, ncols=len(ref_images), sharey=True, figsize=(3*len(ref_images),10))
    for i, ref_image in enumerate(ref_images):
        print('\nReference image:', ref_image)
        patch_ids = read_data_ids(patch_ids_file)
        NMI_list = []
        image_object_name = color_norm_method + '_' + ref_image
        if image_object_name == 'macenko_EC+OOU-6+92672_69632':
            print('N//A')
            axes[i].text(0.45,0.75, "N/A", fontsize=16)
            axes[i].set_title(ref_image, fontsize=8)
            axes[i].set_xticks([])
        else:
            with h5py.File(h5py_file,'r') as f:
                for patch_id in tqdm(patch_ids):
                    cur_image =(np.asarray(f[patch_id]['image_data'])) 
                    norm_image = (np.asarray(f[patch_id][image_object_name]))
                    mean_values = np.mean(norm_image, axis=2)
                    median_intensity = np.median(mean_values)
                    percentile_95 = np.percentile(mean_values, 95)
                    NMI = median_intensity/percentile_95
                    NMI_list.append(NMI)
            NMI_mean = "{:.4f}".format(np.mean(np.array(NMI_list)))
            NMI_std = "{:.4f}".format(np.std(np.array(NMI_list)))
            NMI_cov = "{:.4f}".format((np.std(np.array(NMI_list)))/(np.mean(np.array(NMI_list))))
            print("\tNumber of patches:", len(patch_ids))
            print("\tMean:", NMI_mean)
            print("\tStandard deviation:", NMI_std)
            print("\tCoefficient of variation:", NMI_cov)
            sns.violinplot(y=NMI_list, ax=axes[i])
            axes[i].text(0,0.55, "std:"+NMI_std, fontsize=12)
            axes[i].text(0,0.52, "cov:"+NMI_cov, fontsize=12)
            axes[i].set_title(ref_image, fontsize=8)
    plt.ylim(0.5, 1.1)
    fig.suptitle(color_norm_method + ' Normalized Median Intensity (Zheng) '+filename_suffix, fontsize=24) 
    fig.savefig('/projects/ovcare/classification/jboschman/colour_norm/logs/violin_'+ color_norm_method +'_Normalized_Median_Intensity_Zheng_'+ filename_suffix +'.png')


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

    parser.add_argument('--h5py_file', type=str, required=True,
            help='the path to an h5py file that currently contains the patches as dataset objects')
    parser.add_argument('--patch_ids', type=str, required=True,
            help='the path to a textfile that contains lines with the patch ids, ex. CC/VOA-113/11243_52134')
    parser.add_argument('--color_norm_method', type=str, required=True, 
            help='ex. vahdane, macenko, reinhard, etc')
    parser.add_argument('--ref_images', nargs='+', type=str, required=True, help='Reference images used for colour normalization')
    parser.add_argument('--filename_suffix', type=str, help='Optional. ex. test_set, training_set, etc')

    parser.add_argument('--SSIM_Roy', action='store_true', help='For calculating the Structural Singularity Index Measurement as described by Roy')
    parser.add_argument('--PCC_Roy', action='store_true', help='For calcuating the Pearson Correlation Coefficient as described by Roy')
    parser.add_argument('--Normalized_Mutual_Information_Zarella', action='store_true', help='For calculating the Normalized Mutual Information as described by Zarella')
    parser.add_argument('--Normalized_Median_Intensity_Zheng', action='store_true', help='For calculating the Normalized Median Intensity as described by Zheng to quantify inter-image color variability reduction')

    args = parser.parse_args()

    if args.SSIM_Roy:
        calculate_SSIM_Roy(args.h5py_file, args.patch_ids, args.color_norm_method, args.ref_images, args.filename_suffix)
        print("--------------------------------------\n\n")

    if args.PCC_Roy:
        calculate_PCC_Roy(args.h5py_file, args.patch_ids, args.color_norm_method, args.ref_images, args.filename_suffix)
        print("--------------------------------------\n\n")

    if args.Normalized_Mutual_Information_Zarella:
        calculate_NormMutInfo_Zarella(args.h5py_file, args.patch_ids, args.color_norm_method, args.ref_images, args.filename_suffix)
        print("--------------------------------------\n\n")

    if args.Normalized_Median_Intensity_Zheng:
        calculate_NormMedianIntensity(args.h5py_file, args.patch_ids, args.color_norm_method, args.ref_images, args.filename_suffix)
