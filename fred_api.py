# -*- coding: utf-8 -*-
"""
FRED API
@author: adam getbags
"""

# Import modules
import requests
import pandas as pd
from fred_key import fred_key

# Import or assign API key
api_key = fred_key
# api_key = 'abcdefgabcdefgabcdefg'

# Define the FRED API endpoint
base_url = 'https://api.stlouisfed.org/fred/'

'''
Get observation data from the FRED API
'''

# Assign endpoint
obs_endpoint = 'series/observations'

# Assign parameters
series_id = 'CPIAUCSL'
start_date = '2000-01-01'
end_date = '2023-06-30'
ts_frequency = 'q'
ts_units = 'pc1'

obs_params = {
    'series_id': series_id,
    'api_key': api_key,
    'file_type': 'json',
    'observation_start': start_date,
    'observation_end': end_date,
    # 'frequency': ts_frequency
    # 'units': ts_units
}

# Make request to FRED API
response = requests.get(base_url + obs_endpoint, params=obs_params)

# Format data
if response.status_code == 200:
    res_data = response.json()
    obs_data = pd.DataFrame(res_data['observations'])
    obs_data['date'] = pd.to_datetime(obs_data['date'])
    obs_data.set_index('date', inplace=True)
    obs_data['value'] = obs_data['value'].astype(float)

else:
    print('Failed to retrieve data. Status code:', response.status_code)

'''
Get category details
'''

# Assign endpoint
cat_endpoint = 'category'
cat_id = 0
# Assign params
cat_params = {
    'api_key': api_key,
    'file_type': 'json',
    'category_id': cat_id
}

# Make request to FRED API
response = requests.get(base_url + cat_endpoint, params=cat_params)

if response.status_code == 200:
    res_data = response.json()
    
else:
    print('Failed to retrieve data. Status code:', response.status_code)
    
'''
Get category children
'''

# Assign endpoint
child_endpoint = 'category/children'
parent_id = 0
# Assign params
child_params = {
    'api_key': api_key,
    'file_type': 'json',
    'category_id': parent_id
}

# Make request to FRED API
response = requests.get(base_url + child_endpoint, params=child_params)

if response.status_code == 200:
    res_data = response.json()
    
else:
    print('Failed to retrieve data. Status code:', response.status_code)

'''
Get series from category
'''

cat_id = '32455'
cat_srs_endpoint = 'category/series'
cat_srs_params = {
    'api_key': api_key,
    'file_type': 'json',
    'category_id': cat_id,
}

response = requests.get(base_url + cat_srs_endpoint, params=cat_srs_params)

if response.status_code == 200:
    cat_srs_data = response.json()
    cat_srs = pd.DataFrame(cat_srs_data['seriess'])
    cat_srs = cat_srs.sort_values(
        by='popularity', 
        ascending=False, 
        ignore_index=True
    )
else:
    print('Failed to retrieve data. Status code:', response.status_code)

'''
Get release ids
'''

rel_id_endpoint = 'releases'
rel_id_params = {
    'api_key': api_key,
    'file_type': 'json',
}

response = requests.get(base_url + rel_id_endpoint, params=rel_id_params)

if response.status_code == 200:
    rel_data = response.json()
    releases = pd.DataFrame(rel_data['releases'])

else:
    print('Failed to retrieve data. Status code:', response.status_code)

# Review data
print(releases[['id', 'name']])

'''
Get release series
'''

rel_srs_endpoint = 'release/series'
rel_srs_params = {
    'api_key': api_key,
    'file_type': 'json',
    'release_id': 10,
}

response = requests.get(base_url + rel_srs_endpoint, params=rel_srs_params)

if response.status_code == 200:
    rel_srs_data = response.json()
    rel_srs = pd.DataFrame(rel_srs_data['seriess'])

else:
    print('Failed to retrieve data. Status code:', response.status_code)

# Review the data // use limit and offset params to paginate
print(rel_srs)
print(rel_srs[['id','title']])

'''
Get source ids
'''

src_endpoint = 'sources'
src_params = {
    'api_key': api_key,
    'file_type': 'json',
}

response = requests.get(base_url + src_endpoint, params=src_params)

if response.status_code == 200:
    src_data = response.json()
    src = pd.DataFrame(src_data['sources'])
else:
    print('Failed to retrieve data. Status code:', response.status_code)

# Review data // sources are related to releases and vice versa
print(src[['id', 'name']])