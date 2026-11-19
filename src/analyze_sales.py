from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "supermarket_sales.csv"
OUTPUT_DIR = ROOT / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"

def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}\n"
            "Download supermarket_sales.csv and place it inside the data folder."
        )

    df = pd.read_csv(DATA_FILE)
    # Standardize column names so small differences in capitalization/spaces do not matter.
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace("%", "percent", regex=False)
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )

    # Convert expected numeric columns safely.
    for col in ["unit_price", "quantity", "tax_5", "total", "cogs",
                "gross_income", "rating"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["month"] = df["date"].dt.to_period("M").astype(str)
        df["day_name"] = df["date"].dt.day_name()

    return df

def print_summary(df):
    print("\n" + "=" * 60)
    print("SUPERMARKET SALES ANALYSIS")
    print("=" * 60)
    print(f"Number of transactions : {len(df):,}")
    print(f"Number of columns      : {len(df.columns)}")
    if "total" in df.columns:
        print(f"Total revenue          : {df['total'].sum():,.2f}")
        print(f"Average transaction   : {df['total'].mean():,.2f}")
    if "gross_income" in df.columns:
        print(f"Total gross income     : {df['gross_income'].sum():,.2f}")
    if "rating" in df.columns:
        print(f"Average customer rating: {df['rating'].mean():.2f}/10")
    print("\nMissing values by column:")
    print(df.isnull().sum().to_string())

def save_grouped_analysis(df, column, value="total", filename=None):
    if column not in df.columns or value not in df.columns:
        return
    result = df.groupby(column)[value].sum().sort_values(ascending=False)
    result.to_csv(OUTPUT_DIR / filename)
    print(f"\n{value} by {column}:")
    print(result.round(2).to_string())

def create_charts(df):
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    charts = [
        ("product_line", "total", "Revenue by Product Line",
         "Revenue", "revenue_by_product_line.png", "bar"),
        ("branch", "total", "Revenue by Branch",
         "Revenue", "revenue_by_branch.png", "bar"),
        ("payment", "total", "Revenue by Payment Method",
         "Revenue", "revenue_by_payment.png", "bar"),
        ("customer_type", "total", "Revenue by Customer Type",
         "Revenue", "revenue_by_customer_type.png", "bar"),
    ]

    for category, metric, title, ylabel, filename, kind in charts:
        if category in df.columns and metric in df.columns:
            plt.figure(figsize=(10, 6))
            data = df.groupby(category)[metric].sum().sort_values(ascending=False).reset_index()
            sns.barplot(data=data, x=category, y=metric)
            plt.title(title, fontsize=15, weight="bold")
            plt.xlabel(category.replace("_", " ").title())
            plt.ylabel(ylabel)
            plt.xticks(rotation=20, ha="right")
            plt.tight_layout()
            plt.savefig(CHART_DIR / filename, dpi=150)
            plt.close()

    if "date" in df.columns and "total" in df.columns:
        monthly = df.dropna(subset=["date"]).groupby(df["date"].dt.to_period("M"))["total"].sum()
        if not monthly.empty:
            plt.figure(figsize=(10, 5))
            monthly.index = monthly.index.astype(str)
            monthly.plot(marker="o")
            plt.title("Monthly Revenue Trend", fontsize=15, weight="bold")
            plt.xlabel("Month")
            plt.ylabel("Revenue")
            plt.xticks(rotation=30)
            plt.tight_layout()
            plt.savefig(CHART_DIR / "monthly_revenue.png", dpi=150)
            plt.close()

    if "quantity" in df.columns and "total" in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x="quantity", y="total", alpha=0.6)
        plt.title("Quantity vs Transaction Total", fontsize=15, weight="bold")
        plt.tight_layout()
        plt.savefig(CHART_DIR / "quantity_vs_total.png", dpi=150)
        plt.close()

    print(f"\nCharts saved in: {CHART_DIR}")

def save_cleaned_data(df):
    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_DIR / "supermarket_sales_cleaned.csv", index=False)

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = load_data()
    print_summary(df)

    # Remove exact duplicate rows and rows without a transaction total.
    before = len(df)
    df = df.drop_duplicates()
    if "total" in df.columns:
        df = df.dropna(subset=["total"])
    print(f"\nDuplicate/invalid rows removed: {before - len(df)}")

    save_cleaned_data(df)
    save_grouped_analysis(df, "product_line", filename="sales_by_product_line.csv")
    save_grouped_analysis(df, "branch", filename="sales_by_branch.csv")
    save_grouped_analysis(df, "payment", filename="sales_by_payment.csv")
    save_grouped_analysis(df, "customer_type", filename="sales_by_customer_type.csv")
    create_charts(df)

    print("\nAnalysis completed successfully.")
    print("Check the outputs folder for cleaned data, summary CSV files and charts.")

if __name__ == "__main__":
    main()
