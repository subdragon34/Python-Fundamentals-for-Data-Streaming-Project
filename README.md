# Assignment 1 - Python Fundamentals for Data Streaming

## AITU Campus Shuttle and Mobility Data

This folder contains the complete implementation for Assignment 1 in Real-time Data Analysis.

The project uses the supplied ten-event shuttle dataset and covers parsing, validation, event generation, streaming simulation, JSON export, a FastAPI endpoint, basic analysis, tests, and execution evidence.

## Project files

- `main.py` - dataset, parsing, validation, generator, streaming processing, occupancy logic, and analysis
- `api.py` - FastAPI application with `POST /events`
- `export_json.py` - exports the supplied dataset to `events.json`
- `events.json` - JSON version of the supplied ten events
- `test_assignment.py` - automated tests
- `requirements.txt` - required Python packages
- `completed_tables.md` - completed assignment tables
- `Assignment1_Technical_Report_Amankos_Danial_BDA_2405.pdf` - technical report and submission record
- `evidence/` - saved execution output, API responses, and test results

## Python version

The project was verified with Python 3.10.11.

## Install packages

Open a terminal in this folder and run:

```bash
python -m pip install -r requirements.txt
```

## Run the main program

```bash
python main.py
```

This prints the validated event stream, the streaming-processing results, and the required analysis.

## Export JSON

```bash
python export_json.py
```

## Run the API

```bash
python -m uvicorn api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Use the Swagger interface to test `POST /events`.

Example accepted event:

```json
{
  "Timestamp": "08:05",
  "Route": "AITU-Campus–Residence",
  "Bus": "B02",
  "Passengers": 26,
  "Speed_kmh": 30,
  "Status": "ON_ROUTE"
}
```

Example rejected event:

```json
{
  "Timestamp": "28:90",
  "Route": "AITU-Campus–Residence",
  "Bus": "B02",
  "Passengers": -5,
  "Speed_kmh": 150,
  "Status": "MOVING"
}
```

## Run tests

```bash
python -m pytest -q
```

## Main design choices

The stream is represented as dictionaries because the same structure maps naturally to JSON requests.

`validate_event()` is reused by the generator and by the API. This keeps validation rules in one place.

`event_generator()` keeps only the previous timestamp while yielding events. It does not collect a second full copy of the stream inside the processing logic.

The analysis is also written as a single pass over the generator. This is closer to a real streaming workflow than repeatedly loading the whole dataset into a DataFrame.

## Required results

- Average passenger count: `24.4`
- Maximum passenger count: `30`
- Number of `STOPPED` events: `1`
- Busiest minute: `08:09`
- Busiest bus: `B02`

