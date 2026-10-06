# AI-Powered Data Analyst & Executive Decision Intelligence Dashboard

## Project Overview
This project is a production-style academic dashboard that turns raw sales data into verified business insight. Instead of a chart dump, it behaves like a virtual analyst: it cleans the data, calculates KPIs, identifies trends, measures drivers, predicts churn risk, forecasts sales, flags risk, detects opportunities, and recommends management actions.

## Problem Statement
Organizations often struggle to move from raw operational data to business decisions. Traditional dashboards show charts but do not explain what is happening, why it matters, what could go wrong, and what action should be taken. This project addresses that gap through a structured executive intelligence pipeline.

## Objectives
- Build a complete data cleaning and validation workflow
- Calculate robust business KPIs and trends
- Detect key revenue and profit drivers
- Model risk and churn intelligently
- Forecast near-term sales performance
- Produce structured AI-based executive findings grounded in verified data
- Deliver a professional dashboard suitable for an academic internship submission

## Features
- Executive overview with KPI cards
- Sales and product analysis
- Customer segmentation with RFM and K-Means
- Churn and risk scoring
- Sales forecasting
- Business risk detection engine
- Opportunity engine
- AI executive summary and action logic
- Interactive dashboard filters
- Data quality summary and graceful degradation when AI is unavailable

## Architecture
The system follows this business intelligence pipeline:

Raw Data → Clean Data → EDA → KPI Calculation → Trend Analysis → Driver Analysis → Prediction → Risk Detection → Opportunity Detection → AI Executive Analysis → Recommended Actions

## Technology Stack
- Python
- Pandas and NumPy
- Plotly
- Streamlit
- Scikit-learn
- Jupyter Notebook
- Joblib
- Matplotlib and Seaborn

## Dataset
The project generates a synthetic but realistic sales dataset when no existing dataset is provided. This ensures the dashboard runs immediately and demonstrates the full data pipeline. If an external dataset is added to data/raw/sales_data.csv, the app automatically uses it.

## Installation
```bash
cd AI_Data_Analyst
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## How to Run
```bash
streamlit run app/app.py
```

## AI Configuration
The project does not hardcode any API keys. If a real LLM provider is used later, configure environment variables such as OPENAI_API_KEY and update the AI analyst layer. The default implementation uses verified Python metrics and a rule-based executive summary so the system remains fully functional without external APIs.

## Dashboard Pages
- Executive Overview
- Sales & Product Analysis
- Customer & Risk Analysis

## ML Models
- RFM segmentation with K-Means
- Interpretable churn model based on customer behavior features
- Linear-trend sales forecasting

## Project Structure
```text
AI_Data_Analyst/
├── app/
│   ├── app.py
│   ├── components
│   └── pages
├── data/
│   ├── processed/
│   └── raw/
├── models/
├── notebooks/
├── reports/
├── src/
├── .gitignore
├── README.md
├── requirements.txt
└── ProjectReport.md
```

## Results
The dashboard focuses on meaningful business outcomes:
- revenue and profit performance
- sales trends and demand movement
- regional and category drivers
- product profitability
- customer risk and churn likelihood
- structured recommendations for management action

## Limitations
- The default dataset is synthetic and designed to demonstrate the full business intelligence pipeline.
- Real predictive accuracy depends on the quality and completeness of enterprise data.
- Some AI features are local and rule-based by design to keep the project reliable without external API dependencies.

## Future Scope
- Integrate live ERP and CRM data
- Add a true LLM layer with validated metric grounding
- Build automated scheduled reports
- Extend the dashboard into a multi-page enterprise analytics portal

## Author
AI Data Analyst Project for academic internship submission.
