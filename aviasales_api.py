from requests_futures import sessions
from json import loads
import pandas as pd

def response_hook(response, *args, **kwargs):
    response.data = response.json()

session = sessions.FuturesSession()
session.hooks['response'] = response_hook

iata_codes = ['MOW', 'LED', 'KZN', 'CEK', 'SVX']    # Moscow, Saint Petersburg, Kazan, Chelyabinsk, Ekaterinburg

futures = [
    session.get("http://api.travelpayouts.com/v1/prices/calendar?origin={0}&destination={1}&depart_date=2021-03&token=101d5606239788bc02f0f52531623618".format(A, B))
    for A in iata_codes for B in iata_codes if A != B
]
results = [
    future.result()
    for future in futures
]

ds_results = []
res_dicts = [result.data['data'] for result in results]
for res_dict in res_dicts:
    for key in res_dict:
        ds_results.append((res_dict[key]['origin'], res_dict[key]['destination'],
            res_dict[key]['departure_at'], res_dict[key]['airline'],
                res_dict[key]['flight_number'], res_dict[key]['price'],
                    res_dict[key]['expires_at']))
## Fields: origin, destination, departure_at, airline, flight_number, price, expires_at, requested_at(?)

dataset = pd.DataFrame(ds_results)
dataset.columns = ['origin', 'destination', 'departure_at', 'airline',
    'flight_number', 'price', 'expires_at']
print(dataset.sample(3))
print(dataset.size)
dataset.to_csv('./aviasales_data.csv')
