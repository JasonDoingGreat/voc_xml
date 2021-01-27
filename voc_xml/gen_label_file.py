"""
Generate XML label file
"""
import os
import codecs
from xml.etree import ElementTree as ET

from .prettier import ENCODE_METHOD
from .prettier import prettify


BASIC_INFOS = ["folder", "filename", "size", ""]


def gen_labels(file_path: str, labels_dict: dict):
    """build new XML label file depends on labels_dict information

    Args:
        file_path (str): XML file absolute path
        labels_dict (dict): XML label file information, structure like:
            {
                "folder": "labels",
                "filename": "123.jpg",
                "size": {"width": "480", "height": "640", "depth": "3"},
                "segmented": "0",
                "object": [
                    {
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
                    }
                ]
            }
    """
    # some safe checks
    assert type(file_path) is str, f"file_path should be a string, not {type(file_path)}."
    assert not os.path.exists(file_path), f'{file_path} exists, will not build a new one, please check.'
    assert type(labels_dict) is dict, f'labels_dict should be a dictionary, not {type(labels_dict)}'
    if not labels_dict:
        print("labels_dict is empty, will not build XML file")
        return

    all_info_keys = list(labels_dict.keys())
    for basic_key in BASIC_INFOS:
        assert basic_key in all_info_keys, f"Requires basic information {basic_key} exist in labels_dict."

    # create the file structure
    xml_root = ET.Element("annotation")
    folder = ET.SubElement(xml_root, "folder")
    folder.text = labels_dict["folder"]

    filename = ET.SubElement(xml_root, "filename")
    filename.text = labels_dict["filename"]

    size = ET.SubElement(xml_root, "size")
    width = ET.SubElement(size, "width")
    width.text = labels_dict["size"]["width"]
    height = ET.SubElement(size, "height")
    height.text = labels_dict["size"]["height"]
    depth = ET.SubElement(size, "depth")
    depth.text = labels_dict["size"]["depth"]

    segmented = ET.SubElement(xml_root, "segmented")
    segmented.text = labels_dict["segmented"]

    for obj in labels_dict["object"]:
        cur_obj = ET.SubElement(xml_root, "object")
        name = ET.SubElement(cur_obj, "name")
        
        assert "name" in obj, "Labeled object must have a name"
        name.text = obj["name"]

        if "pose" in obj:
            pose = ET.SubElement(cur_obj, "pose")
            pose.text = obj["pose"]

        if "truncated" in obj:
            truncated = ET.SubElement(cur_obj, "truncated")
            truncated.text = obj["truncated"]

        if "difficult" in obj:
            difficult = ET.SubElement(cur_obj, "difficult")
            difficult.text = obj["difficult"]

        assert "bndbox" in obj, "Labeled object must have coordinates"
        assert "xmin" in obj, "box xmin must exist"
        assert "ymin" in obj, "box ymin must exist"
        assert "xmax" in obj, "box xmax must exist"
        assert "ymax" in obj, "box ymax must exist"

        xmin_value = float(obj["bndbox"]["xmin"])
        ymin_value = float(obj["bndbox"]["ymin"])
        xmax_value = float(obj["bndbox"]["xmax"])
        ymax_value = float(obj["bndbox"]["ymax"])

        assert 0 <= xmin_value < xmax_value, f"xmin {xmin_value} & xmax {xmax_value} appear to be abnormal value"
        assert 0 <= ymin_value < ymax_value, f"ymin {ymin_value} & ymax {ymax_value} appear to be abnormal value"

        bndbox = ET.SubElement(cur_obj, "bndbox")
        
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(xmin_value)
        
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(ymin_value)

        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(xmax_value)

        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(ymax_value)

    with codecs.open(file_path, "w", encoding=ENCODE_METHOD) as out_file:
        prettify_result = prettify(xml_root)
        out_file.write(prettify_result.decode("utf8"))
