"""
Code copied from Udacity's given sample code.
"""

'''We use the following code to take a systematic sample of elements from our 
original OSM file. Try changing the value of k so that  resulting 
SAMPLE_FILE ends up at different sizes. When starting out, try using a 
larger k, then move on to an intermediate k before processing your 
whole dataset. We do this primarily to test our scripts with a smaller data set
before we try our scripts on our actual data set.'''

import xml.etree.cElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "SeattleOpenStreetMapData.osm"  
SAMPLE_FILE = "SampleStreetMapData.osm"

k = 100 # Parameter: take every k-th top level element


'''Only look at  'node', 'way' and 'relation' as these are the map
elments. All of the above can have one or more associated tags 
(which describe the meaning of a particular element).

Reference:
http://wiki.openstreetmap.org/wiki/Elements'''

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write(b'<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write(b'</osm>')