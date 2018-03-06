
**Overview**

The Enron fraud is a big, messy and totally fascinating story about corporate malfeasance of nearly every imaginable type. 
The goal of this project is to build a person of interest (POI) classifier from the Enron dataset which comprises of financial 
and e-mail data of around 150 persons whose records were made public during the subsequent federal hearings.  Based on the various 
financial and e-mail features, the objective is to build a classification model that separates POIs from non POIs. The classification model is 
to achieve a precision and recall of greater than 0.3. 

**Scripts**

*data_cleaning.py* - Cleans and fixes the data associated with Enron Dataset. 

*fix_records.py* - Fixes out of sync records of Robert Belfer and Sanjay Bhatnagar. 

*main.py* - Run this file. Contains the code for feature selection, validation and parameter tuning. Also, selects the 
best model and calls the testing script. 

*poi_email_addresses.py* - List of e-mail addresses associated with people in the Enron data set. 

*select_k_best.py* - Script for selecting K best features using the ANOVA F-value between label and feature. 

*tester.py* - A basic script for checking the results of the classification model. Requires that the algorithm, dataset, and features list
 be written to my_classifier.pkl, my_dataset.pkl, and my_feature_list.pkl, respectively.This process should happen at the end of *main.py*. 


