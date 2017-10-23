
# OpenStreetMap Data Case Study<br>
# Author: Karthik Iyer



## Introduction


### What is OpenStreetMap?

OpenStreetMap (OSM) is a collaborative project to create a free editable map of the world. Map data is collected from scratch by volunteers performing systematic ground surveys using tools such as a handheld GPS unit, a notebook, digital camera, or a voice recorder. The data is then entered into the OpenStreetMap database. Notable services using OSM include Apple Inc, Flikr, Craigslist, Tableau etc.

#### Data Format

OpenStreetMap uses a topological data structure, with four core elements (also known as data primitives):

* *Nodes* are points with a geographic position, stored as coordinates (pairs of a latitude and a longitude). 

* *Ways* are ordered lists of nodes, representing a polyline, or possibly a polygon if they form a closed loop. They are used both for representing linear features such as streets and rivers, and areas, like forests, parks, parking areas and lakes.

* *Relations* are ordered lists of nodes, ways and relations (together called "members"), where each member can optionally have a "role" (a string). Relations are used for representing the relationship of existing nodes and ways. Examples include turn restrictions on roads, routes that span several existing ways (for instance, a long-distance motorway), and areas with holes.

* *Tags* are key-value pairs (both arbitrary strings). They are used to store metadata about the map objects (such as their type, their name and their physical properties). Tags are not free-standing, but are always attached to an object: to a node, a way or a relation. A recommended ontology of map features (the meaning of tags) is [maintained on a wiki](https://wiki.openstreetmap.org/wiki/Map_features).

The raw data set that we will use is available to us an XML formatted .osm file.  To know more about the OSM XML data format and an example of how data is structured in an OSM XML file, have a look at https://wiki.openstreetmap.org/wiki/OSM_XML.

### Map area and overview of the project

In this project we choose to study the map area of Seattle, WA, United States downloaded as a custom extract XML OpenStreetMap (OSM) data set for "City of Seattle, WA, USA" from https://mapzen.com/data/metro-extracts/
(Uncompressed file size ~ 283 MB).

The primary motivatation behind this project is to go through the complete process of data munging or data wrangling.
We will process the data set, programmatically audit and clean it and convert it from XML to CSV format. We will then import the cleaned .csv files in to a SQL databse and run queries on it. 



## Raw data transformation

### Problems encountered in the OSM XML file

After initially downloading a small sample size of the Seattle area and running it against a provisional data.py file, we noticed two main problems with the data.

* Street name abbreviation inconsistencies ('*N Allen Pl*', '*North E Jefferson st*')

* Non standardized telephone numbers ("+1xxxxxxxxxx", "xxxxxxxxxx", "xxx-xxx-xxx")

We used the following techniques to programmatically clean the data.

#### Street name auditing

To deal with correcting street names or city name, we did not use regular expressions, and instead iterated over each word in an address, correcting them to their respective mappings through the use of a dictionary called *mapping* which held the old street names as keys and their updated names as values and a function *update_name( )* which accomplished the name change.




```python
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
            "N.": "North",
            "S." : "South",
            "N.E." : "Northeast",
            "NE" : "Northeast",
            "NW": "Northwest",
            "SW": "Southwest",
            "nw": "Northwest",
            "street" : "Street",
            "E" : "East",
            "Dr" : "Drive",
            
            "seattle": "Seattle", 
            "Seattle, WA" :"Seattle"
            }

def update_name(oldname, mapping):

    new_name_list=[]
    list_name = oldname.split(" ")
    for element in list_name:
        if element in mapping.keys():
            new_name_list.append(mapping[element])
        else:
            new_name_list.append(element)
    new_name = " ".join(new_name_list)
    

    return new_name
```

Thus "*N Allen Pl* becomes "*North Allen Place*" and "*North E Jefferson st*" becomes "*North East Jefferson Street*"

#### Standardizing Telephone numbers

Printing out telephone numbers from the sample OSM XML file revealed inconsistent and incorrect phone numbers. 
For instance, we had phone numbers of the type "1xxxxxxxxxx", "xxxxxxxxxx", "+1 xxx-xxx-xxxx", "(xxx)-xxx-xxxx", "+1xxxxxxxxxx" and even some incorrect/ incomplete ones like "xxx", "0", etc. 

To take care of the inconsistencies and incomplete entries, we changed all incorrect/ incomplete entries to a default phone number "000-000-0000" and all actual phone numbers to the format "xxx-xxx-xxxx" i.e the leading +1 or 1 were stripped and placeholders were introduced in the correct places. This was accomplished using the function *update_phone_number( )* and an auxillary function *format_phone_number( )* (for correct formatting).


```python
def update_phone_number(phone_number):
    '''This function takes in a string representing a phone number
    and returns the properly formatted phone number as a string.
    A properly  formatted phone number is of the form
    'xxx-xxx-xxxx' where the first 3 digits correspond to the area code.
    A helper function format_phone_numnber() is used to introduce hyphen(-) at
    the correct places. 
    
    Example: 1) '12065789000' is returned as '206-578-9000'
             2) '2065789000' is returned as '206-579-9000
             3) '+1 206-578-9000' is returnd a 206-578-9000
             4) '(206)-578-9000' is returned as 206-578-9000
             5) '+12065789000' is retuned as 206-578-9000'''
    
    
    # create a common placeholder value for incorrect phone numbers
    default_phone_number = '000-000-0000'
    
    #Choose only the digits in the phone number string.
    stripped_number =''.join(i for i in phone_number if i.isdigit())
    
    if len(stripped_number)>10:
        
        if stripped_number[0]=='1':
            updated_phone_number = format_phone_number(stripped_number[1:])
            return(updated_phone_number)
        
        else:
            # for extensions
            updated_phone_number = format_phone_number(stripped_number)
            return(updated_phone_number)
    
    elif len(stripped_number) ==10:
        
        updated_phone_number = format_phone_number(stripped_number)
        return(updated_phone_number)
    
    else:
        #incorrect phone number
        updated_phone_number = default_phone_number
        return(updated_phone_number)

#------------------    
# HELPER FUNCTION
#------------------    
def format_phone_number(stripped_number):
    result =''
    if len(stripped_number) > 10:
        # for extensions
        result = result + stripped_number[:3]+'-'+stripped_number[3:6]+'-' \
        + stripped_number[6:10] + 'x'+stripped_number[10:]
        return(result)
    
    if len(stripped_number)==10:
        result = result + stripped_number[:3]+'-'+stripped_number[3:6]+'-' \
        + stripped_number[6:]
        return(result)
```

## Preparing the data to be inserted in to a database

We now prepare the data to be inserted into a SQL database.
To do so we will parse the elements in the OSM XML file, transforming them from document format to
tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
imported to a SQL database as tables. This is accomplished in the *data.py* script.

The process for this transformation is as follows:

- Use iterparse to iteratively step through each top level element in the XML

- Shape each element into several data structures using a custom function. We will insert
  the audited data in this step. For our project, <br>as discussed before, we choose to audit the street addresses
  and properly format the phone numbers. 
  
- Utilize a schema and validation library to ensure the transformed data is in the correct format.

- Write each data structure to the appropriate .csv files.

We've already defined a schema in the *schema.py* file. Using the 
cerberus library we can validate the output against this schema to ensure it is correct.


Once this is done, we get access to.csv files which we then import to a SQL data base as tables . This step is accomplished through the script *connecttodatabase.py* (using [this](https://gist.github.com/swwelch/f1144229848b407e0a5d13fcb7fbbd6f) schema.) 


### File Sizes and Data Overview

The file sizes are as follows:

| File           |    Size       |
|----------------|:-------------:|
| nodes.csv      |  105 MB       | 
| nodes_tags.csv |  13  MB       | 
| ways.csv       |  9   MB       |
| ways_tags.csv  |  25.3 MB      |
| ways_nodes.cv  |  33.5 MB      |
| SeattleOpen    |               |
| MapData.osm    | 283 MB        |
| SeattleData.db | 159 MB        |

* **Number of nodes**
```sql
sqlite> SELECT COUNT(*) FROM nodes;
```
Answer: 1237556
 
* **Number of ways**
```sql
sqlite> SELECT COUNT(*) FROM ways;
```
Answer: 146962

* **Number of unique users**
```sql
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
Answer: 893

* **Top 10 contributing users**
```sql
sqlite> SELECT e.user, COUNT(*)  as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY  num desc
LIMIT 10;
```
Answer: 
```sql
Glassman|545896
SeattleImport|319871
seattlefyi|97524
sctrojan79|66606
jeffmeyer|51500
lukobe|37151
Sudobangbang|29970
Omnific|28002
Ballard OpenStreetMap|24423
chronomex|21970
```
* **Percentage split up of top 10 contributing users**
```sql 
sqlite> CREATE  TABLE contributing_users as
SELECT user FROM nodes
union ALL
SELECT user FROM ways;
```
```sql
sqlite> SELECT user, COUNT(*) * 100.0 /(SELECT  COUNT(*) from contributing_users) as percent
FROM contributing_users
GROUP BY user
ORDER BY percent DESC
LIMIT 10;
```
Answer: 
```sql
Glassman|39.428595366763
SeattleImport|23.1034193849412
seattlefyi|7.04389542064458
sctrojan79|4.81077169094226
jeffmeyer|3.71970606377093
lukobe|2.68331650437192
Sudobangbang|2.16465224720805
Omnific|2.02250891646046
Ballard OpenStreetMap|1.76400740185393
chronomex|1.5868338295349
```

```sql
sqlite> DROP TABLE contributing_users;
```

* **Number of users having only 1 post**

```sql
sqlite> SELECT COUNT(*) 
FROM
(SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
HAVING num=1)  u;
```
Answer: 244

#### Contributor statistics and suggestions for improvement

The contributions of users is quite skewed with the top 3 users contributing to about 70 % of the map data. Here are some user percentage statistics:

* Top user *Glassman* contribution percentage (39.43%)

* Combined Top 10 users contribution (88.32%)

* Combined Top 15 users contribution (92.24%)

* Percentage of users who only contributed once (27.32%)

We see that a good chunk of users contributed only once. OpenStreetMap should come up with a way to ensure 
that the retention rate for users is higher. One way to do that is by incentivizing users to contribute more by
providing points or having a rewards system. This will
lead to a more diverse set of contributors and as a result help reach OSM to a wider audience. 

### More SQL queries

* **Let's see the top 10 frequenty occuring keys in *nodes_tags* and *ways_tags* tables**

```sql
sqlite> SELECT tags.key, count(*) as num
FROM
(SELECT * FROM nodes_tags UNION  SELECT * FROM ways_tags) tags
GROUP BY tags.key
ORDER BY num DESC
LIMIT 10;

```
Answer:
```
source|171349
street|118054
housenumber|117983
postcode|116804
city|116750
building|109475
highway|32805
name|23344
amenity|10502
lanes|9007
```

* **How about the top 10 frequently occuring amenities?**

```sql
sqlite> SELECT tags.value, COUNT(*) as num
FROM
(SELECT * FROM nodes_tags UNION SELECT * FROM ways_tags) tags
WHERE tags.key="amenity"
GROUP BY tags.value
ORDER BY num desc
LIMIT 10;
```
Answer:

``` sql
bicycle_parking|2634
parking|2095
restaurant|1000
bench|721
cafe|549
waste_basket|532
fast_food|275
place_of_worship|250
bar|204
parking_entrance|167
```
Quite a few restaurants, cafes and bars there!

* **Let us check the top 10 different types of cuisine available in Seattle**

```sql
sqlite> SELECT tags.value, COUNT(*) as num
FROM
(SELECT * from nodes_tags UNION  SELECT * FROM ways_tags) tags
WHERE tags.key="cuisine"
GROUP BY tags.value
ORDER BY num DESC
LIMIT 10;
```
Answer:
```
coffee_shop|256
mexican|101
pizza|98
sandwich|96
american|72
thai|66
burger|58
italian|58
vietnamese|49
chinese|47
```
It is no surprise that coffee shops head that list. After all, we are talking about Seattle here!

* **Let's see the how places of worship are split by religion** 

```sql
sqlite> SELECT tags.value, count(*) as num
FROM
(SELECT * FROM nodes_tags UNION  SELECT * FROM ways_tags) tags
WHERE tags.key="religion"
GROUP BY tags.value
ORDER BY num DESC;
```
Answer:
```sql 
christian|225
buddhist|9
jewish|8
new_thought|1
religious_science|1
scientologist|1
scientology|1
```
Again, no surprise there. 

### Additional Data Exploration

* Recall that phone numbers which were incorrect in the raw data file were all standardized to a default phone number 
  000-000-0000.<br> Let's see which users erred in entering the phone numbers. 

```sql
sqlite> SELECT nodes.user, nodes.timestamp FROM
nodes JOIN nodes_tags 
ON nodes.id  = nodes_tags.id
WHERE 
(nodes_tags.key="phone"
AND nodes_tags.value="000-000-0000");
```
Answer:
```sql
sctrojan79|2015-07-30T21:30:14Z
Omnific|2016-08-31T07:52:27Z
Omnific|2016-08-31T07:52:31Z
Omnific|2016-01-28T03:33:49Z
seattlefyi|2013-11-09T23:19:02Z
Omnific|2016-08-31T07:52:26Z

sqlite> SELECT ways.user, ways.timestamp FROM
ways JOIN ways_tags 
ON ways.id  = ways_tags.id
WHERE 
(ways_tags.key="phone"
AND ways_tags.value="000-000-0000");
```
Answer:
```sql
Omnific|2016-01-28T03:33:46Z
```

* Let us now look at the top 10 sources of data

```sql
sqlite> SELECT tags.value, COUNT(*) AS num
FROM
(SELECT * FROM nodes_tags UNION  SELECT * FROM ways_tags) tags
WHERE tags.key="source"
GROUP BY tags.value
ORDER BY num DESC
LIMIT 10;
```
Answer:
```sql
King County GIS;data.seattle.gov|98633
King County GIS|31693
data.seattle.gov|31214
SDOT Bike Rack Import 2012|2152
yahoo_wms|1877
bing|1319
data.seattle.gov;King County GIS|911
PGS|835
Bing|654
survey|231
```
Majority of the data comes from a Geographical Information System (GIS) or the official city [website](https://data.seattle.gov/) which confirms the data integrity. 

However some amount of data entries are not very official but 
rather come from local knowledge as the following query reveals.

```sql
sqlite> SELECT COUNT(tags.value) FROM
(SELECT * FROM nodes_tags UNION  SELECT * FROM ways_tags) tags
WHERE tags.key="source"
AND 
(tags.value LIKE "%knowledge%" OR tags.value LIKE "%local%")
```
Answer:

```sql 
522
```

**This is a potential problem as the data entries rely
on '*local knowledge*' which is a rather unscientific way of collecting data. One way to remedy this is 
to ensure that all such data such entries, before submission, are cross verified by official sources. This will
protect the integrity of data collection.**

## Conclusion

In this project, we went about the process of data auditing and cleaning in a programmatic manner. We took a raw data file, cleaned and wrangled it. We observed that the Seattle area data is rather complete but not completely standardized which we went about achieving via Python scripts.  For the purposes of this project, we believe that the data has been well cleaned. We then ran SQL queries on the cleaned data and extracted useful information.   For the future, we can work with a more robust data processor similar  to *data.py* and input a great amount of cleaned data to [OpenStreetMap](https://www.openstreetmap.org/)

-----------------------


```python
#Custom styling for display

from IPython.core.display import display, HTML

HTML("""
<style>

div.cell { /* Tunes the space between cells */
margin-top:1em;
margin-bottom:1em;
}

div.text_cell_render h1 { /* Main titles bigger, centered */
font-size: 2.2em;
line-height:1.4em;
text-align:center;
}

div.text_cell_render h2 { /*  Parts names nearer from text */
margin-bottom: -0.3em;
}


div.text_cell_render { /* Customize text cells */
font-family: 'Times New Roman';
font-size:1em;
line-height:1.4em;
padding-left:3em;
padding-right:3em;
}
</style>
""");
```
