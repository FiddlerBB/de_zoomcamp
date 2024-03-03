import json
import requests

cities = ['An Giang', 'Ba Ria - Vung Tau', 'Bac Lieu', 'Bac Giang', 'Bac Kan', 'Bac Ninh', 
          'Ben Tre', 'Binh Duong', 'Binh Dinh', 'Binh Phuoc', 'Binh Thuan', 'Ca Mau', 'Cao Bang', 
          'Can Tho', 'Da Nang', 'Dak Lak', 'Dak Nong', 'Dien Bien', 'Dong Nai', 'Dong Thap', 'Gia Lai', 
          'Ha Giang', 'Ha Nam', 'Ha Noi', 'Ha Tinh', 'Hai Duong', 'Hai Phong', 'Hau Giang', 'Hoa Binh', 
          'Ho Chi Minh', 'Hung Yen', 'Khanh Hoa', 'Kien Giang', 'Kon Tum', 'Lai Chau', 
          'Lang Son', 'Lao Cai', 'Lam Dong', 'Long An', 'Nam Dinh', 'Nghe An', 'Ninh Binh', 'Ninh Thuan', 
          'Phu Tho', 'Phu Yen', 'Quang Binh', 'Quang Nam', 'Quang Ngai', 'Quang Ninh', 'Quang Tri', 
          'Soc Trang', 'Son La', 'Tay Ninh', 'Thai Binh', 'Thai Nguyen', 'Thanh Hoa', 'Thua Thien Hue', 
          'Tien Giang', 'Tra Vinh', 'Tuyen Quang', 'Vinh Long', 'Vinh Phuc', 'Yen Bai']


# empty lists for storing coordinates
locations = []

# loop over cities to get their coordinates
for id, city in enumerate(cities):
    print(f"getting data for {city}")
    url = f"https://nominatim.openstreetmap.org/search?q={city},+Vietnam&format=json"
    response = requests.get(url).json()
    location = {
        "City_index": id,
        "Latitude": response[0]["lat"],
        "Longitude": response[0]["lon"],
        "City": city,
    }
    print(location)
    locations.append(location)

# write locations to a json file
with open("vietnam_locations.json", "w", encoding='utf8') as f:
    json.dump(locations, f, ensure_ascii=False)


