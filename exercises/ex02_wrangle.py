import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exercise 2: Data Wrangling

    **Practice Polars!**

    **What you'll do:**

    - Load and explore real datasets
    - Filter and transform data
    - Answer questions with data

    **Instructions:**

    - Complete each TODO section
    - Run cells to see your results

    ---
    """)
    return


@app.cell
def _():
    import polars as pl
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1: Load and Explore Data
    """)
    return


@app.cell
def _(pl):
    # TODO: Load the students.csv file using Polars
    # The file is at: ../data/raw/students.csv

    students = pl.read_csv("../data/raw/students.csv")

    # TODO: Display the first 10 rows
    students.head(10)
    return (students,)


@app.cell
def _(students):
    # TODO: Display basic information about the students dataset
    # - How many rows and columns?
    # - What are the column names?
    # - What are the data types?

    # Hint: Use students.shape, students.columns, students.dtypes, or students.describe()
    print(f"Rows: {students.shape[0]}, Columns: {students.shape[1]}")
    print("\nColumn names:", students.columns)
    print("\nData types:")
    print(students.dtypes)
    print("\nSummary statistics:")
    print(students.describe())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2: Filtering Practice
    """)
    return


@app.cell
def _(pl, students):
    # TODO: Filter to find students who scored above 85 on their test

    high_scorers = students.filter(pl.col("test_score") > 85)

    print(f"Number of high scorers: {len(high_scorers) if high_scorers is not None else 0}")
    high_scorers.head()
    return (high_scorers,)


@app.cell
def _(pl, students):
    # TODO: Filter to find students in grade_level 10 with attendance_rate > 90%

    grade_10_good_attendance = students.filter(
        (pl.col("grade_level") == 10) & (pl.col("attendance_rate") > 90)
    )
    grade_10_good_attendance.head()
    return (grade_10_good_attendance,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3: Selecting and Creating Columns
    """)
    return


@app.cell
def _(pl, students):
    # TODO: Select only the name, grade_level, and test_score columns

    subset = students.select(["name", "grade_level", "test_score"])
    subset.head()
    return (subset,)


@app.cell
def _(pl, students):
    # TODO: Create a new column "performance_category" that categorizes students:
    # - "Excellent" if test_score >= 90
    # - "Good" if test_score >= 75
    # - "Needs Improvement" if test_score < 75
    # - Handle null values appropriately

    # Hint: Use pl.when().then().otherwise() chains

    students_categorized = students.with_columns(
        pl.when(pl.col("test_score").is_null())
        .then(pl.lit("Missing"))
        .when(pl.col("test_score") >= 90)
        .then(pl.lit("Excellent"))
        .when(pl.col("test_score") >= 75)
        .then(pl.lit("Good"))
        .otherwise(pl.lit("Needs Improvement"))
        .alias("performance_category")
    )
    students_categorized.select(["name", "test_score", "performance_category"]).head()
    return (students_categorized,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4: Working with Sales Data
    """)
    return


@app.cell
def _(pl):
    # TODO: Load the sales.json file
    # The file is at: ../data/raw/sales.json

    sales = pl.read_json("../data/raw/sales.json")
    return (sales,)


@app.cell
def _(sales):
    # TODO: Display basic info about the sales dataset
    # How many transactions? What's the date range?
    print(f"Number of transactions: {sales.shape[0]}")
    print(f"Columns: {sales.columns}")

    # Parse date column to find range
    if "date" in sales.columns:
        date_series = sales.select(pl.col("date").str.strptime(pl.Date, "%Y-%m-%d").alias("date"))
        min_date = date_series["date"].min()
        max_date = date_series["date"].max()
        print(f"Date range: {min_date} to {max_date}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 5: Date Operations
    """)
    return


@app.cell
def _(pl, sales):
    # TODO: Convert the date column to datetime type
    # Then extract the month and create a new column "month"

    sales_with_month = sales.with_columns(
        pl.col("date").str.strptime(pl.Date, "%Y-%m-%d").alias("date_parsed")
    ).with_columns(
        pl.col("date_parsed").dt.month().alias("month")
    )
    sales_with_month.select(["date", "month"]).head()
    return (sales_with_month,)


@app.cell
def _(pl, sales_with_month):
    # TODO: Calculate total sales by month
    # Show which month had the highest revenue

    monthly_sales = (
        sales_with_month
        .group_by("month")
        .agg(pl.sum("total_amount").alias("total_sales"))
        .sort("month")
    )
    print("Monthly sales:")
    print(monthly_sales)

    highest_month = monthly_sales.sort("total_sales", descending=True).head(1)
    print("\nMonth with highest revenue:")
    print(highest_month)
    return (highest_month, monthly_sales)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🎉 Excellent Work!

    You've completed the data wrangling exercises!

    **What you practiced:**

    - ✅ Loading CSV and JSON data with Polars
    - ✅ Filtering and selecting data
    - ✅ Creating calculated columns
    - ✅ Date operations

    **What's next?**

    - Move on to Exercise 3: Plot

    **Pro Tips:**

    - Chain Polars operations for cleaner code
    - Always explore your data before plotting
    """)
    return


if __name__ == "__main__":
    app.run()