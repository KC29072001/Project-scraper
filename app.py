# This is the main script for running the web scraper. It contains the logic for initiating the scraping process, processing the scraped data, and saving it to a file.
# Key functions:
# main(): Starts the scraping process.
# standardize_data(df): Makes columns headings and their type for extracted data 
# scrape_and_standardize(urls): Scrapes them and standardize the data for each project according to standardize_data df format 


import os
import requests
import pandas as pd
import uuid
import logging
import streamlit as st
from bs4 import BeautifulSoup
from llm_extractor import extract_data_with_llm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('web_scraping_project')

def standardize_data(df):
    logger.info("Standardizing data")
    required_columns = [
        'original_id', 'aug_id', 'country_name', 'country_code', 
        'url', 'title', 'description', 'status', 'stages', 'date', 
        'procurementMethod', 'budget', 'currency', 'buyer', 
        'sector', 'subsector', 'map_coordinates', 'region_name', 
        'region_code'
    ]
    for col in required_columns:
        if col not in df.columns:
            df[col] = None

      # Convert data types as needed
    df['original_id'] = df['original_id'].astype(str)
    df['aug_id'] = df['aug_id'].astype(str)
    df['country_name'] = df['country_name'].astype(str)
    df['country_code'] = df['country_code'].astype(str)
    df['url'] = df['url'].astype(str)
    df['title'] = df['title'].astype(str)
    df['description'] = df['description'].astype(str)
    df['status'] = df['status'].astype(str)
    df['stages'] = df['stages'].astype(str)
    df['date'] = df['date'].astype(str)
    df['procurementMethod'] = df['procurementMethod'].astype(str)
    df['budget'] = df['budget'].astype(float)
    df['currency'] = df['currency'].astype(str)
    df['buyer'] = df['buyer'].astype(str)
    df['sector'] = df['sector'].astype(str)
    df['subsector'] = df['subsector'].astype(str)
    df['map_coordinates'] = df['map_coordinates'].astype(str)
    df['region_name'] = df['region_name'].astype(str)
    df['region_code'] = df['region_code'].astype(str)

    return df

def scrape_and_standardize(urls):
    logger.info("Starting the scraping and standardization process")
    all_data = []
    api_key = os.getenv('OPENAI_API_KEY')
    for url in urls:
        logger.info(f"Extracting data from {url}")
        data = extract_data_with_llm(url, api_key)
        all_data.extend(data)

    df = pd.DataFrame(all_data)
    standardized_df = standardize_data(df)
    return standardized_df

def main():
    st.title("Web Scraping and Data Standardization")

    # Get URLs input from the user
    urls_input = st.text_area("Enter URLs (one per line):")
    urls = urls_input.split('\n') if urls_input else []

    if st.button("Scrape and Standardize"):
        if urls:
            # Perform scraping and standardization
            df = scrape_and_standardize(urls)
            st.write(df)
            # Save to CSV file
            df.to_csv("extracted.csv", index=False)
            st.success("Data saved to extracted.csv")
        else:
            st.warning("Please enter at least one URL.")

if __name__ == "__main__":
    main()
