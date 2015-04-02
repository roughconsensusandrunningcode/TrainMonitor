import unittest
from TrainMonitor import viaggiatreno

class TestViaggiatrenoAPI(unittest.TestCase):
  def setUp(self):
    self.api = viaggiatreno.API()

  def test_region(self):
      api = viaggiatreno.API()
      reg_code = self.api.call('regione', 'S00219')
      self.assertEqual(reg_code, 3)

if __name__ == '__main__':
    unittest.main()
