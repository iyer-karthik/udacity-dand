''' Script for auditing and cleaning street names and phone numbers.
Author: Karthik Iyer'''

# UPDATE street abbreviations and city name according to the dictionary 'mapping'.
mapping = { "St": "Street",
            "St.": "Street",
            "Ave" :"Avenue",
            "Ave." :"Avenue",
            "avenue":"Avenue",
            "Rd." : "Road",
            "Rd" : "Road",
            "Pl" : "Place",
            "S" :  "South",
            "N" : "North",
            "N." : "North",
            "S." : "South",
            "N.E." : "Northeast",
            "NE" : "Northeast",
            "NW" : "Northwest",
            "SW" : "Southwest",
            "nw" : "Northwest",
            "street" : "Street",
            "E" : "East",
            "Dr" : "Drive",
            
            "seattle": "Seattle", 
            "Seattle, WA" :"Seattle"
            }

''' This function takes in a name and a dictionary and updates the returns
the 'cleaned' version of the name accroding to the dictionary map.
For instance, 'N Allen st' will be returned as 'North Allen Street'.'''

def update_name(oldname, mapping):

    new_name_list = []
    list_name = oldname.split(" ")
    for element in list_name:
        if element in mapping.keys():
            new_name_list.append(mapping[element])
        else:
            new_name_list.append(element)
    new_name = " ".join(new_name_list)
    

    return new_name

#-----------------------------------------------------------------
#Update phone numbers
#------------------------------------------------------------------

def update_phone_number(phone_number):
    '''This function takes in a string representing a phone number
    and returns the properly formatted phone number as a string.
    A properly  formatted phone number is of the form
    'xxx-xxx-xxxx' where the first 3 digits correspond to the area code.
    A helper function format_phone_numnber() is used to introduce hyphen(-) at
    the correct places. 
    
    Example: 1) 12065789000 is returned as '206-578-9000'
             2) 2065789000 is returned as '206-579-9000
             3) +1 206-578-9000 is returnd a 206-578-9000
             4) (206)-578-9000 is returned as 206-578-9000
             5) +12065789000 is retuned as 206-578-9000'''
    
    
    # create a common placeholder value for incorrect phone numbers
    default_phone_number = '000-000-0000'
    
    #Choose only the digits in the phone number string.
    stripped_number =''.join(i for i in phone_number if i.isdigit())
    
    if len(stripped_number) > 10:
        
        if stripped_number[0] == '1':
            updated_phone_number = format_phone_number(stripped_number[1:])
            return(updated_phone_number)
        
        else:
            # take care of extensions
            updated_phone_number = format_phone_number(stripped_number)
            return(updated_phone_number)
    
    elif len(stripped_number) == 10:
        
        updated_phone_number = format_phone_number(stripped_number)
        return(updated_phone_number)
    
    else:
        #incorrect phone number. Revert to default
        updated_phone_number = default_phone_number
        return(updated_phone_number)

#------------------    
# HELPER FUNCTION
#------------------    
def format_phone_number(stripped_number):
    result =''
    
    # for extensions
    if len(stripped_number) > 10:
        result = result + stripped_number[:3] +'-' + stripped_number[3:6] + '-' \
        + stripped_number[6:10] + 'x'+ stripped_number[10:]
        return(result)
    
    if len(stripped_number) == 10:
        result = result + stripped_number[:3] +'-'+ stripped_number[3:6] + '-' \
        + stripped_number[6:]
        return(result)
