import requests


class BreweryDataAnalyzer:
    def __init__(self, url):
        self.url = url

    def fetch_brewery_data(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException as e:
            print(f"Request Exception: {e}")
            return None

    def filter_breweries_by_states(self, data, states):
        if data:
            filtered_breweries = [brewery for brewery in data if brewery.get('state') in states]
            return filtered_breweries
        return []

    def count_breweries_by_state(self, data):
        state_counts = {}
        for brewery in data:
            state = brewery.get('state')
            state_counts[state] = state_counts.get(state, 0) + 1
        return state_counts

    def count_types_by_city(self, data, state):
        city_types_count = {}
        for brewery in data:
            if brewery.get('state') == state:
                city = brewery.get('city')
                brewery_type = brewery.get('brewery_type')
                if city:
                    if city not in city_types_count:
                        city_types_count[city] = {}
                    city_types_count[city][brewery_type] = city_types_count[city].get(brewery_type, 0) + 1
        return city_types_count

    def count_websites_by_state(self, data, states):
        website_count = {}
        for brewery in data:
            if brewery.get('state') in states and brewery.get('website_url'):
                state = brewery.get('state')
                website_count[state] = website_count.get(state, 0) + 1
        return website_count
# Given URL
given_url = "https://api.openbrewerydb.org/breweries"
# Creating an instance of BreweryDataAnalyzer class with the provided URL
brewery_analyzer = BreweryDataAnalyzer(given_url)
# Fetching brewery data
brewery_data = brewery_analyzer.fetch_brewery_data()

# Task 1: List names of breweries in specific states
target_states = ['Alaska', 'Maine', 'New York']
filtered_breweries = brewery_analyzer.filter_breweries_by_states(brewery_data, target_states)
breweries_names = [brewery['name'] for brewery in filtered_breweries]
print("Breweries in Alaska, Maine, and New York:")
print(breweries_names)

# Task 2: Count of breweries in each state
state_counts = brewery_analyzer.count_breweries_by_state(filtered_breweries)
print("\nCount of breweries in each state:")
print(state_counts)

# Task 3: Count of types of breweries in cities of specific states
for state in target_states:
    city_types_count = brewery_analyzer.count_types_by_city(filtered_breweries, state)
    print(f"\nCount of brewery types in cities of {state}:")
    for city, types_count in city_types_count.items():
        print(f"{city}: {types_count}")

# Task 4: Count and list breweries with websites in specific states
websites_count = brewery_analyzer.count_websites_by_state(brewery_data, target_states)
print("\nCount of breweries with websites in each state:")
print(websites_count)
