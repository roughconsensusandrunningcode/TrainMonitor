import unittest
from TrainMonitor import viaggiatreno

class TestViaggiatrenoUtils(unittest.TestCase):
    def test_station_ids(self):
        self.assertEqual(viaggiatreno.Utils.exists_station_ID('X00000'), False)
        self.assertEqual(viaggiatreno.Utils.exists_station_ID('S00219'), True)
        
        self.assertEqual(viaggiatreno.Utils.station_from_ID('S00219'), 'TORINO P.NUOVA')
        self.assertEqual(viaggiatreno.Utils.station_from_ID('X00000'), 'UNKNOWN')
        

class TestViaggiatrenoAPI(unittest.TestCase):
  def setUp(self):
    self.api = viaggiatreno.API()

  def test_region(self):
      api = viaggiatreno.API()
      reg_code = self.api.call('regione', 'S00219')
      self.assertEqual(reg_code, 3)

if __name__ == '__main__':
    unittest.main()
