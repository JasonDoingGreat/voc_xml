"""
prettier library
"""
from lxml import etree
from xml.etree import ElementTree as ET


ENCODE_METHOD = "utf-8"


# create a new XML file with the results
def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, "utf8")
    root = etree.fromstring(rough_string)
    temp_string = etree.tostring(root, pretty_print=True, encoding=ENCODE_METHOD)

    return temp_string.replace(
        "  ".encode(), "\t".encode()
    )


def deprettify(elem):
    """check if the XML file has been prettified before,
       a prettified XML should have '\n\t' inside,
       if so, deprettify this file

    Args:
        elem (ElementTree): ElementTree Root
    """
    rough_string = ET.tostring(elem, "utf8").decode("utf8")
    if '\n\t' in rough_string:
        rough_string = rough_string.replace("\n", "").replace("\t", "")
        print("This XML file was prettified, will deprettify")
        return ET.fromstring(rough_string.encode("utf8"))
    else:
        print("Not prettified XML file.")
        return ET.fromstring(rough_string.encode("utf8"))
