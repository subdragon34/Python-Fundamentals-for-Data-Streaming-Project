# Completed Assignment Tables

## Part A - Data Structures and Parsing

| Field | Python type | Validation rule | Example |
|---|---|---|---|
| Timestamp | `datetime.time` | Valid `HH:MM` time | `08:00` |
| Passengers | `int` | Non-negative integer | `18` |
| Speed_kmh | `int` or `float` | From 0 to 120 inclusive | `31` |
| Status | `str` | `ON_ROUTE` or `STOPPED` | `ON_ROUTE` |

The implementation also checks that Route and Bus are non-empty strings and that all required event fields are present.

## Part B - Streaming Simulation

| Event | Passengers | Speed | Status | Processed? | Reason |
|---|---:|---:|---|---|---|
| 1 | 18 | 31 | ON_ROUTE | Yes | Valid event |
| 2 | 22 | 28 | ON_ROUTE | Yes | Valid event |
| 3 | 21 | 29 | ON_ROUTE | Yes | Valid event |
| 4 | 25 | 27 | ON_ROUTE | Yes | Valid event |
| 5 | 24 | 0 | STOPPED | Yes | Valid event |

The fifth event is still processed because a speed of 0 is valid and its status is correctly marked as `STOPPED`.

## Part C - Occupancy Category

| Passenger count | Occupancy category |
|---|---|
| 0–10 | LOW |
| 11–20 | MEDIUM |
| 21–30 | HIGH |
| >30 | OVER_CAPACITY |

## Part D - Analysis

| Measure | Result |
|---|---|
| Average passenger count | 24.4 |
| Maximum passenger count | 30 |
| Number of STOPPED events | 1 |
| Busiest minute | 08:09 |
| Busiest bus | B02 |

## Part E - Test Record

| Test | Input / condition | Expected result | Actual result |
|---|---|---|---|
| Valid event | 12 passengers, 35 km/h, ON_ROUTE | Accepted | Passed |
| Negative passengers | -1 passenger | Rejected | Passed |
| Speed above limit | 121 km/h | Rejected | Passed |
| Invalid status | MOVING | Rejected | Passed |
| Invalid timestamp | 25:61 | Rejected | Passed |
| Student-designed boundary/type test | 12.5 passengers | Rejected as non-integer | Passed |
| Generator order | 10 supplied events | 08:00 through 08:09 in order | Passed |
| Occupancy boundaries | 10, 11, 20, 21, 30, 31 | Correct categories | Passed |
| Analysis | supplied dataset | 24.4, 30, 1, 08:09, B02 | Passed |
| FastAPI valid request | 26 passengers | accepted=true, HIGH | Passed |
| FastAPI invalid request | bad time, passengers, speed, status | accepted=false with 4 errors | Passed |
