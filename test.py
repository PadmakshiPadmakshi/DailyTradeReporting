"""
Test the code for the tech test solution.
"""
import unittest
from models import Instruction, Reporting, DATA_FIELDS

class DailyTradingReport(unittest.TestCase):
    def test_Instruction(self):
        """Test the Instruction object, which represents a single Buy or Sell
        instruction from a client.
        """
        i = Instruction()
        assert isinstance(i, Instruction),"Instruction is an Instruction"

        for afield in DATA_FIELDS:
            assert bool(type(getattr(i, afield))) == True, \
                "Instruction has a {} slot".format(afield)

    def test_Reporting(self):
        """Test the top-level Reporting object, which holds the data and reports on it.
        """
        r = Reporting()
        assert isinstance(r, Reporting),"Reporting is an Reporting"

        for zmeto in ['add_data','report_amount_settled_every_day',
                     'report_rank_entities']:
            assert getattr(r, zmeto, None) is not None, \
                "Reporting has the {} attribute/method".format(zmeto)

        
if __name__ == '__main__':
    unittest.main()
