#!/usr/bin/python3

__author__ = "6ru"
__version__ = "0.0.1"

import argparse
import csv
import sys
import os
import logging
import xml.etree.ElementTree as et

logger = logging.getLogger()


class ParsingException(Exception):
    pass


class UfedLocation:
    def __init__(self, loc_model, extra_info=None, ns=""):
        """
        Takes a <model type="Location" ElementTree elem to parse and enrich the contained data.

        :param loc_model: xml element <model type="Location" ...
        """

        # Init member vars
        self.ts = None
        self.lat = None
        self.lon = None
        self.ele = None
        self.comment = None
        self.precision = None
        self.confidence = None
        self.name = None
        self.desc = None
        self.source_index = None
        self.deleted_state = None
        self.origin = None
        self.account = None
        self.src_idx = None
        self.category = None

        # ExtraInfo
        self.path = None
        self.size = None
        self.id = loc_model.attrib.get("id")

        self.process_coord_elem(loc_model, ns)
        self.process_fields(loc_model, ns)

        if extra_info:
            ei_id = extra_info.attrib.get("id")
            if ei_id == self.id:
                self.process_extra_info(extra_info, ns)
            else:
                raise ParsingException(f"IDs mismatch: {self.id} - {ei_id}")

    def process_fields(self, loc_model, ns):
        # Extract source info and timestamp
        fields = loc_model.findall(f"{ns}field")
        for f in fields:
            try:
                if f.attrib.get("name") == "Name":
                    self.name = f.find(f"{ns}value").text
                elif f.attrib.get("name") == "Category":
                    # <field name="Category"
                    self.category = f.find(f"{ns}value").text
                elif f.attrib.get("name") == "Account":
                    # <field name="Category"
                    self.category = f.find(f"{ns}value").text
                elif f.attrib.get("name") == "Precision":
                    # <field name="Precision" type="String">
                    self.precision = f.find(f"{ns}value").text
                elif f.attrib.get("name") == "Confidence":
                    # <field name="Confidence" type="Int32">
                    self.confidence = int(f.find(f"{ns}value").text)
                elif f.attrib.get("name") == "TimeStamp":
                    if not self.ts:  # Fallback to unformatted
                        val_elem = f.find(f"{ns}value")
                        self.ts = val_elem.attrib.get("formattedTimestamp")
                        if not self.ts:
                            self.ts = val_elem.text
            except AttributeError as e:
                # <empty /> was found instead of <value type="...
                pass

    def process_extra_info(self, extra_info, ns):
        nodes_info_elems = extra_info.findall(f"{ns}sourceInfo/{ns}nodeInfos/{ns}nodeInfo")

        for ni in nodes_info_elems:
            self.path = ni.attrib.get("path")
            self.size = int(ni.attrib.get("size"))

    def process_coord_elem(self, loc_model, ns):
        # Get <modelField name="Position" type="Coordinate"> child elements
        coord_elem = loc_model.find(f"{ns}modelField")

        # If coords are there, extract lat/lon
        if coord_elem.attrib.get("name") == "Position" and coord_elem.attrib.get("type") == "Coordinate":
            coord_model = coord_elem.find(f"{ns}model")

            # < model type = "Coordinate" deleted_state="Unknown" decoding_confidence="High" source_index="4604"
            if coord_model and coord_model.get("type") == "Coordinate":
                self.deleted_state = coord_model.attrib.get("deleted_state")
                self.source_index = coord_model.attrib.get("source_index")

                for field in coord_model:
                    try:  # Catch AttributeErrors on missing values
                        if field.attrib.get("name") == "Latitude":
                            # <field name="Latitude" type="Double"> ...
                            val = field.find(f"{ns}value")
                            self.lat = float(val.text)
                        elif field.attrib.get("name") == "Longitude":
                            # <field name="Longitude" type="Double"> ...
                            val = field.find(f"{ns}value")
                            self.lon = float(val.text)
                        elif field.attrib.get("name") == "Elevation":
                            # <field name="Elevation" type="Double"> ...
                            val = field.find(f"{ns}value")
                            self.ele = float(val.text)
                        elif field.attrib.get("name") == "Comment":
                            # <field name="Comment" type="String"> ...
                            val = field.find(f"{ns}value")
                            self.comment = val.text
                    except AttributeError:
                        pass


class UfedXMLParser:

    UFED_XMLNS = r"http://pa.cellebrite.com/report/2.0"

    def __init__(self, xml_data):

        self.xml_tree = et.ElementTree(et.fromstring(xml_data))
        # See https://medium.datadriveninvestor.com/getting-started-using-pythons-elementtree-to-navigate-xml-files-dc9bc720eaa6
        self.ns = f"{{{self.UFED_XMLNS}}}"  # has to be enclodes in curly braces

    def parse_locations(self):

        locs = []

        # Queries all models of type location
        models = self.xml_tree.findall(f"./{self.ns}decodedData/{self.ns}modelType/{self.ns}model/[@type='Location']")

        # Processes each model with its 'ExtraInfo' data, if existent
        for m in models:
            # Retrieves id of model-element
            id = m.attrib.get("id")

            # Queries ExtraInfo with matching id
            extra_info = self.xml_tree.find(f"./{self.ns}extraInfos/{self.ns}extraInfo/[@id='{id}']")

            # Parses model element and extraInfo elem
            ul = UfedLocation(m, extra_info=extra_info, ns=self.ns)

            locs.append(ul)

        return locs

    @staticmethod
    def transform_locs_to_csv(locs):
        # Prints results as csv to stdout
        csv_cols = list(vars(locs[-1]).keys())
        try:
            writer = csv.DictWriter(sys.stdout, fieldnames=csv_cols)
            writer.writeheader()

            # Forms rows and print to stdout
            for l in locs:
                writer.writerow(l.__dict__)

        except IOError:
            print("Error printing results to stdout")
            return 1
        return 0


def main(report=None):
    xml_data = None

    # Checks, if interactive session or reading from a file
    if sys.stdin.isatty():
        if not report.name == "<stdin>":
            with open(report.name, "r") as f:
                xml_data = f.read()
        else:
            exit("Supply report via STDIN or file!")
    else:
        xml_data = sys.stdin.read()

    # Parse XML
    parser = UfedXMLParser(xml_data)
    locs = parser.parse_locations()

    UfedXMLParser.transform_locs_to_csv(locs)


def parse_args():
    parser = argparse.ArgumentParser(description='Parser to extract geolocation from UFEDs XML Report.')

    # Report XML exported by UFED PA, which should be processed
    parser.add_argument('report', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()
    main(**vars(args))
