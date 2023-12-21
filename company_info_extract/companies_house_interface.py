import requests
from company_info_extract.urls import company_base
import configparser
import urllib
from datetime import date


config = configparser.ConfigParser()
config.read("config.ini")
token = config['global']['companyies_house_key']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
}


def company_house_base(company_symbol):
    existing_url = urllib.parse.urljoin(company_base,company_symbol)
    response = requests.get(existing_url,headers=headers,auth=(token,''))
    return response.json()

def company_house_filling_history(company_symbol):
    existing_url = urllib.parse.urljoin(company_base,company_symbol+'/filing-history')
    print(existing_url )
    response = requests.get(existing_url,headers=headers,auth=(token,''))
    return response.json()

def company_house_officers(company_symbol):
    response_dict = {}
    today = date.today()
    year = today.year
    existing_url = urllib.parse.urljoin(company_base,company_symbol+'/officers')
    print(existing_url )
    company_officers = requests.get(existing_url,headers=headers,auth=(token,'')).json()
    officers_list = []
    changes_in_current_year = []
    number_of_changes = 0
    for parts in company_officers['items']:
        officers = {}
        officers['name'] = parts['name']
        officers['appointment_data']  = parts['appointed_on']
        officers['officers_role'] = parts['officer_role']
        officers['date_of_birth'] = parts['date_of_birth']
        officers['country_of_residence'] = parts['country_of_residence']
        officers['address'] = f"""{parts['address']['address_line_1'].strip()}
        {parts['address']['locality'].strip()}
        {parts['address']['postal_code'].strip()}              
        """
        if str(year) in parts['appointed_on']:
            number_of_changes+=1
            changes_in_current_year.append(officers)
        officers_list.append(officers)
    response_dict['officers_list'] = officers_list
    response_dict['number_of_changes'] = number_of_changes
    response_dict['changes_in_current_year'] = changes_in_current_year
    return response_dict


def company_house_significant(company_symbol):
    existing_url = urllib.parse.urljoin(company_base,company_symbol+'/persons-with-significant-control-statements')
    print(existing_url )
    response = requests.get(existing_url,headers=headers,auth=(token,''))
    return response.json()