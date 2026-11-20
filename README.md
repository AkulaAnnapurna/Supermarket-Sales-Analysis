Intern ID: CITS9988

# Supermarket Sales Analysis

## Project Overview
This beginner-friendly data analysis project explores supermarket transaction data using Python. It examines revenue, product categories, branch performance, customer types, payment methods and monthly sales patterns.

## Objectives
- Understand and inspect supermarket transaction data.
- Clean duplicate and invalid records.
- Calculate total revenue, average transaction value and gross income.
- Compare sales across product lines, branches, payment methods and customer types.
- Create charts to communicate the findings.

## Tools and Technologies
- Python
- Pandas
- Matplotlib
- Seaborn
- Git and GitHub

## Dataset
Download the educational Supermarket Sales CSV dataset from:
https://github.com/graphext/1000-Supermarket-Sales-Dataset

Save the downloaded file as `supermarket_sales.csv` inside the `data/` folder.

The dataset contains transaction fields such as branch, city, customer type, gender, product line, unit price, quantity, total, date, payment method, gross income and customer rating.

## Project Structure
```text
Supermarket-Sales-Analysis/
├── data/
│   └── supermarket_sales.csv
├── outputs/
│   ├── charts/
│   └── (generated summary CSV files)
├── src/
│   └── analyze_sales.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup Instructions

### 1. Open the project
Open this folder in Visual Studio Code.

### 2. Create and activate a virtual environment (recommended)
Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Add the dataset
Place `supermarket_sales.csv` inside the `data` folder.

### 5. Run the analysis
```bash
python src/analyze_sales.py
```

## Outputs
The script generates:
- `outputs/supermarket_sales_cleaned.csv`
- Revenue summaries by product line, branch, payment method and customer type.
- Charts in `outputs/charts/`:
  - Revenue by product line
  - Revenue by branch
  - Revenue by payment method
  - Revenue by customer type
  - Monthly revenue trend
  - Quantity versus transaction total

## Notes
- The dataset's monetary values are in the currency represented by the source dataset; do not label them as Indian rupees.
- Results and conclusions should be written after running the analysis on the downloaded dataset.
- This is an educational analysis, not a live supermarket reporting system.

## Author
Akula Annapurna
