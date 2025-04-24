from typing import List


def crawl_links(links : List[str]=[]):
    extracted_content = []
    for link in links:
        text = crawl_one_link(link)
        extracted_content.append({
        "page_content": text,
        "meta_data": {
            "source": link
        }})
    return extracted_content        

def crawl_one_link(link:str):
    try : 
        print("d")
    except Exception as e:
        print(f"Error parsing link: {link} - {e}")
        return None    


