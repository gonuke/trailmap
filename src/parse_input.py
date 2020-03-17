import os
import sys
import subprocess
import json
import xml.etree.ElementTree as ET
import cyclus


def parse_input(input, commodity_dictionary):
    '''
    archetype_commods = parse_input(input, commodity_dictionary)

    inputs:
        - input: a Cyclus XML input file
        - commodity_dictionary: a dictionary with the Cyclus archetypes
        available and the archetype tags of their incommodities and
        outcommodities

    outputs:
        - facility_dictionary: a dictionary of each facility and its
        incommodities and outcommodities. format:
        {'facility' : (['incommodities'], ['outcommodities'])}
    '''

    tree = ET.parse(input)
    root = tree.getroot()

    facilities = get_facility_names(root)
    archetypes_in_input = archetypes_in_input_file(root)

    facility_dictionary = facility_commods(facilities, archetypes_in_input,
                                           commodity_dictionary)

    return facility_dictionary


def get_facility_names(root):
    '''
    facilities = get_facility_names(root)

    get_facility_names reads a Cyclus input file element tree and finds the
    facility names for each facility specified in a <facility> tag.

    inputs:
        - root: an xml.etree.ElementTree root of a Cyclus input file tree

    outputs:
        - facilities: a list of facility names specified in the input file
    '''

    facilities = []
    for facility in root.findall('./facility/name'):
        facilities.append(facility.text)

    return facilities


def archetypes_in_input_file(root):
    '''
    input_archetypes = archetypes_in_input_file(root)

    archetypes_in_input_file reads a Cyclus input file element tree and finds
    the modules and archetypes that are defined in the <archetypes> tag.

    inputs:
        - root: an xml.etree.ElementTree root of a Cyclus input file tree

    outputs:
        - archetypes_in_input: a dictionary with format
                               {'archetype' : 'module::archetype'}
    '''

    archetypes_in_input = {}
    for archetypes in root.findall('./archetypes/'):
        for library in archetypes.findall('./lib'):
            lib = library.text
        for name in archetypes.findall('./name'):
            name = name.text

        library_and_archetype = (':%s:%s' % (lib, name))
        archetypes_in_input[name] = library_and_archetype

    return archetypes_in_input
