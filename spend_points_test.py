import unittest
from spend_points import read_csv, cal_tot_balance, cal_result


TEST_CASE1 = {
    "true_records": [
        ("DANNON",1000,"2020-11-02T14:00:00Z"),
        ("UNILEVER",200,"2020-10-31T11:00:00Z"),
        ("DANNON",-200,"2020-10-31T15:00:00Z"),
        ("MILLER COORS",10000,"2020-11-01T14:00:00Z"),
        ("DANNON",300,"2020-10-31T10:00:00Z")
    ],
    "true_sorted_records": [
        ("DANNON",300,"2020-10-31T10:00:00Z"),
        ("UNILEVER",200,"2020-10-31T11:00:00Z"),
        ("DANNON",-200,"2020-10-31T15:00:00Z"),
        ("MILLER COORS",10000,"2020-11-01T14:00:00Z"),
        ("DANNON",1000,"2020-11-02T14:00:00Z")
    ],
    "true_tot_balance": {
        "DANNON": 1100,
        "UNILEVER": 200,
        "MILLER COORS": 10000
    }
}

class TestReadCSV(unittest.TestCase):

    def test_wrong_header(self):
        with self.assertRaises(ValueError):
            read_csv('test_csv/test1_wrong_header.csv')

    def test_wrong_data(self):
        with self.assertRaises(ValueError):
            read_csv('test_csv/test2_wrong_data.csv')

    def test_missed_data(self):
        with self.assertRaises(ValueError):
            read_csv('test_csv/test3_missed_data.csv')

    def test_read_data(self):
        records = read_csv('test_csv/demo.csv')
        self.assertEqual(records, TEST_CASE1['true_records'])

class TestCalBalance(unittest.TestCase):

    def test_violate_rule(self):
        with self.assertRaises(ValueError):
            cal_tot_balance([("DANNON",-200,"2020-10-31T15:00:00Z")])

    def test_balance(self):
        balance = cal_tot_balance(TEST_CASE1['true_records'])
        self.assertEqual(balance, TEST_CASE1['true_tot_balance'])

class TestCalResult(unittest.TestCase):
    
    def test_unenough_point(self):
        remain, _ = cal_result(
            TEST_CASE1["true_sorted_records"],
            TEST_CASE1["true_tot_balance"],
            spend=11300
        )
        self.assertLessEqual(0, remain)
        remain, _ = cal_result(
            TEST_CASE1["true_sorted_records"],
            TEST_CASE1["true_tot_balance"],
            spend=15000
        )
        self.assertLessEqual(0, remain)

    def test_enough_point(self):
        remain, result = cal_result(
            TEST_CASE1["true_sorted_records"],
            TEST_CASE1["true_tot_balance"],
            spend=5000
        )
        self.assertEqual(remain, 0)
        self.assertEqual(result, { 
            "DANNON": 1000, 
            "UNILEVER": 0, 
            "MILLER COORS": 5300 
        })

if __name__ == '__main__':
    unittest.main()

