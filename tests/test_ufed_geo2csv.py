import unittest
import xml.etree.ElementTree as et
import os

import ufed_geo2csv


class TestUfedLocation(unittest.TestCase):
    test_elem = \
        """
        <model type="Location" id="7465e04d-9569-4a12-82e9-dd714874f82e" deleted_state="Intact" decoding_confidence="High" isrelated="False" source_index="2507" extractionId="1">
            <field name="UserMapping" type="DecodingSourceOptions">
              <value type="DecodingSourceOptions"><![CDATA[Decoding]]></value>
            </field>
            <field name="Source" type="String">
              <empty />
            </field>
            <modelField name="Position" type="Coordinate">
              <model type="Coordinate" id="92cb100e-cb42-4c15-a77f-5557f7e4fdc9" deleted_state="Unknown" decoding_confidence="High" isrelated="False" source_index="2306" extractionId="1">
                <field name="UserMapping" type="DecodingSourceOptions">
                  <value type="DecodingSourceOptions"><![CDATA[Decoding]]></value>
                </field>
                <field name="Longitude" type="Double">
                  <value type="Double"><![CDATA[12.21851]]></value>
                </field>
                <field name="Latitude" type="Double">
                  <value type="Double"><![CDATA[52.3461117]]></value>
                </field>
                <field name="Elevation" type="Double">
                  <empty />
                </field>
                <field name="Comment" type="String">
                  <value type="String"><![CDATA[A Comment]]></value>
                </field>
                <field name="PositionAddress" type="String">
                  <empty />
                </field>
                <field name="Map" type="String">
                  <empty />
                </field>
              </model>
            </modelField>
            <field name="PositionAddress" type="String">
              <empty />
            </field>
            <modelField name="Address" type="StreetAddress">
              <empty />
            </modelField>
            <field name="TimeStamp" type="TimeStamp">
              <value type="TimeStamp" format="DateTimeOnly" formattedTimestamp="2020-12-16T11:53:14+01:00">2020-12-16T11:53:14.000</value>
            </field>
            <field name="Name" type="String">
              <value type="String"><![CDATA[3235326112452127.jpg]]></value>
            </field>
            <field name="Description" type="String">
              <empty />
            </field>
            <field name="Type" type="String">
              <empty />
            </field>
            <field name="Precision" type="String">
              <empty />
            </field>
            <field name="Confidence" type="Int32">
              <empty />
            </field>
            <field name="Map" type="String">
              <empty />
            </field>
            <field name="Category" type="String">
              <value type="String"><![CDATA[Media Locations]]></value>
            </field>
            <field name="Origin" type="LocationOrigin">
              <empty />
            </field>
            <field name="Account" type="String">
              <empty />
            </field>
            <jumptargets name="">
              <targetid ismodel="false"><![CDATA[148ff26d-7c38-4a04-9651-8cbd6a8ccdfb]]></targetid>
            </jumptargets>
          </model>
              """

    extra_info_matching = \
        """
        <extraInfo type="model" id="7465e04d-9569-4a12-82e9-dd714874f82e">
          <sourceInfo>
            <nodeInfos>
              <nodeInfo name="20200720_175243.jpg_embedded_1_partial.jpg" path="NO NAME/DCIM/Camera/20180720_175843.jpg/20200720_175243.jpg_embedded_1_partial.jpg" size="1590096" tableName="" offset="823" />
            </nodeInfos>
          </sourceInfo>
        </extraInfo>
        """

    extra_info_not_matching = \
        """
        <extraInfo type="model" id="39243dsb-q47e-41e3-82b5-e3000c3cefb">
          <sourceInfo>
            <nodeInfos>
              <nodeInfo name="20200720_175243.jpg_embedded_1_partial.jpg" path="NO NAME/DCIM/Camera/20180720_175243.jpg/20200720_175243.jpg_embedded_1_partial.jpg" size="1590096" tableName="" offset="823" />
            </nodeInfos>
          </sourceInfo>
        </extraInfo>
        """

    def test_lat_parsing(self):
        """
        Tests that latitude gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        ul = ufed_geo2csv.UfedLocation(xml_tree)
        self.assertEqual(ul.lat, float(52.3461117))

    def test_lon_parsing(self):
        """
        Tests that longitude gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        ul = ufed_geo2csv.UfedLocation(xml_tree)
        self.assertEqual(ul.lon, float(12.21851))

    def test_timestamp_parsing(self):
        """
        Tests that longitude gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        ul = ufed_geo2csv.UfedLocation(xml_tree)
        self.assertEqual(ul.ts, "2020-12-16T11:53:14+01:00")

    def test_category_parsing(self):
        """
        Tests that category gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        ul = ufed_geo2csv.UfedLocation(xml_tree)
        self.assertEqual(ul.category, "Media Locations")

    def test_source_parsing(self):
        """
        Tests that source entry gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        ul = ufed_geo2csv.UfedLocation(xml_tree)
        self.assertEqual(ul.name, "3235326112452127.jpg")

    def test_comment_parsing(self):
        """
        Tests that comment gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        ul = ufed_geo2csv.UfedLocation(xml_tree)
        self.assertEqual(ul.comment, "A Comment")

    def test_deleted_parsing(self):
        """
        Tests that deleted state gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        ul = ufed_geo2csv.UfedLocation(xml_tree)
        self.assertEqual(ul.deleted_state, "Unknown")

    def test_source_index_parsing(self):
        """
        Tests that source index gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        ul = ufed_geo2csv.UfedLocation(xml_tree)
        self.assertEqual(ul.deleted_state, "Unknown")

    def test_matching_extra_info_parsing(self):
        """
        Tests that extraInfo gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        extra_info_tree = et.fromstring(TestUfedLocation.extra_info_matching)
        ul = ufed_geo2csv.UfedLocation(xml_tree, extra_info_tree)
        self.assertEqual(ul.path, "NO NAME/DCIM/Camera/20180720_175843.jpg/20200720_175243.jpg_embedded_1_partial.jpg")
        self.assertEqual(ul.size, 1590096)

    def test_mismatching_extra_info_parsing(self):
        """
        Tests that extraInfo gets parsed correctly
        """
        xml_tree = et.fromstring(TestUfedLocation.test_elem)
        extra_info_tree = et.fromstring(TestUfedLocation.extra_info_not_matching)

        self.assertRaises(ufed_geo2csv.ParsingException, ufed_geo2csv.UfedLocation, xml_tree, extra_info_tree)


class TestUfedXMLParser(unittest.TestCase):
    test_report = "./tests/test_report.xml"

    def test_parse_location(self):
        """
        Tests that extraInfo gets parsed correctly
        """

        target_loc_dict = {'ts': '2020-12-16T11:53:14+01:00', 'lat': 52.3461127, 'lon': 12.21821, 'ele': None,
                           'comment': 'A Comment', 'precision': None, 'confidence': None,
                           'name': '3255326112452127.jpg', 'desc': None, 'source_index': '2306',
                           'deleted_state': 'Unknown', 'origin': None, 'account': None, 'src_idx': None,
                           'category': 'Media Locations',
                           'path': 'NO NAME/DCIM/Camera/20180720_175843.jpg/20200720_175243.jpg_embedded_1_partial.jpg',
                           'size': 1590096, 'id': '7465e04d-9569-4a12-82e9-dd714874f92e'}

        with open(os.path.abspath(TestUfedXMLParser.test_report), "r") as f:
            xml_data = f.read()

        parser = ufed_geo2csv.UfedXMLParser(xml_data)
        actual_loc = parser.parse_locations()[0].__dict__
        self.assertDictEqual(actual_loc, target_loc_dict)


if __name__ == '__main__':
    unittest.main()
