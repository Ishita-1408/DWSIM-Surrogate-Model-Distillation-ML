# Surrogate Modeling of Distillation Column using Machine Learning

---

## Project Overview

This project develops machine learning (ML) surrogate models to predict the behavior of a distillation column simulated in DWSIM. Instead of running computationally expensive simulations repeatedly, the trained ML models can quickly predict outputs based on input operating conditions.


---

## Objectives

- Automate DWSIM simulations using Python
- Generate a dataset of operating conditions and outputs
- Train multiple machine learning models
- Compare model performance
- Select the best surrogate model

---

## Inputs and Outputs

### Inputs (Features)

| Variable | Description |
|---|---|
| `T_feed` | Feed temperature |
| `P_feed` | Feed pressure |
| `z_benzene` | Feed composition |
| `reflux_ratio` | Reflux ratio |
| `stages` | Number of stages |
| `feed_stage` | Feed stage location |
| `bottoms_flow` | Bottoms flow rate |

### Outputs (Targets)

| Variable | Description |
|---|---|
| `xD` | Distillate composition |
| `xB` | Bottoms composition |
| `QC` | Condenser duty |
| `QR` | Reboiler duty |

---

## Project Structure

```
DWSIM_Surrogate_Project/
│
├── code/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda_and_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   ├── generate_lhs_inputs.py
│   ├── lhs_input_cases.csv
│   ├── run_dwsim_cases.py
│   └── test_dwsim_connection.py
│
├── dataset/
│   ├── cleaned_dataset.csv
│   ├── failed_runs.csv
│   ├── lhs_input_cases.csv
│   └── raw_simulation_data.csv
│
└── DWSIM_Flowsheet/
    └── dwsim(ben-tol).dwxml
    └── flowchart.png
```

---

## Software Requirements

- Python 3.10+
- DWSIM (installed on your system)

### Required Python Libraries

```bash
pip install pandas numpy matplotlib scikit-learn xgboost
```

---

## Step-by-Step Instructions

### Step 1 — Open the DWSIM Flowsheet

1. Open **DWSIM**
2. Click **File → Open**
3. Navigate to `DWSIM_Flowsheet/dwsim(ben-tol).dwxml`
4. Verify the flowsheet loads correctly, all streams and units are connected, and the simulation runs manually

**Flowsheet Preview:**

![DWSIM Flowsheet](DWSIM_Flowsheet/flowchart.png)

---

### Step 2 — Generate Input Data (LHS Sampling)

Run the following from the project root:

```bash
cd code
python generate_lhs_inputs.py
```

**Output:** `code/lhs_input_cases.csv`

---

### Step 3 — Run DWSIM Simulations

```bash
python run_dwsim_cases.py
```

This script loads input cases, runs DWSIM simulations automatically, and extracts outputs.

**Outputs:**
- `dataset/raw_simulation_data.csv`
- `dataset/failed_runs.csv`

> **Note:** Update the DWSIM installation path inside `run_dwsim_cases.py` if required.

---

### Step 4 — Data Cleaning

Open and run all cells in:

```
code/01_data_cleaning.ipynb
```

This removes failed simulation cases and cleans the dataset.

**Output:** `dataset/cleaned_dataset.csv`

---

### Step 5 — Exploratory Data Analysis (Optional)

Open and run:

```
code/02_eda_and_preprocessing.ipynb
```

---

### Step 6 — Train Machine Learning Models

Open and run all cells in:

```
code/03_model_training.ipynb
```

Models trained:
- Polynomial Regression
- Random Forest
- XGBoost
- ANN (Artificial Neural Network)

Evaluation metrics used: **MAE**, **RMSE**, **R²**

---

### Step 7 — Reproducing Results

1. Ensure `dataset/cleaned_dataset.csv` exists
2. Open and run all cells in `code/03_model_training.ipynb`
3. Outputs: model performance tables, prediction comparison plots, and final model selection

---

## Results Summary

| Model | Performance |
|---|---|
| Random Forest | ✅ Highest accuracy, lowest error |
| XGBoost | ✅ High accuracy |
| Polynomial Regression | ⚠️ Captured trends but higher error |
| ANN | ⚠️ Lower performance (untuned) |

---

## Final Model

**Random Forest** was selected as the final surrogate model based on:
- Lowest prediction error (MAE, RMSE)
- Highest R² score
- Robust performance across all output variables

---

## Limitations

- Some input variables showed limited variation, affecting feature importance analysis
- Operating space coverage can be improved with denser sampling

---

## Future Work

- Improve input variable sampling range and density
- Perform hyperparameter tuning for ANN and XGBoost
- Deploy the model for real-time prediction

---

## Author

**Ishita**

---

## Notes

- Ensure DWSIM is properly installed before running simulation scripts
- All scripts should be run from within the `code/` directory
- Run scripts in order (Steps 2 → 3 → 4 → 6) for full reproducibility
