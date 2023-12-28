import requests
class CountryDataFetcher:
    def __init__(self, url):
        self.url = url
        self.data = None
    def fetch_data(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.data = response.json()
                return "Data fetched successfully"
            else:
                return f"Failed to fetch data. Status code: {response.status_code}"
        except requests.RequestException as e:
            return f"Request Exception: {e}"

    def display_country_info(self):
        if self.data:
            for country_info in self.data:
                name = country_info.get('name', 'N/A')
                currencies = country_info.get('currencies')

                if currencies:
                    if isinstance(currencies, list):
                        currency_names = [currency.get('name', 'N/A') for currency in currencies if
                                          isinstance(currency, dict)]
                        currency_symbols = [currency.get('symbol', 'N/A') for currency in currencies if
                                            isinstance(currency, dict)]
                    elif isinstance(currencies, dict):
                        currency_names = [currencies.get('name', 'N/A')]
                        currency_symbols = [currencies.get('symbol', 'N/A')]
                    else:
                        currency_names = ['N/A']
                        currency_symbols = ['N/A']
                else:
                    currency_names = ['N/A']
                    currency_symbols = ['N/A']

                print(f"Country: {name}")
                print(f"Currencies: {', '.join(currency_names)}")
                print(f"Currency Symbols: {', '.join(currency_symbols)}")


    def countries_with_currency(self, currency_code):
        if self.data:
            currency_countries = []
            for country in self.data:
                currencies = country.get('currencies')

                if currencies:
                    if isinstance(currencies, list):
                        if any(currency.get('code') == currency_code for currency in currencies if
                               isinstance(currency, dict)):
                            currency_countries.append(country.get('name', 'N/A'))
                    elif isinstance(currencies, dict) and currencies.get('code') == currency_code:
                        currency_countries.append(country.get('name', 'N/A'))

            return currency_countries


# Given URL
given_url = "https://restcountries.com/v3.1/all"

# Creating an instance of CountryDataFetcher class with the provided URL
country_fetcher = CountryDataFetcher(given_url)

# Fetching data from the URL
fetch_result = country_fetcher.fetch_data()
print(fetch_result)

# Displaying country information
print("\nCountry Information:")
country_fetcher.display_country_info()

# Displaying countries with specific currencies
print("\nCountries with DOLLAR as currency:")
dollars = country_fetcher.countries_with_currency('USD')
print(dollars if dollars else "No countries found with DOLLAR as currency")

print("\nCountries with EURO as currency:")
euros = country_fetcher.countries_with_currency('EUR')
print(euros if euros else "No countries found with EURO as currency")
