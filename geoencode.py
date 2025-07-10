from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import json

# Your location data, could be a list or DataFrame column
df = pd.read_csv("kecelakaan-with-location-raw.csv")


# Init geocoder
geolocator = Nominatim(user_agent="kecelakaan-ner-mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

results = []

known_locations = {
    "jalan kaliurang": "jalan kaliurang",
    "jakal": "jalan kaliurang",
    "sedayu": "sedayu",
    "Jl kabupaten": "Jl kabupaten",
    "jalan kabupaten": "Jl kabupaten",
    "wates": "Jl wates",
    "selokan mataram": "selokan mataram",
    "ringroad": "ringroad", 
    "Bantul": "Bantul",
    "Sleman": "Sleman",
    "Yogyakarta": "Yogyakarta",
    "Kulon Progo": "Kulon Progo",
    "Gunung Kidul": "Gunung Kidul",
    "Kota Yogyakarta": "Kota Yogyakarta",
    "sagan": "sagan",
    "prambanan": "prambanan",
    "pakualaman": "pakualaman",
    "semanu": "jl semanu",
    "UPN": "UPN",
    "UII": "UII",
    "selomartani": "selomartani",
    "Turi": "Turi",
    "sungai gajah": "gajah wong",
    "siyono": "siyono",
    "kentungan": "kentungan",
    "tugu": "malioboro",
}

df.fillna("", inplace=True)

def geoencode(locations):
    if locations == "":
        return None
    location_list = json.loads(locations)
    location_result = []
    for loc in location_list:
        location = geocode(loc + ", Yogyakarta, Indonesia")
        if location is None:
            print("Location not found: ", loc)
            for kabupaten in known_locations.keys():
                if kabupaten.lower() in loc.lower():
                    location = geocode(known_locations[kabupaten] + ",Yogyakarta, Indonesia")
                    print("Location found: ", location)
                    location_result.append((location.latitude, location.longitude))
                    break
            if location is None:
                location = geocode("Yogyakarta, Indonesia")
                location_result.append((location.latitude, location.longitude))
    if len(location_result) == 0:
        return None
    # take location average for each latitude and longitude
    latitude_list = [loc[0] for loc in location_result]
    longitude_list = [loc[1] for loc in location_result]
    return (sum(latitude_list) / len(latitude_list), sum(longitude_list) / len(longitude_list))


df['coordinates'] = df['location'].apply(geoencode)

print("Missing coordinates: ", df.coordinates.isna().sum())

df.to_csv("kecelakaan-with-location-geoencoded.csv", index=False)

