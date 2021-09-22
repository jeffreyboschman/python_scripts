import os
import sys
import csv
import glob
import numpy as np
import argparse
import enum
import json
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import f1_score 
from sklearn.metrics import roc_auc_score
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

def main(csv_dir, prefix, subtypes_list, patch_pattern, threshold, verbose):
    print(f'All probabilities must be greater than {threshold} in order to be considered.\n')
    for file_idx, csv_file in enumerate(sorted(glob.glob(os.path.join(csv_dir, '*.csv')))):
        print(f'\n{csv_file}\n')
        with open(csv_file, 'r') as results_file: 
                slide_pred_votes_dict = dict()
                slide_real_labels_dict = dict()
                reader = csv.reader(results_file)
            for idx, line in enumerate(reader):
                if idx==0:
                    continue
                try:
                    file_name, predicted_label, real_label, probability, chunk  = line
                except:
                    file_name, predicted_label, real_label, probability = line
                
                slide_id = get_slide_id_from_full_file_name(file_name, patch_pattern)
                probability_list = get_list_from_probability_string(probability)
                if max(probability_list) > threshold: 
                    if slide_id in slide_pred_votes_dict:
                        slide_pred_votes_dict[slide_id][int(predicted_label)]+=1
                    else:
                        slide_real_labels_dict[slide_id] = int(real_label)
                        slide_pred_votes_dict[slide_id] = [0]*len(subtypes_list) 
                        slide_pred_votes_dict[slide_id][int(predicted_label)]+=1
        if verbose:
            print_slide_level_prediction(slide_pred_votes_dict, slide_real_labels_dict, subtypes_list)

        slide_votes_array = get_np_array_from_dict_values(slide_pred_votes_dict)
        slide_probs_array = get_probs_from_votes(slide_votes_array) 
        slide_pred_labels_dict = get_dict_of_predicted_labels(slide_pred_votes_dict)
        slide_real_labels = get_np_array_from_dict_values(slide_real_labels_dict)
        slide_pred_labels = get_np_array_from_dict_values(slide_pred_labels_dict)
        conf_matrix = confusion_matrix(slide_real_labels, slide_pred_labels).T
        acc_per_subtype = get_acc_per_subtype(conf_matrix)
        average_acc = acc_per_subtype.mean()
        weighted_acc = get_slide_level_accuracy(slide_real_labels, slide_pred_labels)
        overall_slide_kappa = cohen_kappa_score(slide_real_labels, slide_pred_labels)
        overall_slide_f1 = f1_score(slide_real_labels, slide_pred_labels, average='macro')
        
        if len(subtypes_list) == 2:
            slide_auc = roc_auc_score(slide_real_labels, slide_pred_labels, average='macro')
        else:
            slide_auc = roc_auc_score(slide_real_labels, slide_probs_array, multi_class ='ovr', average='macro')
        print_confusion_matrix(conf_matrix, subtypes_list)
        print_results_summary(subtypes_list, acc_per_subtype, weighted_acc, overall_slide_kappa, overall_slide_f1, slide_auc)
        all_kappas += [overall_slide_kappa]
        all_auc += [slide_auc]
        all_average_accs += [average_acc]
    print_all(all_kappas, 'kappa')
    print_all(all_auc, 'auc')
    print_all(all_average_accs, 'average_acc')

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

def print_confusion_matrix(conf_matrix, subtypes_list):
    output = '||X||'
    for class1 in subtypes_list:
        output += f'Actual {class1}||'
    output += '\n'
    for idx_x, class2 in enumerate(subtypes_list):
        output += f'|Predicted {class2}|'
        for idx_y, class_y in enumerate(subtypes_list):
            output += f'{conf_matrix[idx_x][idx_y]}|'
        if idx_x != len(subtypes_list):
            output += '\n'
    print(output)

def get_slide_level_accuracy(real_labels_array, pred_labels_array):
    return accuracy_score(real_labels_array, pred_labels_array)*100

def get_acc_per_subtype(conf_matrix):
    acc_per_subtype = conf_matrix.diagonal() / conf_matrix.sum(axis=0) * 100
    acc_per_subtype[np.isinf(acc_per_subtype)] = 0.0
    return acc_per_subtype

def print_results_summary(subtypes_list, acc_per_subtype, weighted_acc, kappa, f1_score, auc):
    output = '||Dataset||'
    for subtype in subtypes_list:
        output += f'{subtype}||'
    output += f'Weighted Slide Acc||Slide Kappa||Slide F1 Score||Slide AUC||Avg Slide Acc||\n|X|'
    for idx, subtype in enumerate(subtypes_list):
        output += f'{acc_per_subtype[idx]:.2f}%|'
    output += f'{weighted_acc:.2f}%|{kappa:.4f}|{f1_score:.4f}|{auc:.4f}|{acc_per_subtype.mean():.2f}%|\n'
    print(output)

def print_all(metric_list, metric_name):
    num_results = len(metric_list)
    output = f'\n All {metric_name}:\n'
    for num in range(num_results):
        output += f'Set {num}  '
    output += '\n'
    for result in metric_list:
        if metric_name == 'average_acc':
            output += f'{result:.2f}  '
        else:
            output += f'{result:.4f}  '
    print(output)

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
    parser.add_argument('--verbose', action='store_true', default=False)

    args = parser.parse_args()
    
    threshold = get_threshold_value(args.subtypes_list, args.threshold) 

    main(args.input_dir, args.output_file, args.subtypes_list, args.patch_pattern, threshold, args.verbose)
