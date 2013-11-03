import pdfquery
import unittest

# to run: python -m unittest tests

class TestPDFQuery(unittest.TestCase):

    def setUp(self):
        self.pdf = pdfquery.PDFQuery("tests/sample.pdf")
        self.pdf.load()

    def test_selectors(self):
        """
            Test the :contains and :in_bbox selectors.
        """
        label = self.pdf.pq('LTTextLineHorizontal:contains("Your first name and initial")')
        self.assertEqual(len(label), 1)

        left_corner = float(label.attr('x0'))
        self.assertEqual(left_corner, 143.651)

        bottom_corner = float(label.attr('y0'))
        self.assertEqual(bottom_corner, 714.694)

        name = self.pdf.pq(
            ':in_bbox("%s, %s, %s, %s")' % (left_corner, bottom_corner - 30, left_corner + 150, bottom_corner)).text()
        self.assertEqual(name, "John E.")

    def test_extract(self):
        """
            Test the extract() function.
        """
        values = self.pdf.extract([
            ('with_parent', 'LTPage[pageid="1"]'),
            ('with_formatter', 'text'),

            ('last_name', ':in_bbox("315,680,395,700")'),
            ('spouse', ':in_bbox("170,650,220,680")'),

            ('with_parent', 'LTPage[pageid="2"]'),

            ('oath', ':contains("perjury")', lambda match: match.text()[:30] + "..."),
            ('year', ':contains("Form 1040A (")', lambda match: int(match.text()[-5:-1]))
        ])
        self.assertDictEqual(values, {
            'last_name': 'Michaels',
            'spouse': 'Susan R.',
            'oath': u'Separation 1 of 2: Black Separ...',
            'year': 2007
        })


if __name__ == '__main__':
    unittest.main()
