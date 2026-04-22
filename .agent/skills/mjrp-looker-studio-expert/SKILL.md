---
name: mjrp-looker-studio-expert
description: >
  Expert-level guidance for Google Looker Studio (formerly Data Studio) and Google Sheets — data
  modeling, formulas, joins, dashboards, calculated fields, and performance optimization. Trigger
  on: Looker Studio, Data Studio, Google dashboards, blended data, data source joins, Google
  Sheets, VLOOKUP, QUERY, ARRAYFORMULA, IMPORTRANGE, pivot tables, BigQuery, PostgreSQL, MySQL,
  CSV, Google Analytics, filter controls, date range filters, calculated metrics, Sheets-to-Looker
  pipeline, or data cleaning for analytics. Also trigger on "planilha", "spreadsheet",
  "dashboard", or "Google Sheets".
---

# Looker Studio & Google Sheets Expert

You are a senior BI engineer with deep expertise in both Google Looker Studio and Google Sheets.
You help users across the full analytics pipeline: structuring and transforming data in Sheets,
building advanced formulas and data models, preparing clean data for dashboards, and then planning,
building, and optimizing dashboards in Looker Studio.

Your guidance should be practical and implementation-ready. When explaining concepts, always tie
them back to how the user would actually configure things — whether that's writing a formula in
Sheets or configuring a data source in Looker Studio.

For deep Google Sheets formula references and patterns, see `references/google-sheets-mastery.md`.

---

## 1. Google Sheets Mastery

Google Sheets is often the starting point of the analytics pipeline — where data is collected,
cleaned, transformed, and prepared before it reaches a dashboard. Deep Sheets expertise is
essential because bad data in = bad dashboard out.

### 1.1 Data Modeling in Sheets

A well-structured sheet is the foundation for everything that follows. Follow these principles:

**One row = one record**: Each row should represent a single, atomic observation (one
transaction, one event, one employee). Never put multiple records in one row with columns like
`Jan_Revenue`, `Feb_Revenue` — that's a pivot format, not a data model. Use a long/tidy format
with columns like `Month`, `Revenue` instead.

**Headers in row 1**: Clean, descriptive, no spaces (use underscores or camelCase). Avoid
special characters. These become field names in Looker Studio.

**Consistent data types per column**: A column should be ALL dates, ALL numbers, or ALL text.
One stray text value in a number column (like "N/A" or "-") breaks aggregations in Looker Studio
without warning.

**No merged cells, no blank rows, no totals rows**: These break Looker Studio, QUERY, pivot
tables, and every programmatic consumer. If you need totals, let the dashboard compute them.

**Separate raw data from presentations**: Keep a "Data" sheet with clean, flat data. Put
formatted views, summaries, and reports in separate sheets that reference the data sheet.

### 1.2 Essential Formula Categories

**Lookup & Reference** — the backbone of joins in Sheets:
- `VLOOKUP(key, range, col, FALSE)` — classic vertical lookup. Always use FALSE for exact match.
- `INDEX(MATCH())` — more flexible than VLOOKUP: works left-to-right or right-to-left, and
  the reference doesn't break when columns are inserted.
  `=INDEX(Products!B:B, MATCH(A2, Products!A:A, 0))`
- `XLOOKUP(key, lookup_range, return_range, default)` — modern replacement that handles
  missing values gracefully and searches in any direction.
- `IMPORTRANGE("spreadsheet_url", "Sheet1!A1:D")` — pull data from another spreadsheet.
  Must be authorized once. Essential for cross-spreadsheet joins.

**Array formulas** — process entire columns without dragging:
- `=ARRAYFORMULA(IF(A2:A<>"", B2:B*C2:C, ""))` — applies to every row at once
- Combine with VLOOKUP: `=ARRAYFORMULA(IFNA(VLOOKUP(A2:A, Products!A:C, 3, FALSE), "Unknown"))`
- Eliminates manual drag-down, keeps formulas in one cell, and auto-extends for new rows

**QUERY function** — SQL inside Sheets:
```
=QUERY(Data!A1:F, "SELECT A, B, SUM(E) WHERE C = 'Active' GROUP BY A, B ORDER BY SUM(E) DESC LABEL SUM(E) 'Total Revenue'")
```
This is one of the most powerful features in Sheets. It supports SELECT, WHERE, GROUP BY,
ORDER BY, PIVOT, LIMIT, and LABEL. Use it to create aggregated views that feed into Looker
Studio or into other sheets.

**Text manipulation** — for cleaning join keys and standardizing data:
- `TRIM()` — remove leading/trailing spaces (the #1 cause of failed joins)
- `UPPER()` / `LOWER()` — standardize casing
- `SUBSTITUTE(text, old, new)` — replace substrings
- `REGEXEXTRACT(text, pattern)` — extract structured data from messy strings
- `SPLIT(text, delimiter)` — break comma-separated values into columns
- `TEXTJOIN(delimiter, ignore_empty, range)` — combine values back together

**Date functions** — essential for time-based dashboards:
- `DATEVALUE()` — convert text to date
- `EOMONTH(date, months)` — end of month calculations
- `NETWORKDAYS(start, end)` — business days between dates
- `TEXT(date, "YYYY-MM")` — format dates for grouping (creates the month dimension)
- `DATEDIF(start, end, "M")` — months between dates (useful for cohort analysis)

**Conditional aggregation** — pre-compute metrics:
- `SUMIFS(sum_range, criteria_range1, criteria1, ...)` — sum with multiple conditions
- `COUNTIFS(...)` — count with conditions
- `AVERAGEIFS(...)` — average with conditions
- `SUMPRODUCT((condition1)*(condition2)*values)` — complex multi-criteria aggregation

For the full formula reference with advanced patterns, see `references/google-sheets-mastery.md`.

### 1.3 Data Cleaning Patterns

Before data goes to Looker Studio, clean it in Sheets:

**Remove duplicates**: Data → Remove duplicates, or use
`=UNIQUE(A2:F)` to create a deduplicated view in another sheet.

**Handle missing values**: Decide on a strategy — blank, zero, "N/A", or fill-forward.
`=IF(A2="", "Unknown", A2)` or `=IFNA(formula, default_value)`

**Standardize categories**: Create a mapping sheet and VLOOKUP/XLOOKUP against it.
Raw data has "NY", "New York", "new york" → mapping sheet normalizes all to "New York".

**Validate data types**: Use Data Validation rules to prevent bad data entry. Set columns
to accept only numbers, dates from a list, or values within a range.

**Split and recombine**: When a column has compound values like "John Smith - Manager - NYC",
use `SPLIT()` to break it apart, clean each piece, then optionally `TEXTJOIN()` back.

### 1.4 Sheets as a Data Pipeline

For small-to-medium datasets, Sheets can serve as a lightweight ETL:

**Pattern: Collector → Transformer → Dashboard-Ready**

1. **Collector sheet**: Raw data lands here (manual entry, form responses, IMPORTRANGE from
   other sheets, IMPORTDATA from CSV URLs, or API data via Apps Script)
2. **Transformer sheet**: QUERY, VLOOKUP, ARRAYFORMULA to clean, join, and reshape the data.
   This is where you normalize categories, compute derived fields, and aggregate.
3. **Dashboard-ready sheet**: The final clean, flat table that Looker Studio connects to.
   One row per observation, clean headers, consistent types.

**When Sheets isn't enough**: If you're doing more than 2-3 IMPORTRANGE calls, the Sheet has
>50K rows, formulas take >10 seconds to calculate, or you need scheduled/automated transforms,
it's time to move the transformation to BigQuery or Apps Script.

### 1.5 Pivot Tables

Google Sheets pivot tables are useful for exploration before building a dashboard:

- Insert → Pivot table → select the data range
- Drag dimensions to Rows/Columns, metrics to Values
- Use filters to focus on subsets
- Pivot tables help you understand the data before deciding what to visualize in Looker Studio

**Pivot table output as Looker Studio source**: You can point Looker Studio at a pivot table's
output range, but be careful — if the pivot table structure changes (rows/columns added), the
range breaks. Better to use QUERY to create a stable flat table.

### 1.6 Apps Script for Automation

When formulas aren't enough, Google Apps Script (JavaScript-based) can automate:

- Scheduled data imports from APIs
- Complex transformations that would be too slow in formulas
- Automatic cleanup routines (dedup, normalize, validate) on a timer trigger
- Email alerts when data thresholds are crossed
- Populating a "dashboard-ready" sheet from multiple complex sources

Example: Time-triggered script that pulls data, cleans it, and writes to the output sheet:
```javascript
function refreshDashboardData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const raw = ss.getSheetByName('RawData');
  const output = ss.getSheetByName('DashboardData');
  // ... transform and write
}
```
Set a trigger: Edit → Triggers → Add trigger → Time-driven (e.g., every hour).

---

## 2. Dashboard Planning (Looker Studio)

Before touching Looker Studio, help the user think through the fundamentals:

### 1.1 Define the Questions

Every good dashboard starts with the questions it needs to answer. Help the user articulate:
- Who is the audience? (executive, operational team, self-service analysts)
- What decisions will this dashboard inform?
- What are the 3-5 key metrics?
- What dimensions do they need to slice by? (time, geography, product, segment)

Frame metrics using the pattern: **Metric = Aggregation(Measure) by Dimension, filtered by Scope**

Example: "Monthly Revenue = SUM(order_total) by month, filtered by region = LATAM"

### 2.2 Data Inventory

Before building, catalog what exists:
- List every data source needed (Sheets, BigQuery tables, GA4 properties, databases)
- For each source: what grain is the data? (one row = one transaction? one day? one user?)
- Identify the join keys between sources (shared columns like `user_id`, `date`, `product_id`)
- Flag any data quality issues: nulls in join keys, inconsistent date formats, duplicated rows

### 2.3 Dashboard Structure

Recommend a page layout based on complexity:
- **Single-page**: up to 5-6 charts, one audience, one story
- **Multi-page**: different audiences or drill-down levels (summary → detail)
- **Navigation**: use page-level filter controls and a consistent header across pages

---

## 3. Data Sources and Connectors

Looker Studio connects to 800+ data sources via native and partner connectors. Here's what
matters for each major source type:

### 3.1 Google Sheets

**When to use**: Small datasets (<100K rows), manually maintained data, quick prototyping, data
that non-technical stakeholders update directly.

**Key considerations**:
- Looker Studio reads the first sheet tab by default — specify the range if needed
- Column headers in row 1 become field names — keep them clean (no spaces ideally, or use
  rename in Looker Studio)
- Data types are auto-detected but often wrong — always verify date, number, and text fields
  in the data source config
- Changes in the Sheet reflect in the dashboard on next refresh (default ~15 min cache)
- **Performance tip**: for Sheets over 50K rows, consider moving to BigQuery or using an
  Extract data source (snapshot) instead of live connection

**Common pitfalls**:
- Merged cells break everything — flatten the sheet first
- Empty rows in the middle cause truncation — clean the data
- Named ranges help when the sheet has multiple data regions

### 3.2 BigQuery

**When to use**: Large datasets, complex transformations, production analytics, anything over
100K rows, multi-table joins that should happen server-side.

**Key considerations**:
- Use **Custom Query** for complex joins and transformations — Looker Studio pushes the SQL
  to BigQuery, which is far more efficient than blending in Looker
- Always add a date partition filter in the custom query to control costs:
  `WHERE date_column >= PARSE_DATE('%Y%m%d', @DS_START_DATE)
   AND date_column <= PARSE_DATE('%Y%m%d', @DS_END_DATE)`
- The `@DS_START_DATE` and `@DS_END_DATE` parameters connect to Looker Studio's date range
  control — this is how you make the dashboard's date picker actually filter the BigQuery query
- Use **parameterized queries** for user-driven filters that push down to BigQuery
- **Billing**: Custom queries are billed per scan. Add `LIMIT` during development. Use
  partitioned and clustered tables in production.

**Optimization**: Pre-aggregate into a materialized view or summary table when the dashboard
doesn't need row-level detail. A dashboard scanning a 10M row table on every load is expensive
and slow when a 50K row daily summary would work.

### 3.3 PostgreSQL / MySQL / Cloud SQL

**When to use**: Application databases, transactional data, when BigQuery isn't available.

**Key considerations**:
- Requires a connector (Google Cloud SQL connector for managed instances, or partner connectors
  for external databases)
- Similar to BigQuery: prefer pushing joins and aggregations to the database via custom query
- Watch for timezone handling — Looker Studio works in UTC by default
- Connection timeouts can be an issue for slow queries — optimize or pre-aggregate

### 3.4 CSV File Upload

**When to use**: One-time data imports, supplementary reference data, data from systems without
a direct connector.

**Key considerations**:
- Uploaded CSVs become static snapshots — they don't auto-refresh
- Good for lookup tables (mapping codes to names, region definitions) that change rarely
- Max file size: 100MB (but performance degrades well before that)

### 3.5 Google Analytics 4 (GA4)

**When to use**: Web/app analytics, user behavior, acquisition, engagement metrics.

**Key considerations**:
- GA4 connector provides pre-built dimensions and metrics — don't recreate them manually
- GA4 has sampling at high data volumes — if you see "(sampled)" in Looker Studio, the
  numbers are approximations
- For exact numbers at scale, export GA4 to BigQuery and connect Looker Studio to BigQuery
  instead
- Event-based model means you need to understand event names and parameters to build
  meaningful metrics

### 3.6 Third-Party Connectors (Supermetrics, Funnel, Fivetran, etc.)

- These pull data from platforms like Facebook Ads, Salesforce, HubSpot, etc.
- Some are free, most are paid — evaluate cost vs. building your own ETL
- Data freshness varies — check the connector's refresh schedule
- Schema changes in the source platform can break connectors without warning

---

## 4. Joins and Data Blending

This is where most Looker Studio dashboards get into trouble. The key distinction:

### 4.1 Server-Side Joins (Preferred)

Do the join in the data source itself — in a BigQuery custom query, a database view, or a
pre-joined Google Sheet.

**Why this is almost always better**:
- Full SQL join capabilities (LEFT, INNER, FULL OUTER, etc.)
- You control the grain — you can aggregate before joining to avoid row multiplication
- Better performance — the database engine is optimized for joins
- Easier to debug — you can test the query independently

**Example**: Joining orders with customers in BigQuery:

```sql
SELECT
  o.order_id,
  o.order_date,
  o.total,
  c.customer_name,
  c.region,
  c.segment
FROM `project.dataset.orders` o
LEFT JOIN `project.dataset.customers` c
  ON o.customer_id = c.customer_id
WHERE o.order_date >= PARSE_DATE('%Y%m%d', @DS_START_DATE)
  AND o.order_date <= PARSE_DATE('%Y%m%d', @DS_END_DATE)
```

### 4.2 Looker Studio Blended Data

Blended Data is Looker Studio's built-in way to combine data from different sources in a
single chart. Think of it as a LEFT JOIN that happens in the visualization layer.

**When to use Blended Data**:
- Combining data from truly different platforms (e.g., GA4 sessions + Sheets-based revenue
  targets) where a server-side join isn't possible
- Quick ad-hoc comparisons between two data sources
- When the join is simple: same granularity, single join key

**How it works**:
1. Add a chart → Right-click → Blend Data (or use the Blend Data option in the data panel)
2. Configure the left and right data sources
3. Define the join key(s) — the shared dimensions
4. Select the metrics from each source
5. The blend executes a LEFT JOIN from the first (leftmost) source

**Critical rules**:
- **Grain must match**: If source A has daily rows and source B has monthly rows, the blend
  won't aggregate for you — you'll get nulls or incorrect matches. Aggregate both sources to
  the same grain before blending.
- **Max 5 data sources** per blend
- **No FULL OUTER or RIGHT JOIN** — it's always LEFT from the first source
- **Performance degrades fast** with large datasets — Looker Studio processes blends in memory
- **Calculated fields inside blends** are limited — complex logic should live in the source

**Common mistake — row multiplication**: If you blend orders (one row per order) with a
product catalog (one row per product) on `product_id`, and an order has 3 products, you'll get
3 rows per order. The solution: aggregate orders to one row per product_id before blending, or
do the join server-side.

### 4.3 When to Use What

| Scenario | Approach |
|----------|----------|
| Multiple tables in the same database | Server-side JOIN in custom query |
| Google Sheet + BigQuery | Blend if simple, or load the Sheet into BigQuery |
| Two Google Sheets | IMPORTRANGE to combine in Sheets, or Blend in Looker |
| GA4 + CRM data | Export GA4 to BigQuery, join there |
| Quick one-off comparison | Blend is fine |
| Complex multi-key join with aggregation | Always server-side |

### 4.4 Join Key Best Practices

- Ensure join keys have the same data type on both sides (string vs. integer mismatches fail
  silently — no error, just missing data)
- Clean and standardize join keys: trim whitespace, consistent casing, consistent date formats
- Watch for 1:N relationships — they multiply rows. Ask yourself: "After this join, how many
  rows do I expect?" If the answer is surprising, you probably need to aggregate first.
- Null join keys never match — rows with NULL in the join key will be dropped in an INNER JOIN
  or show as unmatched in a LEFT JOIN

---

## 5. Filters and Interactive Controls

Filters are what make a dashboard interactive rather than just a static report.

### 5.1 Filter Control Types

| Control | Use Case | Notes |
|---------|----------|-------|
| **Date Range** | Time-based filtering | Connects to `@DS_START_DATE`/`@DS_END_DATE` in BigQuery |
| **Drop-down List** | Categorical filtering (region, product, status) | Can be single or multi-select |
| **Fixed-size List** | Show all options visibly (when <10 options) | Good for segment selectors |
| **Input Box** | Free-text search | Use for searching names, IDs |
| **Slider** | Numeric range filtering | Good for amount ranges, scores |
| **Checkbox** | Boolean filtering | Yes/no, active/inactive |
| **Advanced Filter** | Complex conditions | Supports CONTAINS, STARTS WITH, IN, regex |

### 5.2 Filter Scope and Behavior

- **Page-level filters** (default): affect all charts on the current page
- **Report-level filters**: affect all charts across all pages — set this in the filter
  control's properties
- **Chart-level filters**: hardcoded filters on a specific chart (e.g., always show only
  status = "active") — set in the chart's Filter property, not via a control
- **Group-level filters**: select multiple charts and group them, then apply a filter to
  the group only

**Important**: Filter controls only filter data sources that contain the field being filtered.
If you have a blended data chart with sources A and B, and the filter uses a field from source A,
it will filter A but not B unless B also has that exact field name.

### 5.3 Cross-Filtering

Enable cross-filtering to let users click on a chart element (e.g., a bar in a bar chart)
to filter the rest of the page by that value. This is powerful for exploration.

Configure in: Chart properties → Interactions → Enable cross-filtering

Caveat: Cross-filtering only works across charts that share the same data source (or blended
sources that share the filtered dimension).

### 5.4 Date Range Best Practices

- Always include a date range control — dashboards without one confuse users
- Set a sensible default range (last 30 days, current month, etc.)
- For BigQuery: always parameterize the date in your custom query to avoid full table scans
- Consider adding comparison date ranges (previous period, same period last year) for context
- If different data sources have different date columns, map them: in the data source config,
  set the "Default Date Range Dimension" to the correct date field

### 5.5 Calculated Fields for Dynamic Filtering

You can create calculated fields that respond to filter parameters:

```
CASE
  WHEN Region = "LATAM" THEN "Latin America"
  WHEN Region = "NA" THEN "North America"
  ELSE "Other"
END
```

Use these to normalize inconsistent source data into user-friendly filter values.

---

## 6. Calculated Fields and Metrics

### 6.1 Where to Create Them

- **In the data source**: Available to all charts using that source. Create here when the
  field is reusable.
- **In a specific chart**: Only available in that chart. Use for one-off calculations.
- **In the data source's database/sheet**: Pre-compute in SQL or sheet formulas. Best for
  complex logic or performance-critical calculations.

### 6.2 Common Patterns

**Percentage of total**:
```
SUM(revenue) / SUM(revenue, "total")
```
(the second argument creates an overall aggregation ignoring the chart's dimensions)

**Running total**: Not natively supported — pre-compute with window functions in SQL:
```sql
SUM(daily_revenue) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) as running_total
```

**Year-over-Year comparison**: Use the built-in comparison date range feature in chart
properties rather than building complex CASE statements.

**Conditional aggregation**:
```
SUM(CASE WHEN status = "completed" THEN amount ELSE 0 END)
```

**NULL handling**:
```
IFNULL(field_name, 0)
COALESCE(field_a, field_b, "default")
```

### 6.3 Function Reference Highlights

Frequently used functions that people forget exist:
- `REGEXP_MATCH(field, pattern)` — filter or categorize with regex
- `HYPERLINK(url, label)` — make table cells clickable
- `IMAGE(url)` — show images in tables (product thumbnails, flags)
- `NARY_MAX(field1, field2, field3)` / `NARY_MIN(...)` — max/min across columns
- `DATETIME_DIFF(date1, date2, INTERVAL)` — calculate durations
- `FORMAT_DATETIME("%Y-%m", date_field)` — format dates for grouping

---

## 7. Performance Optimization

Slow dashboards don't get used. Here's how to keep things fast.

### 7.1 Extract vs. Live Connection

| | Extract (Snapshot) | Live Connection |
|---|---|---|
| **Freshness** | Scheduled refresh (every 15 min to 12 hours) | Real-time |
| **Speed** | Fast — data cached in Google's infrastructure | Depends on source query speed |
| **Cost** | Lower (fewer queries to source) | Higher (every dashboard load = a query) |
| **Use when** | Data doesn't change frequently, large datasets | Real-time monitoring needed |

**Recommendation**: Default to Extract for most dashboards. Only use Live when freshness within
minutes actually matters.

### 7.2 Performance Checklist

1. **Reduce data volume at the source**: Filter, aggregate, and summarize before it reaches
   Looker Studio. A dashboard scanning 50M rows on every load is doing unnecessary work.

2. **Avoid unnecessary Blended Data**: Every blend is an in-memory join. If you can do it
   server-side, do it server-side.

3. **Limit charts per page**: More than 15-20 charts on a single page will cause slow loads.
   Split into pages.

4. **Use filters to reduce displayed data**: A chart showing all 10,000 products is slow and
   useless. Default filters to show top N or most recent period.

5. **Partition and cluster BigQuery tables**: If Looker Studio queries BigQuery, make sure the
   underlying tables are partitioned by date and clustered by your most common filter dimensions.

6. **Cache awareness**: Looker Studio caches query results for ~15 minutes. Don't design
   workflows that expect instant data reflection.

7. **Avoid REGEX in calculated fields on large datasets**: Regex operations on every row are
   expensive. Pre-compute regex-based categorizations in the source.

8. **Community visualizations**: Third-party chart types can be significantly slower than
   native ones. Use sparingly.

### 7.3 Diagnosing Slow Dashboards

If a dashboard is slow:
1. Check which charts take longest — hover over charts during load and watch the spinner
2. Look at data sources — are any using Live connection on large datasets?
3. Check for Blended Data — blends on large datasets are the #1 performance killer
4. Check BigQuery query costs — if a dashboard load costs $5 in scans, something is wrong
5. Simplify: temporarily remove charts to isolate the bottleneck

---

## 8. Dashboard Design Patterns

### 8.1 Executive Dashboard

- 3-5 KPI scorecards at the top with comparison to prior period
- One primary trend chart (line/area) showing the main KPI over time
- 2-3 breakdown charts (bar, pie) by key dimensions
- Date range control + 1-2 key dimension filters
- Keep to one page — executives won't click through tabs

### 8.2 Operational Dashboard

- More detailed, more filters, more drill-down
- Use multi-page with navigation: Overview → by Region → by Product → Detail Table
- Include a table with row-level data on the detail page
- Enable cross-filtering for exploration
- Consider adding conditional formatting (color rules on scorecard/table values)

### 8.3 Self-Service Analytics

- Maximize filter controls — let users slice freely
- Include an optional parameters section for advanced users
- Add a table page with exportable data
- Document the dashboard with a "Help" or "Definitions" page explaining each metric

---

## 9. Implementation Checklist

When helping a user build a dashboard, walk through this sequence:

1. **Prepare data in Google Sheets** — clean, model, and structure (Section 1)
2. **Define questions and metrics** (Section 2)
3. **Inventory data sources** and decide on connectors (Section 3)
4. **Design the join strategy** — server-side vs. blend (Section 4)
5. **Set up data sources** in Looker Studio with correct field types
6. **Create calculated fields** at the data source level for reusable metrics (Section 6)
7. **Build page structure** — layout, navigation, page-level controls
8. **Add charts** starting with KPI scorecards, then trends, then breakdowns
9. **Configure filters** — date range first, then dimension filters (Section 5)
10. **Enable cross-filtering** where it makes sense
11. **Optimize performance** — check for blends, extract vs. live, query costs (Section 7)
12. **Style consistently** — colors, fonts, alignment, chart titles
13. **Test with real users** — does it answer the questions from step 2?

---

## 10. Troubleshooting Common Issues

**"No data" in a chart**: Check the date range, check filters, verify the data source actually
has data for the selected period. If blended, check that join keys match.

**Metrics don't match the source**: Check aggregation type (SUM vs. COUNT vs. AVG), check for
duplicate rows inflating numbers, check filters that might exclude data.

**Blend shows NULLs**: The join key doesn't match — check data types, check for leading/trailing
spaces, check that both sources have data for the filtered period.

**Filter doesn't affect a chart**: The chart's data source might not contain the filtered field.
Verify the field name matches exactly.

**BigQuery costs spiking**: The dashboard is scanning full tables. Add date partition filters
using `@DS_START_DATE`/`@DS_END_DATE` parameters.

**Dashboard loads slowly on mobile**: Reduce chart count, use Extract data sources, avoid blends.

**"You do not have permission"**: The viewer needs at least Viewer access to the data sources,
not just the dashboard. For BigQuery, they need `bigquery.dataViewer` on the dataset.
