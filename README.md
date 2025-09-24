# CORD-19 Metadata Explorer

This project provides an **interactive Streamlit web app** to explore the [CORD-19 dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) metadata (`metadata.csv`). 
Please download only the metadata.csv file from the CORD-19 dataset

The app loads, cleans, and analyzes the metadata, then allows you to interactively:
- Filter papers by publication year and journal
- Visualize publication trends over time
- See which journals and sources have published the most
- Explore frequent words in paper titles
- Browse and download a filtered subset of the dataset

---

## ⚙️ Environment Setup

### 1. Clone or download this repo
```bash
git clone <your-repo-url>
cd <your-repo-folder>

### 2. Install dependencies

This project only needs pandas, matplotlib, seaborn, and streamlit:

### 3. ▶️ Run the App

Launch the Streamlit app with:
streamlit run frameworks.py
Your browser will open automatically at http://localhost:8501


# 📊 Features of the App
Sidebar Filters

Year range slider: Limit results to a specific publication period

Journal dropdown: Focus on one journal or view all

Visualizations

Publications over Time
Line plot showing the number of papers published per year

Top Journals
Bar chart of the most common journals in the dataset

Word Frequency in Titles
Bar chart of the most frequent words in paper titles (common stopwords removed)

Top Sources
Bar chart showing which sources contributed the most papers (if source_x column is present)

Data Table

Displays sample rows of the filtered dataset (cord_uid, title, authors, journal, publish_time, abstract_word_count)

Download Option

Export the filtered dataset as a CSV file with one click


# 🧹 Data Cleaning Steps

Removed columns with >70% missing values

Dropped rows without titles

Converted publish_time to datetime

Extracted pub_year from publication date

Added abstract_word_count column


# 📂 Project Structure
.
├── cord19_explorer.py   # Main Streamlit app script
├── metadata.csv         # Raw dataset (place here after download)
└── README.md            # Documentation


# 📝 Notes

metadata.csv is large — loading may take some time.

Some records lack abstracts, journals, or dates — cleaning handles these gracefully.

Frequent words in titles exclude common stopwords and very short tokens.

If you want faster load times, you can sample a subset of rows when loading the CSV.



