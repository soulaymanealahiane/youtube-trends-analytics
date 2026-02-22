# 📊 Global YouTube Trends & Engagement Analytics

## 📑 Project Overview
This project is an end-to-end data engineering and business intelligence solution designed to analyze global YouTube trending metrics across 113 countries. The goal of this project was to move beyond "vanity metrics" (raw view counts) and uncover the true drivers of audience engagement and content virality.

Architected a Python-based ETL (Extract, Transform, Load) pipeline to process a massive, memory-heavy dataset (\~5.87 GB, 1M+ rows), performing dimensionality reduction, geospatial extraction, and feature engineering. The optimized data was then visualized using Tableau to deliver actionable business insights.

## 💡 Key Business Insights

1. **The "Viral Dilution" Effect:** Higher view volumes directly correspond with proportionally lower engagement rates. Massive reach guarantees eyeballs, but actively dilutes audience interaction.

2. **Engagement Inequality (The 1% Rule):** The vast majority of platform content clusters at the absolute lowest engagement levels. Only a fractional percentage of videos achieve highly concentrated engagement.

3. **Scale-Adjusted Leaders:** By controlling for view scale, identified "Hidden Champion" creators who consistently outperform market averages in pure engagement quality, regardless of subscriber count.

4. **Geographic Momentum:** Consumption behavior and engagement thresholds vary drastically by nation, proving that global platforms require hyper-localized content strategies.

## 🛠️ Data Architecture & Pipeline

The raw dataset from Kaggle contained heavy unstructured text fields that caused memory overflow errors in standard analytics tools. Built a Python pipeline to optimize the data for Tableau:

1. **Dimensionality Reduction (`remove_columns.py`):** Utilized Pandas chunking/streaming to surgically drop unstructured NLP columns (Descriptions, Tags, Thumbnails) without loading the 6GB file into RAM.

2. **Geospatial Extraction (`extract_unique_countries_arr.py`):** Applied Regular Expressions (Regex) to clean and extract standardized ISO-2 country codes. We then integrated the `countries_geocoding_data.csv` lookup table to accurately map these country codes to precise latitude and longitude coordinates, optimizing the data for Tableau's geospatial mapping engine.

3. **Feature Engineering (`stats_columns_addition.py`):**
    * **Standardization:** Calculated `engagement_rate`, `like_ratio`, and `comment_ratio` to combat big-channel bias.
    * **Anomaly Detection:** Deployed the Interquartile Range (IQR) method to identify viral videos. Instead of deleting these outliers, engineered an `is_view_outlier` boolean flag to allow dynamic dashboard filtering.

*Result: A pristine analytical dataset reduced in size by over 90%, ready for seamless ingestion.*

## 📂 Repository Structure
```
├── data/
│   ├── Cleaned_Data_Sample.csv          # Sample of the final processed dataset
│   ├── Raw_data_Sample.csv              # Sample of the original dataset structure
│   └── countries_geocoding_data.csv     # Geospatial mapping data (Latitude/Longitude)
├── scripts/
│   ├── downloader.py                    # Kaggle API script to fetch full raw data
│   ├── first_500000_rows.py             # Utility to chop data rows (Alternative memory approach)
│   ├── remove_columns.py                # Pipeline Step 1: Stream chunking & dropping
│   ├── extract_unique_countries_arr.py  # Pipeline Step 2: Regex geospatial extraction
│   └── stats_columns_addition.py        # Pipeline Step 3: Feature engineering & Outliers
├── dashboards/
│   ├── dashboard_1_geography.png        # Language & Geographic Demand Dash
│   └── dashboard_2_engagement.png       # Engagement & Momentum Dash
├── docs/
│   └── presentation_lastdraft.html      # Interactive HTML Presentation Deck with business recommendations
└── README.md
```

## 📥 Data Access & Reproduction

**⚠️ Important Note on Data Files:** Due to GitHub's strict 100MB file size limit, the full 5.87 GB raw dataset and the final 1M+ row cleaned dataset **are not hosted in this repository**. The `data/` directory contains small *samples* (`Raw_data_Sample.csv` and `Cleaned_Data_Sample.csv`) alongside the auxiliary `countries_geocoding_data.csv` so you can view the schema and transformations.

**To reproduce the full pipeline, you must fetch the data locally:**

1. **Download the Full Dataset:**
   Run the included `downloader.py` script to automatically fetch the latest 6GB dataset via the Kaggle API to your local machine:

```python scripts/downloader.py```


*Alternatively, download it manually from the [Kaggle Dataset Page](https://www.kaggle.com/datasets/asaniczka/trending-youtube-videos-113-countries?select=trending_yt_videos_113_countries.csv).*

2. **Install Dependencies:**

```pip install pandas numpy kagglehub openpyxl```


3. **Execute the ETL Pipeline:**
Update the `INPUT_PATH` and `OUTPUT_PATH` variables inside the scripts to match your local data directory, then run:

```
python scripts/remove_columns.py
python scripts/stats_columns_addition.py
```


4. **Visualize:** Import your newly generated `final_tableau_dataset.csv` into Tableau to recreate the analytical dashboards.

## 📈 Tableau Dashboards

### 1. Global Views & Language Dominance

Explores macro-trends, tracking how viewing volume shifts across languages, regions, and seasonal timelines.

### 2. Engagement Performance & Momentum Analytics

Analyzes the granular quality of creator interactions, proving the "Viral Dilution" theory and highlighting regional momentum


