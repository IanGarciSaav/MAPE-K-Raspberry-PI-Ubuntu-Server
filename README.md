# MAPE-K Loop for Raspberry Pi / Ubuntu Server

This project implements a self-adaptive system using the **MAPE-K** (Monitor, Analyze, Plan, Execute, Knowledge) loop architecture. It is designed to monitor system resources (specifically disk usage) on a Linux-based server (like a Raspberry Pi running Ubuntu) and autonomously perform actions based on defined rules.

## Project Overview

The system continuously monitors the disk usage of the server. If the usage exceeds a defined threshold (both in GB and percentage), it triggers an alert and plans an action (e.g., cleaning the disk or notifying the administrator).

## Architecture (MAPE-K)

The system consists of four main components that run in a continuous loop, sharing data through a common knowledge base (CSV files and configuration).

### 1. Monitor (M)
- **Script**: `src/monitor.py`
- **Function**: Collects real-time disk usage metrics from the system using `psutil`.
- **Behavior**: It can simulate outliers (abnormal usage) based on a configured probability to test the adaptive behavior.
- **Output**: Writes metrics to `data/disk_data.csv`.

### 2. Analyze (A)
- **Script**: `src/analysis.py`
- **Function**: Reads the monitoring data and compares it against the rules defined in the Knowledge base.
- **Behavior**: Identifies "Outliers" if usage exceeds the thresholds defined in `rules/config_rules.txt`.
- **Output**: Generates analysis results in `data/analysis.csv` with a status of "ALERT" or "OK".

### 3. Plan (P)
- **Script**: `src/scheduler.py`
- **Function**: Reads the analysis results and determines the appropriate course of action.
- **Behavior**:
    - If status is "ALERT" and usage > 80%: Plans a "CLEAN_DISK" action.
    - If status is "ALERT" but lower severity: Plans a "NOTIFY" action.
- **Output**: Writes planned actions to `data/actions.csv`.

### 4. Execute (E)
- **Script**: `src/execute.py`
- **Function**: Reads the planned actions and executes them.
- **Behavior**: In this simulation, it prints the actions to the console (e.g., cleaning logs, sending notifications).
- **Input**: Reads from `data/actions.csv`.

### Knowledge (K)
- **Configuration**: `rules/config_rules.txt` contains the thresholds and parameters.
- **Data Bus**: The `data/` directory acts as the shared knowledge base where components exchange current system state.

## Directory Structure

```
MAPE-K/
├── src/                # Python source code
│   ├── monitor.py      # Monitor component
│   ├── analysis.py     # Analysis component
│   ├── scheduler.py    # Planner component
│   └── execute.py      # Executor component
├── data/               # Shared data storage (CSV files generated at runtime)
├── rules/              # Configuration files
│   └── config_rules.txt
└── README.md           # Project documentation
```

## Prerequisites

- Python 3.x
- `psutil` library

To install the dependencies:

```bash
pip install psutil
```

## Usage

To run the complete MAPE-K loop, you need to run the four components. Since they are designed to run continuously, you should run them in separate terminals or as background processes.

1.  **Start the Monitor**:
    ```bash
    python src/monitor.py
    ```

2.  **Start the Analyze Component**:
    ```bash
    python src/analysis.py
    ```

3.  **Start the Planner**:
    ```bash
    python src/scheduler.py
    ```

4.  **Start the Executor**:
    ```bash
    python src/execute.py
    ```

## Configuration

You can adjust the system behavior by editing `rules/config_rules.txt`.

```ini
[Rules]
outlier_threshold_gb = 381.47      # Threshold in GB to consider usage as an outlier
outlier_threshold_percent = 80.0   # Threshold in % to consider usage as an outlier

[Parameters]
check_interval = 5                 # Interval in seconds between checks
outlier_probability = 0.15         # Probability (0.0 to 1.0) of simulating an outlier for testing
```
