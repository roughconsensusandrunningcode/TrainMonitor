import unittest
from TrainMonitor import viaggiatreno
import datetime

class TestViaggiatrenoUtils(unittest.TestCase):
    def test_station_ids(self):
        self.assertEqual(viaggiatreno.Utils.exists_station_ID('X00000'), False)
        self.assertEqual(viaggiatreno.Utils.exists_station_ID('S00219'), True)
        
        self.assertEqual(viaggiatreno.Utils.station_from_ID('S00219'), 'TORINO P.NUOVA')
        self.assertEqual(viaggiatreno.Utils.station_from_ID('X00000'), 'UNKNOWN')

    def test_train_runs_on_date_suspended(self):
        train_info = {'runs_on': 'G', 'suspended': [('2015-08-09', '2015-08-12')]}
        testdates = {
            datetime.date(2015, 8, 7):  True,
            datetime.date(2015, 8, 8):  True,
            datetime.date(2015, 8, 9):  False,
            datetime.date(2015, 8, 10): False,
            datetime.date(2015, 8, 11): False,
            datetime.date(2015, 8, 12): False,
            datetime.date(2015, 8, 13): True,
            datetime.date(2015, 8, 14): True,
        }
        for date in testdates:
            result = viaggiatreno.Utils.train_runs_on_date(train_info, date)
            self.assertEqual(result, testdates[date], date)
        
    def test_train_runs_on_date(self):
        italian_holidays_2015 = (
            datetime.date(2015, 1, 1),
            datetime.date(2015, 1, 6),
            datetime.date(2015, 4, 25),
            datetime.date(2015, 5, 1),
            datetime.date(2015, 6, 2),
            datetime.date(2015, 8, 15),
            datetime.date(2015, 11, 1),
            datetime.date(2015, 12, 8),
            datetime.date(2015, 12, 25),
            datetime.date(2015, 12, 26),
            datetime.date(2015, 4, 5),
            datetime.date(2015, 4, 6)
        )
        workdays = (
            datetime.date(2015, 4, 1),  #Wed
            datetime.date(2015, 4, 2),  #Thu
            datetime.date(2015, 4, 3),  #Fri
            datetime.date(2015, 4, 7),  #Tue
            datetime.date(2015, 4, 8),  #Wed
            datetime.date(2015, 4, 9),  #Thu
            datetime.date(2015, 4, 10), #Fri
            datetime.date(2015, 4, 13)  #Mon
        )
        saturdays = (
            datetime.date(2015, 2, 28), 
            datetime.date(2015, 4, 11), 
            datetime.date(2015, 4, 18)
        )
        sundays = (
            datetime.date(2015, 3, 1),
            datetime.date(2015, 4, 12),
            datetime.date(2015, 4, 19)
        )
        
        testcases = {}
        # G    Runs every day
        # FER5 Runs only Monday to Friday (holidays excluded)
        # FER6 Runs only Monday to Saturday (holidays excluded)
        # FEST Runs only on Sunday and holidays
        for date in italian_holidays_2015:
            testcases[(date, 'G')] = True
            testcases[(date, 'FER6')] = False
            testcases[(date, 'FER5')] = False
            testcases[(date, 'FEST')] = True
        for date in workdays:
            testcases[(date, 'G')] = True
            testcases[(date, 'FER6')] = True
            testcases[(date, 'FER5')] = True
            testcases[(date, 'FEST')] = False
        for date in saturdays:
            testcases[(date, 'G')] = True
            testcases[(date, 'FER6')] = True
            testcases[(date, 'FER5')] = False
            testcases[(date, 'FEST')] = False
        for date in sundays:
            testcases[(date, 'G')] = True
            testcases[(date, 'FER6')] = False
            testcases[(date, 'FER5')] = False
            testcases[(date, 'FEST')] = True
                        
        for date, runs_on in testcases:
            train_info = {'runs_on': runs_on}
            result = viaggiatreno.Utils.train_runs_on_date(train_info, date)
            self.assertEqual(result, testcases[(date, runs_on)], '{0} {1}'.format(date, runs_on))

class TestViaggiatrenoAPI(unittest.TestCase):
  def setUp(self):
    self.api = viaggiatreno.API()

  def test_region(self):
      api = viaggiatreno.API()
      reg_code = self.api.call('regione', 'S00219')
      self.assertEqual(reg_code, 3)

if __name__ == '__main__':
    unittest.main()
