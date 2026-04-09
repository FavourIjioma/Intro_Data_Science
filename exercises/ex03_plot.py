import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import marimo as mo

    students = pl.read_csv("data/raw/students.csv")
    sales = pl.read_json("data/raw/sales.json")
    return go, make_subplots, mo, pl, px, sales, students


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exercise 3: Plotting Visualizations 📊

    **Plot Visuals!**

    **What you'll do:**

    - Create visualizations

    **Instructions:**

    - Complete each TODO section
    - Run cells to see your results
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1: Your First Plot - Bar Chart
    """)
    return


@app.cell
def _(pl, px, sales):
    # TODO: Create a bar chart showing sales by category
    # Use plotly express (px.bar)
    # - x-axis: product_category
    # - y-axis: total sales
    # - Add a title
    # - Color the bars

    # Hint: Make sure category_sales is a valid dataframe first!

    category_sales = sales.group_by("product_category").agg(
        pl.sum("total_amount").alias("total_sales")
    ).sort("total_sales", descending=True)

    ex_fig1 = px.bar(
        category_sales,
        x="product_category",
        y="total_sales",
        title="Total Sales by Product Category",
        color="product_category",
        labels={"product_category": "Category", "total_sales": "Total Sales ($)"}
    )
    ex_fig1
    return (category_sales, ex_fig1)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2: Line Chart - Sales Over Time
    """)
    return


@app.cell
def _(pl, px, sales):
    # TODO: Create a line chart showing sales trends by month
    # Use px.line
    # - x-axis: month
    # - y-axis: total revenue
    # - Add markers to the line
    # - Add a title

    sales_monthly = sales.with_columns(
        pl.col("date").str.strptime(pl.Date, "%Y-%m-%d").alias("date_parsed")
    ).with_columns(
        pl.col("date_parsed").dt.month().alias("month")
    ).group_by("month").agg(
        pl.sum("total_amount").alias("total_revenue")
    ).sort("month")

    ex_fig2 = px.line(
        sales_monthly,
        x="month",
        y="total_revenue",
        title="Monthly Sales Revenue Trend",
        markers=True,
        labels={"month": "Month", "total_revenue": "Total Revenue ($)"}
    )
    ex_fig2
    return (ex_fig2, sales_monthly)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3: Scatter Plot - Exploring Relationships
    """)
    return


@app.cell
def _(px, students):
    # TODO: Create a scatter plot showing the relationship between
    # attendance_rate (x-axis) and test_score (y-axis)
    # - Color points by grade_level
    # - Add a trendline (trendline="ols")
    # - Add appropriate title and labels

    ex_fig3 = px.scatter(
        students,
        x="attendance_rate",
        y="test_score",
        color="grade_level",
        trendline="ols",
        title="Attendance Rate vs Test Score by Grade Level",
        labels={
            "attendance_rate": "Attendance Rate (%)",
            "test_score": "Test Score"
        }
    )
    ex_fig3
    return (ex_fig3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4: Histogram - Distribution Analysis
    """)
    return


@app.cell
def _(px, sales):
    # TODO: Create a histogram of transaction amounts (total_amount)
    # - Use 30 bins
    # - Add a title
    # - Label the axes
    # - Try adding nbins=30 parameter

    ex_fig4 = px.histogram(
        sales,
        x="total_amount",
        nbins=30,
        title="Distribution of Transaction Amounts",
        labels={"total_amount": "Transaction Amount ($)"}
    )
    ex_fig4
    return (ex_fig4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 5: Advanced - Multiple Subplots
    """)
    return


@app.cell
def _(category_sales, go, make_subplots, pl, sales):
    # TODO: Create a dashboard with 2 subplots:
    # 1. Top plot: Bar chart of sales by category (reuse category_sales)
    # 2. Bottom plot: Bar chart of sales by region (reuse region_summary)

    # Hint: Use go.Figure() with make_subplots or add multiple traces
    # This is challenging - check the solution if you get stuck!

    region_summary = sales.group_by("region").agg(
        pl.sum("total_amount").alias("total_sales")
    ).sort("total_sales", descending=True)

    ex_fig5 = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            "Sales by Category",
            "Sales by Region"
        )
    )

    ex_fig5.add_trace(
        go.Bar(
            x=category_sales["product_category"],
            y=category_sales["total_sales"],
            name="Category",
            marker_color="#FF6B6B"
        ),
        row=1, col=1
    )

    ex_fig5.add_trace(
        go.Bar(
            x=region_summary["region"],
            y=region_summary["total_sales"],
            name="Region",
            marker_color="#4ECDC4"
        ),
        row=2, col=1
    )

    ex_fig5.update_layout(
        height=700,
        showlegend=False,
        title_text="Sales Dashboard"
    )
    ex_fig5
    return (ex_fig5, region_summary)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🎉 Excellent Work!

    You've completed the plotting exercises!

    **What you practiced:**

    - ✅ Bar charts
    - ✅ Line charts
    - ✅ Scatter plots
    - ✅ Histograms
    - ✅ Advanced: Subplots
    - ✅ Multiple chart types (bar, line, scatter, histogram)
    - ✅ Combining data analysis with visualization

    **What's next?**

    - Try creating your own visualizations with the data!

    **Pro Tips:**

    - Plotly charts are interactive - hover, zoom, pan!
    - Always explore your data before plotting
    """)
    return


if __name__ == "__main__":
    app.run()