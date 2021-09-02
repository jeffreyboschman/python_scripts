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

def main(input_dir, output_textfile, subtypes_list, patch_pattern, verbose):
    ensure_directory_exists(os.path.dirname(output_textfile)) 
    n_classes = len(subtypes_list)
    threshold = float(1/n_classes)
    with open(output_textfile, 'w') as output_file:
        sys.stdout = output_file
        base_fpr = np.linspace(0, 1, 101)
        tprs = []
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
                    slide_id = get_slide_id_from_full_file_name(file_name, patch_pattern)
                    patch_labels += [int(real_label)]
                    probability_list = get_list_from_probability_string(probability)
                    patch_probs += [probability_list]
                patch_labels = np.array(patch_labels)
                patch_labels = one_hot(patch_labels, n_classes)
                patch_probs = np.array(patch_probs)
                fpr = dict()
                tpr = dict()
                roc_auc = dict()
                for i in range(n_classes):
                    fpr[i], tpr[i], _ = roc_curve(patch_labels[:, i], patch_probs[:, i])
                    roc_auc[i] = auc(fpr[i], tpr[i])
                all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
                mean_tpr = np.zeros_like(all_fpr)
                for i in range(n_classes):
                    mean_tpr += interp(all_fpr, fpr[i], tpr[i])
                mean_tpr /= n_classes
                fpr["macro"] = all_fpr
                tpr["macro"] = mean_tpr
                roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
                
                plt.plot(fpr["macro"], tpr["macro"], 'b', alpha=0.25)
                tpr["macro"] = interp(base_fpr, fpr["macro"], tpr["macro"])
                tpr["macro"][0] = 0.0
                tprs.append(tpr["macro"])
        tprs = np.array(tprs)
        mean_tprs = tprs.mean(axis=0)
        #std = tprs.std(axis=0)
        #tprs_upper = np.minimum(mean_tprs + std, 1)
        #tprs_lower = mean_tprs - std
        print(base_fpr)
        print(mean_tprs)
        plt.plot(base_fpr, mean_tprs, 'b')
        plt.fill_between(base_fpr, tprs_lower, tprs_upper, color='grey', alpha=0.3)

        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.axes().set_aspect('equal', 'datalim')
        plt.savefig('/projects/ovcare/classification/jboschman/colour_norm/reinhard/results/fig.png', dpi=fig.dpi)
                


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


def print_slide_level_prediction(pred_votes_dict, real_labels_dict, subtypes_list):
    output = '||Slide ID||'
    for subtype in subtypes_list:
        output += f'Votes for {subtype}||'
    output += f'Predicted Label||Vote %||Real Label||Correct?||\n'
    for slide in pred_votes_dict:
        output += f'|{slide}|'
        for subtype_vote in pred_votes_dict[slide]:
            output += f'{subtype_vote}|'
        pred_int = pred_votes_dict[slide].index(max(pred_votes_dict[slide]))
        output += f'{subtypes_list[pred_int]}|'
        pred_percentage = calculate_percentage_of_list(pred_votes_dict[slide]) 
        output += f'{pred_percentage:.2f}%|'
        real_int = int(real_labels_dict[slide])
        output += f'{subtypes_list[real_int]}|'
        if real_int == pred_int: 
            output += 'Yes|\n'
        else:
            output += 'No|\n'
    print(output)

def calculate_percentage_of_list(vote_list):
    max_vote = max(vote_list)
    sum_votes = sum(vote_list)
    return float(max_vote/sum_votes)*100

def get_dict_of_predicted_labels(pred_votes_dict):
    pred_labels_dict = dict()
    for slide_id in pred_votes_dict:
        pred_labels_dict[slide_id] = pred_votes_dict[slide_id].index(max(pred_votes_dict[slide_id]))
    return pred_labels_dict

def get_np_array_from_dict_values(dictionary):
    return np.asarray(list(dictionary.values()))

def get_slide_level_accuracy(real_labels_array, pred_labels_array):
    return accuracy_score(real_labels_array, pred_labels_array)*100

def get_acc_per_subtype(conf_matrix):
    acc_per_subtype = conf_matrix.diagonal() / conf_matrix.sum(axis=0) * 100
    acc_per_subtype[np.isinf(acc_per_subtype)] = 0.0
    return acc_per_subtype

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=''' Gets slide level accuracies ''')

    parser.add_argument('--input_dir', type=str, help='the directory that contains the csv files')
    parser.add_argument('--output_file', type=str, help='the output file where you want the results displayed')
    parser.add_argument('--subtypes_list', nargs='+', type=str, help='Space separated strings. Example: "benign malignant"')
    parser.add_argument('--patch_pattern', type=str, default='subtype/slide/magnification', help="'/' separated words describing the directory structure of the patch paths between the root dir and the patch itself.")
    parser.add_argument('--verbose', action='store_true', default=False)

    args = parser.parse_args()
    
    main(args.input_dir, args.output_file, args.subtypes_list, args.patch_pattern, args.verbose)
