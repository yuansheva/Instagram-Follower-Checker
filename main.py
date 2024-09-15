import json

# Baca data followers
with open('./data/followers_1.json', 'r') as f:
    followers_data = json.load(f)

followers = []
for item in followers_data:
    for data in item["string_list_data"]:
        followers.append(data["value"])

# Baca data following
with open('./data/following.json', 'r') as f:
    following_data = json.load(f)

following = []
for item in following_data["relationships_following"]:
    for data in item["string_list_data"]:
        following.append(data["value"])

# Temukan akun yang Anda ikuti tapi tidak mengikuti Anda kembali
not_following_back = set(following) - set(followers)

# Cetak hasilnya
print("Akun yang Anda ikuti tapi tidak mengikuti Anda kembali:")
for username in not_following_back:
    print(f"https://www.instagram.com/{username}")

# Hitung statistik
print(f"\nTotal followers: {len(followers)}")
print(f"Total following: {len(following)}")
print(f"Jumlah akun yang tidak mengikuti Anda kembali: {len(not_following_back)}")