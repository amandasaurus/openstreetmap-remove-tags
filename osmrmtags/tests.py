import unittest
from six import StringIO
import xml.etree.ElementTree as ET
import tempfile
import os

import osmrmtags
import osmwriter


class OSMRMtagsTestCase(unittest.TestCase):
    def testSimple(self):
        return

        # FIXME doesn't work due to imposm reording things due to it's parallelization.
        _, input_filename = tempfile.mkstemp(suffix=".osm")
        output_fp = StringIO()


        xml = osmwriter.OSMWriter(input_filename)
        xml.node(1, 10, 30, {"highway": "yes"}, version=2)
        xml.way(1, {'pub': 'yes'}, [123])
        xml.way(2, {'highway': 'motorway', "name": "Cheese Street"}, [123])
        xml.relation(1, {'type': 'boundary'}, [('node', 1), ('way', 2, 'outer')])
        xml.close()

        osmrmtags.remove_tags(input_filename, output_fp, ['highway'], close_output_fp=False)


        # Different python versions can write XML in different ways, (eg order
        # of attributes). This makes simple string comparison fail. So simple
        # parse & dump canonicalises it
        output = ET.tostring(ET.fromstring(output_fp.getvalue()))

        exected_output = ET.tostring(ET.fromstring('<?xml version="1.0" encoding="utf-8"?>\n<osm version="0.6" generator="osmwriter">\n  <node lat="10" version="2" lon="30" id="1">\n    <tag k="highway" v="yes">\n  </tag>\n  </node>\n  <way id="1">\n    <nd ref="123"></nd>\n    <tag k="highway" v="motorway"></tag>\n  </way>\n</osm>'))

        os.unlink(input_filename)

        self.assertEqual(output, exected_output)




if __name__ == '__main__':
    unittest.main()
