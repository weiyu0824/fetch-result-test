import sys
import csv
import traceback
from typing import List, Tuple
from collections import defaultdict

CSV_FILEPATH = "test_csv/demo.csv"


def read_csv(file_path: str):
    """
    Read CSV file

    Args:
        file_path: file path to the csv file
    Return:
        records: list of record, which is a tuple of payer(str), points(int), timestamp(str)
    Raise:
        TypeError for wrong header name,
        TypeError for wrong data,
        TypeError for missed data
    """

    records = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        row_idx = 0
        for row in csv_reader:
            if row_idx == 0 and ",".join(row) != "payer,points,timestamp":
                raise ValueError("This CSV file contains wrong header")
            elif row_idx != 0:
                try:
                    records.append((row[0], int(row[1]), row[2]))
                except:
                    raise ValueError("This CSV file contains wrong data format")
            row_idx += 1
    return records


def val_records(records: List[Tuple]):
    """
    Examine the balance of each payer at every timestamp. Make sure that their balance would not less than 0.

    Args:
        records: list of record
    Return:
        bool
    """

    balance = defaultdict(lambda: 0)
    for record in records:
        payer = record[0]
        points = record[1]
        balance[payer] += points
        if balance[payer] < 0:
            return False
    return True


def cal_result(records: List[Tuple], spend: int):
    """
    Calculate the result after spending the points
    Args:
        records: list of record
        spend: amount of points
    """

    balance = defaultdict(lambda: 0)
    for record in records:
        payer = record[0]
        points = record[1]
        balance[payer] += points

    remain = spend
    for record in records:
        payer, points = record[0], record[1]
        if remain >= points:
            balance[payer] -= points
            remain -= points
        else:
            balance[payer] -= remain
            remain = 0
            break
    return remain, dict(balance)


def main(spend: int):
    try:
        # Read CSV
        records = read_csv(CSV_FILEPATH)

        # Sort the CSV based on timestamp
        records.sort(key=lambda r: r[2])

        # Validate the records
        correct = val_records(records)
        if not correct:
            raise ValueError("This CSV records violate the rule")

        # Calculate the result
        remain, result = cal_result(records, spend)

        if remain != 0:
            print("Unable to complete the task, cause you dont have enough points")
        else:
            print(result)

    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    # Check the input format
    if len(sys.argv) != 2:
        exit("Wrong input format, [format: python3 spend_points.py <#point that you want to spend>]")
    if int(sys.argv[1]) < 0:
        exit("We do not expect a spend less than 0")

    main(int(sys.argv[1]))
