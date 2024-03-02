import json
import requests

cities = ['An Giang', 'Bà Rịa – Vũng Tàu', 'Bạc Liêu', 'Bắc Giang', 'Bắc Kạn', 'Bắc Ninh', 
          'Bến Tre', 'Bình Dương', 'Bình Định', 'Bình Phước', 'Bình Thuận', 'Cà Mau', 'Cao Bằng', 
          'Cần Thơ', 'Đà Nẵng', 'Đắk Lắk', 'Đắk Nông', 'Điện Biên', 'Đồng Nai', 'Đồng Tháp', 'Gia Lai', 
          'Hà Giang', 'Hà Nam', 'Hà Nội', 'Hà Tĩnh', 'Hải Dương', 'Hải Phòng', 'Hậu Giang', 'Hòa Bình', 
          'Hồ Chí Minh', 'Hưng Yên', 'Khánh Hòa', 'Kiên Giang', 'Kon Tum', 'Lai Châu', 
          'Lạng Sơn', 'Lào Cai', 'Lâm Đồng', 'Long An', 'Nam Định', 'Nghệ An', 'Ninh Bình', 'Ninh Thuận', 
          'Phú Thọ', 'Phú Yên', 'Quảng Bình', 'Quảng Nam', 'Quảng Ngãi', 'Quảng Ninh', 'Quảng Trị', 
          'Sóc Trăng', 'Sơn La', 'Tây Ninh', 'Thái Bình', 'Thái Nguyên', 'Thanh Hóa', 'Thừa Thiên Huế', 
          'Tiền Giang', 'Trà Vinh', 'Tuyên Quang', 'Vĩnh Long', 'Vĩnh Phúc', 'Yên Bái']

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


