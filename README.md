# Automated Multi-Source Currency API Pipeline

An automated data pipeline that connects to a live financial REST API, extracts real-time foreign exchange data relative to the Zambian Kwacha (ZMW), normalizes the fields using pandas, and appends the structured results into an analytical MySQL layer.

## Tech Stack & Skills Highlighted
- **API Extraction:** Python `requests` library (REST API endpoint ingestion, handling JSON payloads)
- **Data Manipulation:** Python `pandas` (Metadata timestamp injection, subset filtering, schema structuring)
- **Database Engine:** MySQL 8.4+ Relational Storage Layer
- **Database Connectivity:** `SQLAlchemy` & `mysql-connector-python`

## Pipeline Architecture Design
1. **Extract:** Programmatically dials a live financial web registry to capture real-time currency fluctuations.
2. **Transform:** Standardizes time zones into clean dates, extracts metadata parameters, and narrows focus to regional trading values (`ZMW`, `ZAR`, `CNY`, `GBP`).
3. **Load:** Automatically maps data types and updates the analytical storage cache table (`dim_currency_rates`).
