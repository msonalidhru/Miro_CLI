# Import dependencies
import unittest
import mirocli as mc

# Inherit from unittest.TestCase
class TestMiroCli(unittest.TestCase):
    # Class intialization
    def setUp(self):
        self.jsonFile = '/Miro/Miro_CLI/data.json'
    
    def test_invalidJSONfile(self):
        # Test file doesnt exists
        #print("----- Testing: File doesnt exist -----")
        with self.assertRaises(Exception) as context:
            mc.loadJson('/Miro/Miro_CLI/ta1.json')
        self.assertTrue('JSON file not valid.' in str(context.exception))
        
        #print("----- Testing: File exists but not a JSON -----")
        with self.assertRaises(Exception) as context:
            mc.loadJson('/Miro/Miro_CLI/data/mirocli.py')
        self.assertTrue('JSON file not valid.' in str(context.exception))
    
    def test_loadJSON(self):
        #"----- Load a Valid JSON -----"
        self.df = mc.loadJson('/Miro/Miro_CLI/data.json')
        self.assertTrue(len(self.df) > 0)
        
        #"----- Check Invalid Key Names -----"
        with self.assertRaises(KeyError) as context:
            mc.getGameComplete(self.df['1modules'])
        self.assertTrue('1modules' in str(context.exception))
        
        #---- Valid Key name -----
        self.dfModules = mc.getGameComplete(self.df['modules'])
        self.assertTrue(len(self.dfModules) > 0)
        
        #---- Filter only unfriendly -----
        self.dfUnf = mc.getTargetUnfriendly(self.dfModules)
        self.assertTrue(len(self.dfUnf) > 0)
        
        #--- Check if finishTime is corrupted there should be exception -----
        self.dfUnf['finishTime'] = "XX"
        with self.assertRaises(Exception) as context:
            mc.calculateAvgResponse(self.dfUnf)
        self.assertTrue('TypeError' in str(context.exception))
        
        
if __name__ == '__main__':
    unittest.main()