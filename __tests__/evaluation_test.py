import unittest
import os
# module
from src.evaluation import Evaluation

class Setup:

    def setup_save_average_as_plot(self, path):
        os.mkdir(path)

class Teardown:

    def tear_down_save_average_as_plot(self, path, file_path):
        os.remove(file_path)
        os.rmdir(path)

class TestEvaluation(unittest.TestCase):

    def test_split_array_to_smaler_arrays(self):
        input = [0,1,2,4,5,6,7,8,9,10,11,12,13,14]
        expectedOutput = [[0,1,2,4,5,6,7],
                          [8,9,10,11,12,13,14]]
        output = Evaluation().split_array_to_smaler_arrays(input, 7)
        self.assertEqual(list(output), expectedOutput)

    def test_calculate_average(self):
        week = {
            "Monday":[1,2,3,4,5,6,7,8,9,10]
        }
        expectedOutput = 5.5

        self.assertEqual(Evaluation().calculate_average("Monday", week), expectedOutput)

    def test_save_average_as_plot(self):
        path = "./__tests__/average_test/"
        file_path = path + "test_save_average_as_plot.png"

        Setup().setup_save_average_as_plot(path)
        evaluation = Evaluation()

        all_new_infections_from_db = [
            '1', '10', '19', '2', '31',
            '29', '37', '66', '220', '188', 
            '129', '241', '136', '281', '451',
            '170', '1597', '910', '1210', '1477',
            '1985', '3070', '2993', '4528', '2365',
            '2660', '4183', '3930', '4337', '6615', 
            '6933', '6824', '4400', '4790', '4923', 
            '6064', '6922', '6365', '4933', '4031', 
            '3251', '4289', '5633', '4885', '3990', 
            '2737', '2946', '2218', '1287', '3394', 
            '2945', '3699', '1945', '1842', '1881', 
            '1226', '2357', '2481', '1870', '1514', 
            '1257', '988', '1154', '1627', '1470', 
            '1068', '890', '697', '488', '855'
        ]
        evaluation.evaluate_average_per_day(all_new_infections_from_db)
        evaluation.save_average_as_plot(file_path)

        expectedOutput = ["test_save_average_as_plot.png"]
        self.assertTrue(os.listdir(path), expectedOutput)

        Teardown().tear_down_save_average_as_plot(path, file_path)

if __name__ == '__main__':
    unittest.main()