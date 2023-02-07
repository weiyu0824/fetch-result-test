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
To my understanding, those records with negative points in the CSV file means the user spend that amount of points from the payer. Thus, we should make sure that the user has enough points from that payer when he/she is about to spend points. 
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
2. Preprocess the records
3. Calculate the result

```
# Preprocess
# sort -> process records with negative points

# Before preprocess
"DANNON", -100, "2020-11-02T14:00:00Z"
"DANNON", 200, "2020-11-01T14:00:00Z"

# After preprocess
"DANNON", 100, "2020-11-01T14:00:00Z"
"DANNON", 0, "2020-11-02T14:00:00Z"
```
