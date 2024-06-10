import openai
import requests
from bs4 import BeautifulSoup
import uuid

def extract_data_with_llm(url, api_key):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Use the language model to extract meaningful information
    openai.api_key = api_key
    # content = soup.get_text()
    body_text = soup.body.get_text(separator='\n', strip=True)
    prompt = f""" Extract all required information regarding projects from the following text: {body_text}"""
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1500
    )

    extracted_info = response.choices[0].message.content
    projects = parse_extracted_info(extracted_info, url)
    
    return projects

def parse_extracted_info(info, url):
    projects = []
    # Assuming the info is a list of projects in text form, parse it accordingly
    lines = info.split('\n')
    for line in lines:
        if line.strip():
            # Parse each line as a project (customize parsing as needed)
            project = {
                'original_id': str(uuid.uuid4()),
                'aug_id': str(uuid.uuid4()),
                'country_name': 'United States',
                'country_code': 'USA',
                'url': url,
                'title': 'Extracted Project Title',
                'description': line,
                'status': 'Unknown',
                'stages': 'Unknown',
                'date': 'Unknown',
                'procurementMethod': 'Unknown',
                'budget': 0.0,
                'currency': 'USD',
                'buyer': 'Unknown',
                'sector': 'Construction',
                'subsector': 'Infrastructure',
                'map_coordinates': '{"type": "Point", "coordinates": [0.0, 0.0]}',
                'region_name': 'Unknown',
                'region_code': 'Unknown'
            }
            projects.append(project)
    return projects

# def parse_extracted_info(info, url):
#     projects = []
#     # Assuming the info is a list of projects in text form, parse it accordingly
#     lines = info.split('\n')
#     for line in lines:
#         if line.strip():
#             # Extract relevant data from HTML elements on the webpage
#             soup = BeautifulSoup(line, 'html.parser')
#             # Extract data for each column dynamically with error handling
#             title = soup.find('h2').text.strip() if soup.find('h2') else None
#             description = soup.find('p').text.strip() if soup.find('p') else None
#             status = soup.find('span', class_='status').text.strip() if soup.find('span', class_='status') else None
#             stages = soup.find('span', class_='stages').text.strip() if soup.find('span', class_='stages') else None
#             date = soup.find('span', class_='date').text.strip() if soup.find('span', class_='date') else None
#             procurement_method = soup.find('span', class_='procurementMethod').text.strip() if soup.find('span', class_='procurementMethod') else None
#             budget = float(soup.find('span', class_='budget').text.strip()) if soup.find('span', class_='budget') else 0.0
#             currency = soup.find('span', class_='currency').text.strip() if soup.find('span', class_='currency') else 'USD'
#             buyer = soup.find('span', class_='buyer').text.strip() if soup.find('span', class_='buyer') else None
#             sector = soup.find('span', class_='sector').text.strip() if soup.find('span', class_='sector') else None
#             subsector = soup.find('span', class_='subsector').text.strip() if soup.find('span', class_='subsector') else None
#             map_coordinates = soup.find('span', class_='mapCoordinates').text.strip() if soup.find('span', class_='mapCoordinates') else '{"type": "Point", "coordinates": [0.0, 0.0]}'
#             region_name = soup.find('span', class_='regionName').text.strip() if soup.find('span', class_='regionName') else None
#             region_code = soup.find('span', class_='regionCode').text.strip() if soup.find('span', class_='regionCode') else None
            
#             # Create the project dictionary with extracted data
#             project = {
#                 'original_id': str(uuid.uuid4()),
#                 'aug_id': str(uuid.uuid4()),
#                 'country_name': 'United States',
#                 'country_code': 'USA',
#                 'url': url,
#                 'title': title,
#                 'description': description,
#                 'status': status,
#                 'stages': stages,
#                 'date': date,
#                 'procurementMethod': procurement_method,
#                 'budget': budget,
#                 'currency': currency,
#                 'buyer': buyer,
#                 'sector': sector,
#                 'subsector': subsector,
#                 'map_coordinates': map_coordinates,
#                 'region_name': region_name,
#                 'region_code': region_code
#             }
#             projects.append(project)
#     return projects














