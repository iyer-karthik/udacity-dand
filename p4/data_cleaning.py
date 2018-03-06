# -*- coding: utf-8 -*-
"""
@author: Karthik Iyer
"""
#import pandas as pd 
import fix_records
def clean_data(data_dict):
    """ 
    Clean the data associated with the Enron Data set.
        
    :param : data_dict; dictionary
    :return: data_dict with the updated values
    """
    
    ### Summary description of the raw data
#    df = pd.DataFrame.from_dict(data_dict, orient='index')
#    print df.describe()
    
    ### Step 1: Remove two data entries which give no new information (TOTAL) or
    ### are possible data entry errors (THE TRAVEL AGENCY IN THE PARK)
    for key in ["TOTAL", "THE TRAVEL AGENCY IN THE PARK"]:
        data_dict.pop(key, 0)
        
    ### Step 2: Remove any entry whose all features are NaN. Check is the no of
    ### NaNs for an entry is one less than the length (one 'feature' is "poi"). 
    for key in data_dict.keys():
        if data_dict[key].values().count('NaN') == len(data_dict[key].values()) - 1:
            data_dict.pop(key, 0)
    
    ### Step 3: Let us now check if the features have been entered correctly. 
    ### Note that on spot checking with the pdf, only two features are allowed 
    ### to take negative values, 'deferred_income' and 'restricted_stock_deferred'.
    ### Any data entry that has negative values for features not in the above 
    ### list merit a closer look. 
    check_once_more = []
    for key in data_dict.keys():
        for k, v in data_dict[key].items():
            if isinstance(v, int) and v < 0 and k not in  \
            ['deferred_income', 'restricted_stock_deferred']:
                    check_once_more.append(key)
    check_once_more = list(set(check_once_more))
    
    ### Step 4: Fix the entries flagged by Step 3. Two entries are flagged.
    data_dict = fix_records.fix_belfer(data_dict)
    data_dict = fix_records.fix_bhatnagar(data_dict)
    
    ### Step5: Add new features. Maintain consistency across all feature 
    ### entries by making incorrect or missing entries as 'NaN'
    for key in data_dict.keys():
        if data_dict[key]['bonus'] != 'NaN' and data_dict[key]['salary'] != 'NaN':
            data_dict[key]['bonus_to_salary'] = \
            float(data_dict[key]['bonus'])/data_dict[key]['salary']
        else:
            data_dict[key]['bonus_to_salary'] = 'NaN'


        if data_dict[key]['bonus'] != 'NaN' and data_dict[key]['total_payments'] != 'NaN' and data_dict[key]['total_stock_value'] != 'NaN':
            data_dict[key]['bonus_to_total'] = \
            float(data_dict[key]['bonus'])/(data_dict[key]['total_payments'] + data_dict[key]['total_stock_value']) 
        else:
            data_dict[key]['bonus_to_total'] = 'NaN'
            
    return data_dict
