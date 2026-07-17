import requests
import re
from bs4 import BeautifulSoup

def test_mal_direct():
    title = "Nisekoi"
    url = f"https://myanimelist.net/anime.php?q={title}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    print("Searching MAL for:", title)
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Search failed:", r.status_code)
        return
        
    soup = BeautifulSoup(r.text, "html.parser")
    # Find the first anime link in the search table
    # The search page usually has a table with class "list" or search results links
    anime_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        # Match https://myanimelist.net/anime/ID/Title
        match = re.search(r"https://myanimelist.net/anime/(\d+)/", href)
        if match:
            anime_links.append((match.group(1), href))
            
    print("Found anime links:")
    for mal_id, href in anime_links[:5]:
        print(f" - ID: {mal_id}, Link: {href}")
        
    if not anime_links:
        print("No anime links found.")
        return
        
    # Test characters list direct fetching
    # URL: https://myanimelist.net/anime/ID/Title/characters
    # Or just: https://myanimelist.net/anime/ID/characters
    mal_id = anime_links[0][0]
    char_url = f"https://myanimelist.net/anime/{mal_id}/characters"
    print(f"\nFetching characters from: {char_url}")
    cr = requests.get(char_url, headers=headers)
    if cr.status_code != 200:
        # Fallback to general page if characters page doesn't exist
        print("Characters page failed:", cr.status_code)
        return
        
    csoup = BeautifulSoup(cr.text, "html.parser")
    # Characters are usually in a table structure or divs
    # Let's find character names and roles
    # Normally, character name links look like: https://myanimelist.net/character/ID/Name
    # And their role is next to it in a small text (Main or Supporting)
    chars = []
    for char_link in csoup.find_all("a", href=True):
        chref = char_link["href"]
        match = re.search(r"https://myanimelist.net/character/(\d+)/", chref)
        if match:
            char_id = match.group(1)
            char_name = char_link.text.strip()
            if char_name:
                # Find role: in MAL, the role is typically in a td or tag near the link
                # For simplicity, let's see if we can find the parent text or adjacent cell
                parent = char_link.find_parent("td")
                role = "Supporting"
                if parent:
                    # Look for "Main" or "Supporting" in sibling elements
                    parent_text = parent.get_text()
                    if "Main" in parent_text:
                        role = "Main"
                    elif "Supporting" in parent_text:
                        role = "Supporting"
                chars.append((char_id, char_name, role, chref))
                
    # Remove duplicates
    seen = set()
    unique_chars = []
    for cid, name, role, href in chars:
        if name not in seen:
            seen.add(name)
            unique_chars.append((cid, name, role, href))
            
    print(f"Found {len(unique_chars)} characters:")
    for cid, name, role, href in unique_chars[:10]:
        print(f" - ID: {cid}, Name: {name}, Role: {role}, URL: {href}")

if __name__ == "__main__":
    test_mal_direct()
