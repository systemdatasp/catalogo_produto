import requests

url = "https://api.first.org/data/v1/countries"
response = requests.get(url)

if response.status_code == 200:

   data = response.json()
   
   country_data = data.get("data", {})
   
   print("Informações dos países:")
  
   for country_code, country_info in country_data.items():
       print(f"{country_code}-{country_info['country']}")
else:
    st.error(f"Erro ao acessar a API: {response.status_code}")
