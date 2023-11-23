import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from model.Brands import Brands
from model.Deals import Deals
from model.Models import Models

deals = Deals()

#all_deals = deals.get_not_bought_cars(31,"autoscout", "true")
all_deals = deals.get_not_bought_cars_system(31,"autoscout", "true")

content = []
previous = ""
not_found = ""
for row in all_deals:

    #car_brand = row['brand'].decode('utf-8') if row['brand'] else ''
    #car_model = row['model'].decode('utf-8') if row['model'] else ''
    #km = row['km'].decode('utf-8') if row['model'] else ''
    #link = row['autoscoutLink'].decode('utf-8') if row['autoscoutLink'] else ''
    #reg_year = row['reg_date'].decode('utf-8') if row['reg_date'] else ''
    car_brand = row['brand']
    car_model = row['model']
    km = row['km']
    link = row['autoscoutLink']

    if link is not None and link != '':
        dealer_link = link.replace("/fahrzeuge", "")
        km_from = int(km) - 30000
        km_to = int(km) + 30000

        #timestamp_in_seconds = int(reg_year) / 1000
        #registration_year = datetime.fromtimestamp(timestamp_in_seconds)
        registration_year = row['registration_date']

        if car_brand == "VW":
            car_brand = "Volkswagen"

        parameter = ""
        link = ""
        found = False

        if 'autoscout24' in dealer_link:
            link = f"{dealer_link}?kmfrom={km_from}&kmto={km_to}&fregfrom={registration_year.year}&fregto={registration_year.year}&page=1"

            response = requests.get(link)
            http_code = response.status_code
        elif dealer_link:
            response = "error"
            http_code = 404

        if response and response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            try:
                next_data = soup.find(id='__NEXT_DATA__').get_text()
                data_json = json.loads(next_data)
                brand_list = data_json['props']['pageProps']['storageStoreSetupData']['availableMakes']
            except Exception as exception:
                # wronglink etiketine karşılık gelen Python kodu
                continue

            brands = Brands()
            if car_brand:
                brand = brands.get_by_name(car_brand, "autoscout24")
                if brand is not None:
                    if car_model:
                        models = Models()
                        model = models.get_by_name(car_model, brand.getId())
                        if model is not None:
                            parameter = f"&mmm=" + str(brand.getUrl()) + "%7C" + str(model.getUrl()) + "%7C"
                            found = "true"

            #filtrede marka var ise
            if found:
                response = requests.get(link + parameter)
                http_code = response.status_code

                if response and response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    try:
                        next_data = soup.find(id='__NEXT_DATA__').get_text()
                        data_json = json.loads(next_data)
                        model_list = data_json['props']['pageProps']['storageStoreSetupData']['availableModels']
                    except Exception as exception:
                        continue

                    print(link + parameter)
                    http_code = response.status_code
                    soup = BeautifulSoup(response.content, 'html.parser')
                    next_data = soup.find(id='__NEXT_DATA__').get_text()
                    data_json = json.loads(next_data)
                    car_list = data_json['props']['pageProps']['listings']
                    #benzer araç var ise
                    if len(car_list) > 0:

                        formatted_date = row['registration_date'].strftime('%Y-%m-%d')

                        content.append({
                            "appointmentId": row['appointmentId'],
                            "dealer_id": row['dealer_id'],
                            "client_id": row['client_id'],
                            "brand": row['brand'],
                            "model": row['model'],
                            "registration_date": formatted_date,
                            "km": row['km'],
                            "url": link + parameter
                        })
                        print(f"Found!! {row['appointmentId']}")

        if response.status_code == 404 and previous != row['dealer_id']:
            not_found += f"""
                <div danger style='margin:10px;padding:10px;background:#f8d7da;border:1px solid #f5c6cb;display:block;width:100%;color:#111;box-sizing:border-box;'>
                    Händler Autoscout24 Seite nicht gefunden <a target='_blank' href='index.php?page=dealers&type=aktiv&searchFilter=dealerNo&search={row['dealer_id']}'>{row['dealer_id']} - {row['company_name']}</a>
                </div>
            """
            previous = row['dealer_id']
    else:
        #url bulunmaz ise
        response = "empty"
        http_code = 404
        print(response)

if not_found != "":
    content.append({
        "not_found" : not_found
    })

print(content)
data = json.dumps(content)
print(data)

# Construct the URL (replace 'example.com' with the actual server name)
url = "https://system.wiveda.de/function/autoscoutFindCarList.php"

# Set up the headers
headers = {
    'Accept': 'de.gmbh.wiveda.api+json',
    'Content-Type': 'application/json',
    'Content-Length': str(len(data))
}

# Make the POST request
response = requests.post(url, data=data, headers=headers)

# Extract and print the result
result = response.text
print(result)