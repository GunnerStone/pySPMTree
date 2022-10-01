import gzip
import xml.etree.ElementTree as ET
import sys
import os

""" Takes a spm file and returns an ET xml object"""
def deserialize_spm(filepath):
    """
    Deserialize a spm file and return the xml.
    """
    if filepath.endswith('.spm'):
        with gzip.open(filepath, 'rb') as f:
            xml = f.read()
            # save the xml file to disk
    return ET.fromstring(xml)

""" Takes an Xml spm object and writes an spm file to disk"""
def serialize_spm(filepath):
    """
    Serialize an xml file and returns the spm
    """
    if filepath.endswith('.xml'):
        f_in = open(filepath)
        # replace .xml with .spm
        f_out = open(filepath.replace('.xml', '.spm'), 'w')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
    return

def get_generators(filepath):
    # deserialize the spm file and print the xml root node
    xml_root = deserialize_spm('SPM_Trees/Gunner_Pine.spm')
    generators = []
    for child in xml_root:
        if child.tag == 'Generators':
            for generator in child:
                if (generator.attrib['Type'] == 'Branch' and generator.find('Hidden').text == 'false') or generator.attrib['Type'] == 'Tree':
                    print(generator.tag, generator.attrib)
                    generators.append(generator)
    return generators

# takes in spm file, sets the generators according to the list of generators
# matches generators by GUID
def set_generators(filepath, generators):
    # deserialize the spm file and print the xml root node
    xml_root = deserialize_spm(filepath)
    for child in xml_root:
        if child.tag == 'Generators':
            length = len(child) # to prevent i replacing itself
            for generator in child[:length]:
                # check the GUID of the generator and compare with GUID's in the list
                curr_GUID = generator.find('GUID').text
                for i in generators:
                    if curr_GUID == i.find('GUID').text:
                        child.remove(generator)
                        child.append(i)
                        print("Found matching GUID: ", curr_GUID)
                        break
                        
    return xml_root


if __name__ == '__main__':
    my_generators = get_generators('SPM_Trees/Gunner_Pine.spm')
    # change the name of each generator
    for i, generator in enumerate(my_generators):
        generator.find('Name').text = 'Generator_' + str(i)    

    # set the generators in the spm file
    my_xml = set_generators('SPM_Trees/Gunner_Pine.spm', my_generators)

    # save it to disk
    with open('SPM_Trees/Gunner_Pine_deserialized.xml', 'w') as f:
        f.write(ET.tostring(my_xml, encoding='unicode'))

    # serialize the xml file and print the spm root node
    serialize_spm('SPM_Trees/Gunner_Pine_deserialized.xml')

    print("Program finished")