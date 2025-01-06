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

def extract_signature(html_content):
    signature_pattern = r'"signature":"([^"]*)"'
    signature_match = re.search(signature_pattern, html_content)
    
    if signature_match:
        return signature_match.group(1)
    return None

def main():
    while True:
        try:
            username = input("\nEntrez un nom d'utilisateur TikTok (ou 'q' pour quitter): ")
            
            if username.lower() == 'q':
                print("Programme terminé")
                break
                
            response = make_request(username)
            
            if response.status_code == 200:
                stats = extract_stats(response.text)
                signature = extract_signature(response.text)
                
                print("\nRésultats:")
                if stats:
                    print(f"Followers: {stats.get('followerCount', 'N/A')}")
                    print(f"Following: {stats.get('followingCount', 'N/A')}")
                    print(f"Likes: {stats.get('heartCount', 'N/A')}")
                    print(f"Videos: {stats.get('videoCount', 'N/A')}")
                
                if signature:
                    print(f"Signature: {signature}")
                    
                if not stats and not signature:
                    print("Aucune donnée trouvée pour cet utilisateur")
                    
            else:
                print(f"Erreur lors de la requête. Code: {response.status_code}")
                
        except Exception as e:
            print(f"Une erreur s'est produite: {str(e)}")
            
        time.sleep(1)

if __name__ == "__main__":
   main()