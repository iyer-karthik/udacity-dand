# -*- coding: utf-8 -*-
"""
@author: Karthik Iyer
"""
import data_cleaning
import numpy as np
import pickle
import select_k_best
import sys
import tester
import time
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectKBest

### Step 1:
### ---------
### First select what features we'll use. features_list is a list of strings, 
### each of which is a feature name. The first feature must be "poi" (which is 
### actually the label. ) 

### The original data set has 20 features out of which  14 features are 
### financial features and 6 are e-mail features. We remove some of the e-mail 
### features and consider the following feature list for further analysis. 

feature_list = ['poi',
                'bonus',
                'deferral_payments',
                'deferred_income',
                'director_fees',
                'exercised_stock_options',
                'expenses',
                'from_messages',
                'loan_advances',
                'long_term_incentive',
                'other',
                'restricted_stock',
                'restricted_stock_deferred',
                'salary',
                'to_messages',
                'total_payments',
                'total_stock_value',
                'bonus_to_salary',
                'bonus_to_total'] 

#### Load the dictionary containing the dataset. This dictionary has keys comprising 
#### of names of people whose data was collected. 
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Step 2: CLean the data
### ----------------------------
data_dict = data_cleaning.clean_data(data_dict)
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(data_dict, feature_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

### Step 3: Feature scaling
### -----------------------
### Scaling creates non-dimensional features so that features with larger units 
### do not have an undue influence on the classifier as would be the case if 
### the classifier uses some sort of distance measurement (such as Euclidean 
### distance) as a similarity metric.

scaler = StandardScaler()
features = scaler.fit_transform(features)

### Step 4: Model selection, validation and tuning.
t0 = time.time() # time the process!

### Create a dictionary that keeps the F1 score of the best model object chosen
### through GridSearchCV
f1_metric = {}

### Create a StratifiedShuffeSplit of the dataset which will we passed as an 
### argument to GridSearchCV through a pipeline object.
sss = StratifiedShuffleSplit(n_splits=100, test_size=0.3, random_state=0) 

### Algorithm 1: Gaussian Naive Bayes
pipeline_gnb = Pipeline([('pca', PCA()),
                         ('classify', GaussianNB())])
param_grid_gnb = [{'pca__n_components':list(range(1, 19))}]
gs_gnb = GridSearchCV(pipeline_gnb, param_grid=param_grid_gnb, scoring='f1', 
                      cv=sss)
gs_gnb.fit(features, labels)
f1_metric['Gaussian Naive Bayes'] = gs_gnb.best_score_
print "Gaussian Naive Bayes validation finished!"

### Algorithm 2: Linear Discriminant Analysis
pipeline_lda = Pipeline([('pca', PCA()),
                         ('classify', LinearDiscriminantAnalysis())])
param_grid_lda = [{'pca__n_components':list(range(1, 19))}]
gs_lda = GridSearchCV(pipeline_lda, param_grid=param_grid_lda, scoring='f1', 
                      cv=sss)
gs_lda.fit(features, labels)
f1_metric['LDA'] = gs_lda.best_score_
print "LDA cross validation finished!"

### Algorithm 3:  Logistic Regression
pipeline_lgr = Pipeline([('classify', LogisticRegression(random_state=0, 
                                                         class_weight='balanced',
                                                         penalty='l1'))
                        ])
param_grid_lgr =  [{'classify__C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}]
gs_lgr = GridSearchCV(pipeline_lgr, param_grid=param_grid_lgr, scoring='f1', 
                      cv=sss)
gs_lgr.fit(features, labels)
f1_metric['Logistic Regression'] = gs_lgr.best_score_
print "Logistic Regression validation finished!"

### Algoruthm 4:  Decision Tree with SelectKBest() preprocessing
pipeline_dt = Pipeline([
    ('select_features', SelectKBest()),
    ('classify', DecisionTreeClassifier(random_state=0, class_weight='balanced'))
])
param_grid_dt = [
    {
        'select_features__k': np.arange(1, 18), 
        'classify__criterion' : ['gini', 'entropy'],
        'classify__min_samples_split' : [2, 4, 6, 8, 10, 20],
        'classify__max_depth' : [None, 5, 10, 15, 20]
    }
]
gs_dt = GridSearchCV(pipeline_dt, param_grid=param_grid_dt, scoring='f1',
                     cv=sss)
gs_dt.fit(features, labels)
f1_metric['Decision Tree Classifer'] = gs_dt.best_score_
print "Decision Tree validation finished!"
t1 = time.time()
#t1 - t0 # Total time for tuning and validation
### Choose the best performing model
print f1_metric

### Step 5: Testing
### ----------------
### Decision Tree with certain parameters works best. Use this classifer
### object for testing. Since one of the parameters of the tuning selected
### optimal number of features, we modify the feature list to only contain
### these features. 

reduced_feature_list = select_k_best.select_k_best(data_dict, feature_list, 
                                               num_features=gs_dt.best_params_['select_features__k'])
reduced_feature_list.insert(0, 'poi')
tester.test_classifier(gs_dt.best_estimator_, data_dict, reduced_feature_list)


### Step 6: 
### ------
### Dump classifier, dataset, and features_list so anyone can check our results. 
tester.dump_classifier_and_data(gs_dt.best_estimator_, my_dataset, 
                                 reduced_feature_list)

