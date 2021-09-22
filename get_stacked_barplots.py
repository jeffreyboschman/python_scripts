import os
import glob
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def create_stacked_barplots(csv_dir, subtypes_list, patch_pattern, threshold, verbose):
    print(f'All patch probabilities must be greater than {threshold} in order to be considered.\n')
    for file_idx, csv_file in enumerate(sorted(glob.glob(os.path.join(csv_dir, '*.csv')))):
        print(f'\n{csv_file}\n')
        slide_pred_votes_dict = dict()
        slide_real_labels_dict = dict()
        df = pd.read_csv(csv_file)
        for idx, row in df.iterrows():
            slide_id = get_slide_id_from_full_file_name(row['path'], patch_pattern)
            probability_list = get_list_from_probability_string(row['probability'])
            target_label = int(row['target_label'])
            predicted_label = int(row['predicted_label'])
            if max(probability_list) > threshold: 
                if slide_id in slide_pred_votes_dict:
                    slide_pred_votes_dict[slide_id][predicted_label]+=1
                else:
                    slide_real_labels_dict[slide_id] = target_label
                    slide_pred_votes_dict[slide_id] = [0]*len(subtypes_list) 
                    slide_pred_votes_dict[slide_id][predicted_label]+=1

        pred_df = pd.DataFrame.from_dict(slide_pred_votes_dict, orient='index')
        for idx, subtype in enumerate(subtypes_list):
            pred_df.rename(columns={idx:subtype}, inplace=True)
        pred_df['total_patches'] = pred_df[subtypes_list].sum(axis=1)
        for subtype in subtypes_list:
            pred_df[subtype+'_%'] = pred_df[subtype]/pred_df['total_patches']
        if verbose:
            print("First 5 rows of dataframe that has the counts and percentages of predicted patches for each slide")
            print(pred_df.head())

        target_df = pd.DataFrame.from_dict(slide_real_labels_dict, orient='index')
        target_df.rename(columns={0:'target_label'}, inplace=True)
        for idx, subtype in enumerate(subtypes_list):
            target_df["target_label"].replace({idx:subtype}, inplace=True)
        if verbose:
            print("First 5 rows of dataframe that has the true label for each slide")
            target_df.head()

        slide_df = pd.merge(pred_df, target_df, how='outer', left_index=True, right_index=True)
        subtypes_df = pd.DataFrame(subtypes_list, columns=['real_subtype'])
        for subtype in subtypes_list:
            subtype_perc_means = slide_df.groupby('target_label')[subtype + '_%'].mean()
            print(subtype_perc_means.values)
            subtypes_df[subtype+'_%_mean'] = subtype_perc_means.values
        subtypes_df.set_index('real_subtype', inplace=True)
        if verbose:
            print("The mean % of patches predicted as a subtype per slide by true subtype")
            subtypes_df

        ax = subtypes_df.plot.bar(stacked=True)
        fig = ax.get_figure()
        save_name = "stacked_barplot_" + os.path.basename(csv_file)[:-4] + ".png"
        print(save_name)
        plt.savefig(os.path.join(csv_dir, save_name), dpi=fig.dpi)
        plt.close(fig)

def get_slide_id_from_full_file_name(file_name, patch_pattern):
    patch_pattern_parts = patch_pattern.split('/')
    patch_pattern_slide_id_relative_index = patch_pattern_parts.index('slide') - len(patch_pattern_parts) - 1
    file_name_parts = file_name.split('/')
    return file_name_parts[patch_pattern_slide_id_relative_index]

def get_list_from_probability_string(orig_string):
    '''probability has form "[0.333 0.666]", for example. It is type str.'''
    new_list = []
    for num in orig_string[1:-1].split(' '):
        try:
            new_list.append(float(num))
        except:
            pass
    return new_list


def get_threshold_value(subtypes_list, threshold):
    if threshold is None:
        return float(1/len(subtypes_list))
    else:
        return threshold

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=''' Gets slide level accuracies ''')

    parser.add_argument('--csv_dir', type=str, help='the directory that contains the csv files. This is also the dir where the output images will be saved.')
    parser.add_argument('--subtypes_list', nargs='+', type=str, help='Space separated strings. Ensure the order is the same as in the training file. Example: "benign malignant"')
    parser.add_argument('--patch_pattern', type=str, default='subtype/slide/magnification', help="'/' separated words describing the directory structure of the patch paths between the root dir and the patch itself.")
    parser.add_argument('--threshold', type=float, help='The threshold for whether to include a patch-level prediction. The default is 1/len(subtype_list)')
    parser.add_argument('--verbose', action='store_true', default=False)

    args = parser.parse_args()
    
    threshold = get_threshold_value(args.subtypes_list, args.threshold) 

    create_stacked_barplots(args.csv_dir, args.subtypes_list, args.patch_pattern, threshold, args.verbose)
