# cord19_explorer.py
# End-to-end pipeline for CORD-19 metadata.csv
# Uses: pandas, matplotlib, seaborn, streamlit

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import re
from collections import Counter

sns.set(style="whitegrid")

# -----------------------------------------------------------
# Part 1 + 2: Load, Explore, and Clean
# -----------------------------------------------------------
@st.cache_data
def load_and_clean():
    # Load raw metadata
    df = pd.read_csv("metadata.csv", low_memory=False)

    # Drop columns with >70% missing
    missing_frac = df.isna().mean()
    cols_drop = missing_frac[missing_frac > 0.7].index
    df = df.drop(columns=cols_drop)

    # Drop rows without titles
    df = df.dropna(subset=["title"])

    # Parse dates
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["pub_year"] = df["publish_time"].dt.year

    # Abstract word count
    def word_count(text):
        if pd.isna(text):
            return 0
        return len(re.findall(r"\w+", str(text)))

    df["abstract_word_count"] = df["abstract"].apply(word_count)

    return df

df = load_and_clean()

# -----------------------------------------------------------
# Part 3: Data Analysis Functions
# -----------------------------------------------------------
def plot_publications_over_time(data):
    year_counts = data["pub_year"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8,4))
    sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o", ax=ax)
    ax.set_title("Publications Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    return fig

def plot_top_journals(data, n=10):
    top_journals = data["journal"].fillna("Unknown").value_counts().head(n)
    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax)
    ax.set_title(f"Top {n} Journals")
    ax.set_xlabel("Count")
    return fig

def plot_title_word_freq(data, n=15):
    def tokenize(title):
        title = str(title).lower()
        words = re.findall(r"[a-z]+", title)
        stopwords = {"the","and","for","with","from","this","that",
                     "covid","coronavirus","study","using"}
        return [w for w in words if w not in stopwords and len(w) > 2]

    all_words = []
    data["title"].dropna().apply(lambda t: all_words.extend(tokenize(t)))
    word_counts = Counter(all_words).most_common(n)

    if not word_counts:
        return None

    words, counts = zip(*word_counts)
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=list(counts), y=list(words), ax=ax)
    ax.set_title(f"Top {n} Words in Titles")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Word")
    return fig

def plot_top_sources(data, n=10):
    if "source_x" not in data.columns:
        return None
    top_sources = data["source_x"].fillna("Unknown").value_counts().head(n)
    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(x=top_sources.values, y=top_sources.index, ax=ax)
    ax.set_title(f"Top {n} Sources")
    ax.set_xlabel("Count")
    return fig

# -----------------------------------------------------------
# Part 4: Streamlit App
# -----------------------------------------------------------
st.set_page_config(page_title="CORD-19 Explorer", layout="wide")
st.title("CORD-19 Metadata Explorer")
st.write("End-to-end exploration of the metadata.csv from the CORD-19 dataset")

# Sidebar filters
years = df["pub_year"].dropna().astype(int)
if not years.empty:
    min_year, max_year = int(years.min()), int(years.max())
else:
    min_year, max_year = 2015, 2022

year_range = st.sidebar.slider("Select year range", min_year, max_year, (min_year, max_year))
journal_choice = st.sidebar.selectbox("Filter by journal", ["All"] + sorted(df["journal"].dropna().unique().tolist()))

# Apply filters
df_filtered = df[(df["pub_year"] >= year_range[0]) & (df["pub_year"] <= year_range[1])]
if journal_choice != "All":
    df_filtered = df_filtered[df_filtered["journal"] == journal_choice]

st.markdown(f"### Showing {len(df_filtered)} papers ({year_range[0]}–{year_range[1]}, journal: {journal_choice})")

# Layout with columns
col1, col2 = st.columns([2,1])
with col1:
    fig1 = plot_publications_over_time(df_filtered)
    st.pyplot(fig1)
with col2:
    fig2 = plot_top_journals(df_filtered)
    st.pyplot(fig2)

# Word frequencies
st.markdown("### Word Frequency in Titles")
fig3 = plot_title_word_freq(df_filtered)
if fig3:
    st.pyplot(fig3)
else:
    st.write("No title data available for analysis.")

# Sources
st.markdown("### Top Sources")
fig4 = plot_top_sources(df_filtered)
if fig4:
    st.pyplot(fig4)

# Show sample table
st.markdown("### Sample Data")
st.dataframe(df_filtered[["cord_uid","title","authors","journal","publish_time","abstract_word_count"]].head(20))

# Download option
@st.cache_data
def convert_to_csv(data):
    return data.to_csv(index=False).encode("utf-8")

csv = convert_to_csv(df_filtered)
st.download_button("Download Filtered Data", data=csv, file_name="metadata_filtered.csv", mime="text/csv")
