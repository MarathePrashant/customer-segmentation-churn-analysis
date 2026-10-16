
# 🛍️ Customer Shopping Behavior & Segmentation Analysis

> An end-to-end customer analytics project using **Python, Pandas, SQL, and Power BI** to explore purchasing patterns, customer demographics, product performance, subscription behavior, discount usage, and customer satisfaction.

## 📌 Project Overview

Understanding customer shopping behavior helps businesses evaluate product performance, identify customer segments, and make more informed marketing and merchandising decisions.

This project analyzes a dataset containing **3,900 customer records** to explore purchasing patterns, customer demographics, product categories, subscription status, promotional discounts, shipping preferences, and review ratings.

The project combines Python-based data preparation, SQL business analysis, and Power BI visualization to demonstrate an end-to-end analytics workflow.

## 🎯 Business Objectives

- Analyze purchase amounts across customer demographics and product categories.
- Explore customer segments using age groups and purchasing attributes.
- Evaluate subscription status and shopping behavior.
- Investigate discount usage and promotional patterns.
- Compare product ratings and category-level performance.
- Analyze purchasing frequency, payment methods, seasons, and shipping preferences.
- Develop business-focused KPIs and interactive Power BI visualizations.

## 📊 Project Snapshot

| Metric | Result |
|---|---:|
| Customer records | 3,900 |
| Unique customer IDs | 3,900 |
| Total recorded purchase amount | $233,081 |
| Average purchase amount | $59.76 |
| Average review rating | 3.75 / 5 |
| Missing review ratings handled | 37 |
| Exact duplicate records removed | 0 |

*These figures are based on the Python analysis. Purchase amounts represent the supplied dataset and should not automatically be interpreted as a retailer's complete financial revenue.*

## 🛠️ Tech Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data Manipulation | Pandas, NumPy |
| Query Language | SQL |
| Data Visualization | Matplotlib, Seaborn |
| Business Intelligence | Microsoft Power BI |
| Dashboard Calculations | DAX |
| Data Transformation | Python, Power Query |
| Analytical Techniques | Exploratory Data Analysis, data quality checks, customer segmentation, KPI analysis |

## 🔄 Analytics Workflow

```text
Raw Customer Dataset
        ↓
Data Inspection & Quality Checks
        ↓
Data Cleaning & Standardization
        ↓
Feature Engineering
        ↓
Python-Based Exploratory Analysis
        ↓
SQL Business Analysis
        ↓
KPI Development & Data Visualization
        ↓
Interactive Power BI Dashboard
        ↓
Business Findings & Recommendations
```

## 🧹 Data Cleaning & Preparation

Python was used to prepare the dataset for analysis.

Key data preparation steps included:

- Loading and inspecting the source CSV file.
- Standardizing column names for consistent analysis.
- Validating the required columns.
- Handling missing review ratings using category-level medians, with an overall median fallback.
- Checking for and removing exact duplicate records.
- Creating age groups for demographic analysis.
- Mapping purchasing-frequency labels to numerical day values.
- Checking whether discount-related columns contained redundant information.
- Exporting cleaned data and analytical summaries for downstream use.
- Creating log files to support execution monitoring and troubleshooting.

### Data Quality Results

| Check | Result |
|---|---|
| Initial records | 3,900 |
| Missing review ratings handled | 37 |
| Exact duplicate records removed | 0 |
| Final records | 3,900 |
| Final columns | 19 |
| Missing values in final cleaned dataset | 0 |

## 🔎 SQL Business Analysis

The SQL analysis script explores business questions using aggregations, conditional logic, subqueries, and window functions.

Key analytical areas include:

- Purchase amount comparisons by gender.
- Discounted purchases compared with the overall average.
- Product rating analysis with minimum observation thresholds.
- Spending comparisons by shipping type.
- Subscription status and purchase behavior.
- Discount application rates by product.
- Customer classification using purchasing attributes.
- Top-ranked products within categories.
- Purchasing frequency and subscription comparisons.
- Purchase amount by age group and product category.
- Seasonal purchasing patterns.
- Payment method preferences.
- Category-level customer ratings.
- Comparisons involving subscription and discount usage.

**Implementation note:** SQL analysis is maintained as a project script. A PostgreSQL database connection or production database pipeline is not claimed as completed.

## 🐍 Python Exploratory Data Analysis

Python and Pandas support data preparation, summary statistics, and category-level analysis.

### Purchase Amount by Product Category

| Product Category | Records | Total Purchase Amount | Average Purchase Amount |
|---|---:|---:|---:|
| Clothing | 1,737 | $104,264 | $60.03 |
| Accessories | 1,240 | $74,200 | $59.84 |
| Footwear | 599 | $36,093 | $60.26 |
| Outerwear | 324 | $18,524 | $57.17 |

These results describe the supplied dataset. They do not, on their own, establish profitability, customer retention, or repeat-purchase performance.

### Customer Age-Group Distribution

| Age Group | Customer Records | Share |
|---|---:|---:|
| Young Adult | 486 | 12.46% |
| Adult | 755 | 19.36% |
| Middle Age | 1,100 | 28.21% |
| Senior | 1,559 | 39.97% |

The age groups provide a basis for comparing purchasing attributes across demographic segments.

## 📊 Power BI Dashboard

The Power BI dashboard is designed to present customer and product metrics through interactive visualizations.

### Planned Dashboard Components

- **KPI Cards:** Total recorded purchase amount, customer records, average purchase amount, and average review rating.
- **Category Analysis:** Purchase amount by product category.
- **Customer Demographics:** Customer distribution by age group.
- **Subscription Analysis:** Comparison of subscriber and non-subscriber purchasing metrics.
- **Discount Analysis:** Discount usage and category-level comparisons.
- **Product Performance:** Product ratings and purchasing metrics.
- **Interactive Slicers:** Gender, product category, season, and subscription status.

Dashboard descriptions and filenames should be updated to reflect the visuals and Power BI file actually committed to the repository.

## 💡 Business Questions & Recommendations

The analysis provides a foundation for investigating questions such as:

- Which product categories account for the largest share of recorded purchase amounts?
- How do average purchase amounts vary across demographic groups?
- How do subscriber and non-subscriber purchasing patterns compare?
- How does discount usage vary across categories and customer segments?
- Which products have stronger customer ratings?
- How do shipping preferences and purchasing patterns differ?

### Potential Business Recommendations

The following are analytical opportunities, not assumed findings:

1. **Subscription Growth:** Compare subscriber and non-subscriber behavior before designing conversion campaigns.
2. **Targeted Promotions:** Evaluate discount usage alongside purchase amounts and, where available, margin data before allocating promotional budgets.
3. **Customer Segmentation:** Use validated demographic and purchasing attributes to develop relevant customer groups.
4. **Product Strategy:** Combine purchase amounts, product ratings, and category performance to identify areas for further investigation.
5. **Customer Retention:** Analyze longitudinal purchase history or suitable repeat-purchase indicators before recommending retention interventions.

Recommendations should be supported by validated results and the limitations of the available dataset.

## 📁 Project Structure

The following is an example structure. Keep it synchronized with the actual files and folders in your GitHub repository.

```text
customer_shopping_behavior/
├── data/
│   └── customer_shopping_behavior.csv
├── outputs/
│   ├── customer_shopping_behavior_cleaned.csv
│   ├── data_quality_report.csv
│   ├── category_analysis.csv
│   └── age_group_analysis.csv
├── logs/
│   └── customer_shopping_behavior.log
├── shopping behavior.py
├── customer_shopping_behavior.sql
├── Customer_Shopping_Behavior_Analytics.pbix
└── README.md
```

Do not list files that are not present in the repository. If you organize the project into separate `python/`, `sql/`, `powerbi/`, and `reports/` directories, update this section to match the final structure.

## 🧠 Skills Demonstrated

- Python programming and data manipulation
- Pandas and NumPy
- Data cleaning and quality validation
- Missing-value treatment and duplicate checks
- Feature engineering
- Exploratory Data Analysis (EDA)
- SQL aggregations, subqueries, and window functions
- Customer and product analytics
- KPI development and business reporting
- Power BI and DAX
- Data visualization
- Analytical reasoning and business recommendations

## 🚀 Business Value

This project demonstrates how raw customer data can be transformed into structured analytical outputs and business-focused reporting.

It showcases an analytics workflow covering data quality, feature engineering, SQL-based business questions, exploratory analysis, and dashboard development. The results can help stakeholders investigate purchasing patterns, compare customer groups, and identify areas for further analysis.

## 👤 Author

**Prashant Marathe**

B.Tech — Artificial Intelligence & Data Science, 2026

**Target Roles:** Data Analyst | BI Analyst | Business Analyst | Junior SQL Developer

📍 Pune, Maharashtra, India

- **GitHub:** [MarathePrashant](https://github.com/MarathePrashant)
- **LinkedIn:** [Prashant Marathe](https://www.linkedin.com/in/prashantmarathe17)
- **Portfolio:** [View Portfolio](https://prashant-marathe.framer.website/)

* [GitHub](https://github.com/MarathePrashant)
* Email: [p04747391@gmail.com](mailto:p04747391@gmail.com)
