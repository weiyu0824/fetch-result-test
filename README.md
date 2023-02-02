# Fetch Result Test
This is the repo for Fetch Result Test (Backend)

## How to run the code
- Run code
```
python3 spend_points.py <points>
```

- Run unit test
```
python3 spend_points_test.py
```

## Design
### Logic
To my understanding, negative points in the CSV file means the amount of points from specific payer the user spend. Thus, we should make sure that balance should not less than 0 at any timestamp. 

### Flow
This simple program contains several steps.
1. Read the CSV file
2. Sort the records
3. Calculate the total balance
4. Calculate the result