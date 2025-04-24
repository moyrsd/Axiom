# from typing import List
# import requests
# from bs4 import BeautifulSoup
# import time
# import random
# from urllib.parse import urlparse

# def crawl_links(links: List[str]=None):
#     if links is None:
#         links = []
    
#     extracted_content = []
#     for link in links:
#         text = crawl_one_link(link)
#         if text:  
#             extracted_content.append({
#             "page_content": text,
#             "meta_data": {
#                 "source": link
#             }})
#         # Add a small delay between requests
#         time.sleep(random.uniform(1, 3))
#     return extracted_content        

# def crawl_one_link(link: str):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
#     }
    
#     try:
#         response = requests.get(link, headers=headers, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')
#         for element in soup.find_all(['nav', 'footer', 'header', 'aside', 'script', 'style']):
#             element.decompose()
            
#         content = None
#         for selector in ['main', 'article', '.content', '#content', '.post', '.article']:
#             content = soup.select_one(selector)
#             if content:
#                 break
        
#         if not content:
#             content = soup.body
            
#         if content:
#             return ' '.join(content.get_text(separator=' ', strip=True).split())
#         return None
#     except Exception as e:
#         print(f"Error parsing link: {link} - {e}")
#         return None
    

# def extract_urls(text):
#         urls = []
#         for word in text.split():
#             parsed = urlparse(word)
#             if parsed.scheme and parsed.netloc:
#                 urls.append(word)
#         return urls    
    
# # https://beautiful-soup-4.readthedocs.io/en/latest/