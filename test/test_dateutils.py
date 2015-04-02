import unittest
import datetime
from TrainMonitor import dateutils

class TestDateutils(unittest.TestCase):
    def test_easter(self):
        easter = {
            2010: datetime.date(2010, 4, 4),
            2011: datetime.date(2011, 4, 24),
            2012: datetime.date(2012, 4, 8),
            2013: datetime.date(2013, 3, 31),
            2014: datetime.date(2014, 4, 20),
            2015: datetime.date(2015, 4, 5),
            2016: datetime.date(2016, 3, 27),
            2017: datetime.date(2017, 4, 16),
            2018: datetime.date(2018, 4, 1),
            2019: datetime.date(2019, 4, 21),
            2020: datetime.date(2020, 4, 12)
        }
        for year in easter:
            self.assertEqual(easter[year], dateutils.easter(year))
            
    def test_is_holiday(self):
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
        
        date = datetime.date(2015, 1, 1)
        oneday = datetime.timedelta(1)
        while date.year == 2015:
            self.assertEqual(dateutils.is_holiday(date), date in italian_holidays_2015, date.isoformat())
            date += oneday

    def test_is_weekend(self):
        testdates = {
            datetime.date(2015, 4, 1):  False, #Wed
            datetime.date(2015, 4, 2):  False, #Thu
            datetime.date(2015, 4, 3):  False, #Fri
            datetime.date(2015, 4, 4):  True,  #Sat
            datetime.date(2015, 4, 5):  True,  #Sun
            datetime.date(2015, 4, 6):  False, #Mon
            datetime.date(2015, 4, 7):  False, #Tue
            datetime.date(2015, 4, 8):  False, #Wed
            datetime.date(2015, 4, 9):  False, #Thu
            datetime.date(2015, 4, 10): False, #Fri
            datetime.date(2015, 4, 11): True,  #Sat
            datetime.date(2015, 4, 12): True,  #Sun
        }

        for date in testdates:
            self.assertEqual (testdates[date], dateutils.is_weekend(date))

    def __test_iter_month (self, year, month, monthdays):
        l = list(dateutils.iter_month(year, month))
        n = len(l)
        self.assertEqual(n, monthdays)
        days = [d.day for d in l]
        self.assertEqual(days, list(range(1, n+1)))
        
    def test_iter_month(self):
        self.__test_iter_month(2015, 1, 31)
        self.__test_iter_month(2015, 2, 28)
        self.__test_iter_month(2015, 3, 31)
        self.__test_iter_month(2015, 4, 30)
        self.__test_iter_month(2012, 2, 29)

if __name__ == '__main__':
    unittest.main()
