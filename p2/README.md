In this project, we choose the city of Seattle from https://www.openstreetmap.org and use data munging techniques,<br> 
such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity, 
to clean the OpenStreetMap data. The project comprises of the following files.

__Python Scripts__

1. _getsampleosm.py_ - Take a systematic sample of elements from the original OSM file.

2. _cleaning.py_ - Programmatically clean the street names and phone numbers


3. _data.py_ - Parse the elements in the OSM XML file, transforming them from document format to tabular format,<br> 
thus making it possible to write to .csv files. Also validates the output against a given schema to ensure it is correct.


4. _schema.py_ - A dictionary that prescribes the structure of the .csv files that are generated in the data.py script.

5. _connecttodatabase.py_
Create a database files out of .csv files which will act as tables of the SQL database.<br> 
Use this schema (https://gist.github.com/swwelch/f1144229848b407e0a5d13fcb7fbbd6f)

__Markdown__

_final_project_ 

Final project report

__OSM file__

*SampleStreetMapData.osm*

Sample OSM file extracted from the original OSM file. Used for testing the code on 
subset of the original data

__Map Area__

*MapArea.txt*

Information about the area chosen from OpenStreetMap for the project.
