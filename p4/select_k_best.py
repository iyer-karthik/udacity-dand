# -*- coding: utf-8 -*-
"""
@author: Karthik Iyer
"""
from feature_format import featureFormat, targetFeatureSplit
from sklearn.feature_selection import SelectKBest
def select_k_best(data_dict, feature_list, num_features):
    """
    Function for selecting our KBest features.
    :param data_dict: List of employees and features
    :param feature_list: List of features to select
    :param num_features: Number (k) of features to select in the algorithm.
    :return: Returns a list of the KBest feature names
    """
    data = featureFormat(data_dict, feature_list)
    target, features = targetFeatureSplit(data)
    
    # First scale the data. 
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    features = scaler.fit_transform(features)

    clf = SelectKBest(k=num_features)
    clf = clf.fit(features, target)
    feature_weights = {}
    for idx, feature in enumerate(clf.scores_):
        feature_weights[feature_list[1:][idx]] = feature
    best_features = sorted(feature_weights.items(), key = lambda k: k[1], reverse = True)[:num_features]
    new_features = []
    for k, v in best_features:
        new_features.append(k)
    return new_features