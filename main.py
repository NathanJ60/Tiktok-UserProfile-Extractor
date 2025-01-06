import cloudscraper
import json
import time
import re

def make_request(username):
   scraper = cloudscraper.create_scraper()
   
   headers = {
       'authority': 'www.tiktok.com',
       'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
       'accept-language': 'fr-FR,fr;q=0.9',
       'cache-control': 'no-cache',
       'pragma': 'no-cache', 
       'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
       'sec-ch-ua-mobile': '?1',
       'sec-ch-ua-platform': '"Android"',
       'sec-fetch-dest': 'document',
       'sec-fetch-mode': 'navigate',
       'sec-fetch-site': 'none', 
       'sec-fetch-user': '?1',
       'upgrade-insecure-requests': '1',
       'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'
   }

   url = f'https://www.tiktok.com/@{username}'
   response = scraper.get(url, headers=headers)
   response.encoding = 'utf-8'
   return response

def extract_stats(html_content):
   stats_pattern = r'"stats":\s*({[^}]+})'
   stats_match = re.search(stats_pattern, html_content)
   
   if stats_match:
       stats_json = stats_match.group(1)
       try:
           stats = json.loads(stats_json)
           return stats
       except json.JSONDecodeError:
           return None
   return None

def main():
   while True:
       try:
           username = input("\nEntrez un nom d'utilisateur TikTok (ou 'q' pour quitter): ")
           
           if username.lower() == 'q':
               print("Programme terminé")
               break
               
           response = make_request(username)
           print(f"\nStatus Code: {response.status_code}")
           
           stats = extract_stats(response.text)
           if stats:
               print(f"\nStats pour @{username}:")
               print(f"Followers: {stats['followerCount']:,}")
               print(f"Following: {stats['followingCount']:,}")
               print(f"Hearts: {stats['heart']:,}")
               print(f"Videos: {stats['videoCount']:,}")
               print(f"Friends: {stats['friendCount']:,}")
           else:
               print("Impossible d'extraire les stats pour cet utilisateur")
               
           time.sleep(0.5)
           
       except KeyboardInterrupt:
           print("\nProgramme arrêté par l'utilisateur")
           break
       except Exception as e:
           print(f"Erreur: {e}")
           time.sleep(0.5)

if __name__ == "__main__":
   main()