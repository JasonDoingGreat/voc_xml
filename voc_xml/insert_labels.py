"""
Insert new labels into existing XML files
"""
import os
import codecs
from typing import List
from xml.etree import ElementTree as ET

from .prettier import ENCODE_METHOD
from .prettier import prettify, deprettify


def insert_labels(file_path: str, labels_list: List[dict]):
    """Insert object labels into existing label XML

    Args:
        file_path (str): existing label XML file path, should be absolute path
        labels_list (List[dict]): new objects label information,
                labels_list structure like this:
                    [{
                        "name": "object",
                        "pose": "Unspecified",
                        "truncated": "0",
                        "difficult": "0",
                        "bndbox": {
                            "xmin": str(top-left x coordinate),
                            "ymin": str(top-left y coordinate),
                            "xmax": str(bottom-right x coordinate),
                            "ymax": str(bottom-right y coordinate),
                        }
                     },
                     ...
                    ]
    """
    # some safe checks
    assert type(file_path) is str, f"file_path should be a string, not {type(file_path)}"
    assert os.path.exists(file_path), f'{file_path} does not exist'
    assert type(labels_list) is list, f'labels_list should be a list, not {type(labels_list)}'
    if len(labels_list) == 0:
        print("labels_list is empty, will not change XML file")
        return

    # parse XML file
    xml_root = ET.parse(file_path).getroot()

    # check and deprettify
    xml_root = deprettify(xml_root)
    
    # Build and append new components to XML root
    for obj in labels_list:
        # check if obj is dictionary
        assert type(obj) is dict, f'label information should be dictionary, not {type(obj)}'

        cur_obj = ET.SubElement(xml_root, "object")
        name = ET.SubElement(cur_obj, "name")
        name.text = obj["name"]

        pose = ET.SubElement(cur_obj, "pose")
        pose.text = obj["pose"]

        truncated = ET.SubElement(cur_obj, "truncated")
        truncated.text = obj["truncated"]

        difficult = ET.SubElement(cur_obj, "difficult")
        difficult.text = obj["difficult"]

        bndbox = ET.SubElement(cur_obj, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = obj["bndbox"]["xmin"]

        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = obj["bndbox"]["ymin"]

        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = obj["bndbox"]["xmax"]

        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = obj["bndbox"]["ymax"]
    
    with codecs.open(file_path, "w", encoding=ENCODE_METHOD) as out_file:
        prettify_result = prettify(xml_root)
        out_file.write(prettify_result.decode("utf8"))
