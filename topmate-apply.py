import pandas as pd
import requests
import json
import time

# 1. Load your data
# Ensure the CSV file is in the same directory as this script
df = pd.read_csv('e0eed836-b03c-49f6-9de2-7fc9f8c88344.csv')

# 2. Define the API endpoint
url = 'https://api.galactus.run/create-booking/'

# 3. Exact Headers mimicking your browser completely
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'content-type': 'application/json',
    'origin': 'https://topmate.io',
    'priority': 'u=1, i',
    'referer': 'https://topmate.io/',
    'sec-ch-ua': '"Brave";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'x-captcha-token': '0cAFcWeA5E3FKDe5l7ebczrqrfhBNMPUbSDddvNWZOwf2v6DXwcTJHgVghC7bCK1AQUoPSZRLEe8grpd9nP9e4C00itJOzVGJL6dVeTz2mPaPcFfLCW6RBNqFq-fudboF7UIH9uAqxkVvW2JkZtDmly9_lP7QecFo5CrZSKz26YKOF4y-ZueogRKvwuZvy6QDGbbk5V-4hZK4HNd87UuVTPexQonVOY4M2KInXYpPyNpq-8ardIgDIXU6jgO5_mXxkdJ6xmyaXFHj5niCLE5QdqpbdPhWmdSj3klfroek984C6D7JD9iGJ6CtaKKoKPJp8nbUXXiH1RZo96gQ6ug5PdN2tkVjsNFo5p5NjkSr2LXtMW5xxB90h9-RrPg-YaHzOptziue6V7qDyrC6yRWhBIWD93tf2om80U6Y9wB-HJplTPHACDswCJbKnxgoNv7MdK97pZQfB_Ev_NcdQMQ_KBMkLPhXgIeWnPza7zGcCJs8WjxmA57p38K34Heors5eoFCbJ-0ySTJkKuYVgQeNKVp4ai_5WJxkLy8i12GohmXQSfetDouyhD4QWWTHAEHHH3CzHBLWdkkROcDK4jLsmQlKFzmM-g7IkrfR-MPppgcEXagLEFlS7N6ZBt33sq9brayXAZStimMDgAsjnv289K3sRhRPESC7J1a-hPCUJVH4lEQhHPkz050SfYp-DXcPvYLSighVAgJYF7F1LnYZrL3XVW0t-1u-84lyHNyHjKzbISF5J_FixewAKSlM9-QsPvzkW9b9MpZcSZHb0PAcSJQ1X7oeiVQ3KDxo3IEOYFPLFflhFbP10pb60nu8vJ6qkUOrEZKeqe8viozFBchRBqmsZMeJ72bB3cOMk_2tfrtwVNfcPHdW-J4lj6MNC41gspS2bgCoT4mV7AMbomLyqotfcJrB88UQEQ0jRPfZck2_A92PDDNXi8HYVDrLDH8vd3tKay1JZ280DD_8n1Fe3-spPu7SS4J_PQFflVJ3MFI2GY8njFXplJ_bRDKdu7Dl4TDFcfVKkc0b2Ga8kobNPwT8fkV8nWrMsHhrB388J09oB0Kbwc0A-pFOC3M73JLW5J-Wd47BpsoykWIKvpuKMzXIcUbND7HxgO9DwE9wyGih49wYHUsXIPzHRFi1EkDQmdbrvA4VRbqaqO-jdi5_j804sB50_UOegu5UX6vuiGQHnsdqkaFACYEh4VIrp1HAWHHYeT2zLwf0RYlTwcZts9bjepLLl4iFRg7HeOIHnVuA0uXADfUd9LAeBH7EWpHmjNAa4mGLrKcWKtReP3VMVwk5rNg0kpZbdjlAGHzukbHXsRGlad9eEWlirSY6dpnBmbJ7mdHVXVZApXYic30DOnBE4SNDxfzJqYH0nvSmIxN-_XB1l_06wJx8Rnp_pJ1_T5LEFkf3X8wUyyl3XYO-ZoQ0Ba07AQvs-_9gFu171RxXlC9o_XpnsrSKHeTof1w-b5G6iZFnY1-VVCiQ6DvvdtYcmbdgyuf8h2TlDDQgkVsqUsvMCneLo3-gvWQKzlkSLII2fdDW_wac6luG9FbJKEmqa1Lc-D6829ctC55tmXkzHycOB-d03LrrRc5PS-gn6sGFJiD9ygFwT2MFBDt-13NwfJIzrP63IxY4_0-Vhz_ndPyyfxeybcmTBse4t5mL4Br1CtufaOLD0234KfV0gYMk9CFcSwTRdKz1u4xzZ_l6dwSmGU8jJSCXqVqkpPFl7WFE_4eFSgve3qWV09_ZeGUhn8ED5ozAWYrIjRH5FmiAO3yZ2DfkDcG-OzEU3-KTxp_0bomgyvkfAwNuNbWpP69uchIkZWnRURiSXc3ss1ppkTK-UBz98VcvhtqBTZsldfj4w7Cd2nwdJVC4FG07UMDEwXpeEgqYeqUCl25xsDM9_cRqXfpDe5XGPMl_4xmWNAGzZe7ONl0yRKuYOgq4KOAg34QPduSsZRozbGlTbSW4MkXDZtlVmGFUAraGJHkLAYq-JdCwbAfVeudN4R5ayzyzWlK5N7gzfle3Kro8BnJ1bEumAU_RJhl5Vi2BgGb4iXGd2-j2a6p7dXFBrabcJiCxyHgDvYJ8ou4s0Cyu--I6qdl05WALNvwRXyPpJ1nTgyTZWXV6kS6FS_0rALi6RdXoXNW1u-DKAeqiWrfj2waE00sPgFLgbBIWusGDtSZJ0chdyqZ7TgXmFt3RE24UpOajI0bjIuJkfhB1cLZw30Veht1fx1U41XbA05i8qOlVwRPYHAYDtFOL0QXBvc0FKOHOb-kSRUlDjjGoKt53Kl775PQEpKP_niQDYgiLJ5DFh65xqlYe-oa_ftx11EWRACKnTZz2XofOprg',
    'x-client-country': 'IN',
    'x-device-id': '47c9e278-1d71-4054-8603-7c15b7017c36',
    'x-oc-request-id': 'tkiJ40whQQTd6bcZTjxsxkQrVWtyUmEO', 
    'x-timezone': 'Asia/Kolkata',
    'x-user-agent': 'topmate',
    'x-utm-params': '{"utm_source":"","utm_page":"NA","utm_medium":"","utm_campaign":"","utm_user":"","http_referer":"https://topmate.io/dashboard/services/edit/basic-details?id=2173754&type=3","utm_content":"","utm_term":""}'
}

# 4. Iterate through leads and execute requests
for index, row in df.iterrows():
    # Constructing the exact payload formatting from your raw-data
    payload = {
        "service": 2173754,
        "consumer_email": row['email'],
        "consumer_name": row['name'],
        "consumer_phone": str(row['phone']),
        "consumer_timezone": "Asia/Kolkata", 
        "answers_json": [],
        "subscribe_to_whatsapp": True,
        "price": 0,
        "addons": [],
        "product_section": "Digital Product",
        "ai_search_booking": False
    }
    
    # Executing the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Error handling and output
    if response.status_code == 201:
        print(f"[{index + 1}/{len(df)}] Successfully booked for {row['name']}")
    else:
        print(f"[{index + 1}/{len(df)}] Failed to book for {row['name']}. Status: {response.status_code}, Response: {response.text}")
    
    # Adding a small 1-second delay between requests to avoid triggering rate limits
    time.sleep(1)