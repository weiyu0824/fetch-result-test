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
To my understanding, negative points in the CSV file means the amount of points from specific payer the user spend. Thus, we should make sure that balance of each payer should not less than 0 at any timestamp. 
```
# My understanding
"DANNON", 1000, "2020-11-02T14:00:00Z" # The user got 1000 points from DANNON
"DANNON", -200, "2020-11-02T14:00:00Z" # The user spend 200 points that comes from DANNON
```

```
# Good example
"DANNON", 1000, "2020-11-02T14:00:00Z"
"DANNON", -200, "2020-11-02T14:00:00Z"

# Bad example
"DANNON", 100, "2020-11-02T14:00:00Z"
"DANNON", -200, "2020-11-02T14:00:00Z"
```
### Flow
This simple program contains several steps.
1. Read the CSV file
2. Sort the records
3. Validate the records
4. Calculate the result
