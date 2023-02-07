import unittest
from copy import deepcopy
from spend_points import read_csv, preprocess_records, cal_result


TEST_CASE1 = {
    "records": [
        ("DANNON", 1000, "2020-11-02T14:00:00Z"),
        ("UNILEVER", 200, "2020-10-31T11:00:00Z"),
        ("DANNON", -200, "2020-10-31T15:00:00Z"),
        ("MILLER COORS", 10000, "2020-11-01T14:00:00Z"),
        ("DANNON", 300, "2020-10-31T10:00:00Z")
    ],
    "p_records": [
        ("DANNON", 100, "2020-10-31T10:00:00Z"),
        ("UNILEVER", 200, "2020-10-31T11:00:00Z"),
        ("DANNON", 0, "2020-10-31T15:00:00Z"),
        ("MILLER COORS", 10000, "2020-11-01T14:00:00Z"),
        ("DANNON", 1000, "2020-11-02T14:00:00Z"),
    ],
    "spend": 5000,
    "result": {
        "DANNON": 1000, "UNILEVER": 0, "MILLER COORS": 5300
    }
}

TEST_CASE2 = {
    "records": [
        ("A",100,"2020-10-31T10:00:00Z"),
        ("B",100,"2020-10-31T10:01:00Z"),
        ("A",-100,"2020-10-31T10:02:00Z"),
        ("A",100,"2020-10-31T10:03:00Z")
    ],
    "p_records": [
        ("A",0,"2020-10-31T10:00:00Z"),
        ("B",100,"2020-10-31T10:01:00Z"),
        ("A",0,"2020-10-31T10:02:00Z"),
        ("A",100,"2020-10-31T10:03:00Z")
    ],
    "spend": 100, 
    "result": {
        "A": 100, "B": 0
    }
}


class TestReadCSV(unittest.TestCase):
    def test_wrong_header(self):
        with self.assertRaises(ValueError):
            read_csv("test_csv/test1_wrong_header.csv")

    def test_wrong_data(self):
        with self.assertRaises(ValueError):
            read_csv("test_csv/test2_wrong_data.csv")

    def test_missed_data(self):
        with self.assertRaises(ValueError):
            read_csv("test_csv/test3_missed_data.csv")

    def test_read_data(self):
        records = read_csv("test_csv/demo.csv")
        self.assertEqual(records, deepcopy(TEST_CASE1["records"]))


class TestPreprocessRecords(unittest.TestCase):
    def test_violate_rule(self):
        with self.assertRaises(ValueError):
            preprocess_records([("DANNON", -200, "2020-10-31T15:00:00Z")])
        
    def test_preprocess(self):
        # TESTCASE 1
        records = preprocess_records(deepcopy(TEST_CASE1["records"]))
        self.assertEqual(records, TEST_CASE1["p_records"])

        # TESTCASE 2
        records = preprocess_records(deepcopy(TEST_CASE2["records"]))
        self.assertEqual(records, TEST_CASE2["p_records"])


class TestCalResult(unittest.TestCase):
    def test_unenough_point(self):
        # TESTCASE 1
        remain, _ = cal_result(deepcopy(TEST_CASE1["p_records"]), spend=11300)
        self.assertLessEqual(0, remain)
        remain, _ = cal_result(deepcopy(TEST_CASE1["p_records"]), spend=15000)
        self.assertLessEqual(0, remain)

        # TESTCASE 2
        remain, _ = cal_result(deepcopy(TEST_CASE2["p_records"]), spend=200)
        self.assertLessEqual(0, remain)

    def test_enough_point(self):
        # TESTCASE 1
        remain, result = cal_result(deepcopy(TEST_CASE1["p_records"]), spend=TEST_CASE1["spend"])
        self.assertEqual(remain, 0)
        self.assertEqual(result, TEST_CASE1["result"])

        # TESTCASE 2
        remain, result = cal_result(deepcopy(TEST_CASE2["p_records"]), spend=TEST_CASE2["spend"])
        self.assertEqual(remain, 0)
        self.assertEqual(result, TEST_CASE2["result"])


if __name__ == "__main__":
    unittest.main()
