import os
import sys
import csv
import glob
import argparse
import enum
import json
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
from sklearn.metrics import roc_auc_score

def main(input_dir, output_textfile, subtypes_list, patch_pattern, threshold):
    ensure_directory_exists(os.path.dirname(output_textfile)) 
    n_classes = len(subtypes_list)
    threshold = float(1/n_classes)
    with open(output_textfile, 'w') as output_file:
        sys.stdout = output_file
        slide_pred_votes_dict = dict()
        slide_real_labels_dict = dict()

        base_fpr = np.linspace(0, 1, 101)
        patch_tprs = []
        slide_tprs = []
        fig = plt.figure()
        for file_idx, csv_file in enumerate(sorted(glob.glob(os.path.join(input_dir, '*.csv')))):
            print(f'\n{csv_file}\n')
            with open(csv_file, 'r') as results_file: 
                patch_labels = list()
                patch_probs = list()
                reader = csv.reader(results_file)
                for idx, line in enumerate(reader):
                    if idx==0:
                        continue
                    try:
                        file_name, predicted_label, real_label, probability, chunk  = line
                    except:
                        file_name, predicted_label, real_label, probability = line
                    patch_labels += [int(real_label)]
                    patch_prob_list = get_list_from_probability_string(probability)
                    patch_probs += [patch_prob_list]
                    
                    slide_id = get_slide_id_from_full_file_name(file_name, patch_pattern)
                    if max(patch_prob_list) > threshold:
                        if slide_id in slide_pred_votes_dict:
                            slide_pred_votes_dict[slide_id][int(predicted_label)] += 1
                        else:
                            slide_real_labels_dict[slide_id] = int(real_label)
                            slide_pred_votes_dict[slide_id] = [0]*n_classes
                            slide_pred_votes_dict[slide_id][int(predicted_label)] += 1

                patch_labels = np.array(patch_labels)
                patch_labels = one_hot(patch_labels, n_classes)
                patch_probs = np.array(patch_probs)
                print(patch_probs)
                patch_tpr = get_tpr(base_fpr, patch_labels, patch_probs, n_classes)
                patch_tprs.append(patch_tpr)
                patch_auc = auc(base_fpr, patch_tpr)
                print('patch auc = ', patch_auc)
                
                slide_votes_array = get_np_array_from_dict_values(slide_pred_votes_dict)
                slide_probs = get_probs_from_votes(slide_votes_array)
                slide_labels = get_np_array_from_dict_values(slide_real_labels_dict)
                slide_labels = one_hot(slide_labels, n_classes)
                slide_tpr = get_tpr(base_fpr, slide_labels, slide_probs, n_classes)
                slide_tprs.append(slide_tpr)
                slide_auc = auc(base_fpr, slide_tpr)
                print('slide auc = ', slide_auc)
        patch_tprs = np.array(patch_tprs)
        mean_patch_tprs = patch_tprs.mean(axis=0)
        mean_patch_auc = auc(base_fpr, mean_patch_tprs)

        slide_tprs = np.array(slide_tprs)
        mean_slide_tprs = slide_tprs.mean(axis=0)
        mean_slide_auc = auc(base_fpr, mean_slide_tprs)

        print("base_fprs:", base_fpr)
        print("mean_patch_tprs:", mean_patch_tprs)
        print("mean_slide_tprs:", mean_slide_tprs)

        print("\nmean patch auc =", mean_patch_auc)
        print("\nmean slide auc =", mean_slide_auc)

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        Path(directory_path).mkdir(parents=True, exist_ok=True)

def one_hot(arr, num_classes):
        return np.squeeze(np.eye(num_classes)[arr.reshape(-1)])

def get_slide_id_from_full_file_name(file_name, patch_pattern):
    patch_pattern_parts = patch_pattern.split('/')
    patch_pattern_slide_id_relative_index = patch_pattern_parts.index('slide') - len(patch_pattern_parts) - 1
    file_name_parts = file_name.split('/')
    return file_name_parts[patch_pattern_slide_id_relative_index]

def get_list_from_probability_string(orig_string):
    '''probability has form "[0.333 0.666]", for example. It is type str.'''
    new_list = []
    for num in orig_string[1:-2].split(' '):
        try:
            new_list.append(float(num))
        except:
            pass
    return new_list

def get_probs_from_votes(pred_votes_array):
    prob_array = []
    for votes_list in pred_votes_array:
        sum_votes = sum(votes_list)
        prob_list = (votes_list/sum_votes)
        prob_array += [prob_list] 
    return np.asarray(prob_array)

def get_np_array_from_dict_values(dictionary):
    return np.asarray(list(dictionary.values()))

def get_tpr(base_fpr, one_hot_labels, probs, n_classes):
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(one_hot_labels[:, i], probs[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += interp(all_fpr, fpr[i], tpr[i])
    mean_tpr /= n_classes
    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
    
    tpr["macro"] = interp(base_fpr, fpr["macro"], tpr["macro"])
    tpr["macro"][0] = 0.0
    return tpr["macro"]

def get_threshold_value(subtypes_list, threshold):
    if threshold is None:
        return float(1/len(subtypes_list))
    else:
        return threshold

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=''' Gets slide level accuracies ''')

    parser.add_argument('--input_dir', type=str, help='the directory that contains the csv files')
    parser.add_argument('--output_file', type=str, help='the output file where you want the results displayed')
    parser.add_argument('--subtypes_list', nargs='+', type=str, help='Space separated strings. Example: "benign malignant"')
    parser.add_argument('--patch_pattern', type=str, default='subtype/slide/magnification', help="'/' separated words describing the directory structure of the patch paths between the root dir and the patch itself.")
    parser.add_argument('--threshold', type=float, help='the default is 1/len(subtype_list)')

    args = parser.parse_args()

    threshold = get_threshold_value(args.subtypes_list, args.threshold)

    main(args.input_dir, args.output_file, args.subtypes_list, args.patch_pattern, threshold)
