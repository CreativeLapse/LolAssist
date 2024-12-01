import requests
from bs4 import BeautifulSoup
import os
import time

# list of champion names we got from a list
champions = [
    "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe", "Aurelion Sol", "Azir",
    "Bard", "Bel'Veth", "Blitzcrank", "Brand", "Braum", "Caitlyn", "Camille", "Cassiopeia", "Cho'Gath", "Corki", "Darius",
    "Diana", "Dr. Mundo", "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio",
    "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Illaoi", "Irelia", "Ivern",
    "Janna", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "Kai'Sa", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina",
    "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "K'Sante", "LeBlanc", "Lee Sin", "Leona", "Lillia",
    "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi", "Milio", "Miss Fortune", "Mordekaiser",
    "Morgana", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu & Willump", "Olaf", "Orianna", "Ornn",
    "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn", "Rakan", "Rammus", "Rek'Sai", "Rell", "Renata Glasc", "Renekton", "Rengar",
    "Riven", "Rumble", "Ryze", "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion",
    "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "Tahm Kench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh",
    "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vex",
    "Vi", "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo", "Yone", "Yorick",
    "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"
]

# URL of the League Wiki wiki
base_url = "https://wiki.leagueoflegends.com/en-us"

output_folder = 'ragcategories'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_champion_page(url):
    html = get_page_content(url)
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', {'class': 'mw-parser-output'})
    if content is None:
        return None
    text = content.get_text(separator='\n', strip=True)
    return text

def main():
    for i, champion in enumerate(champions, start=1):
        champion_url = f"{base_url}/{champion.replace(' ', '_')}"
        print(f"Scraping page {i}/{len(champions)}: {champion_url}")
        page_text = scrape_champion_page(champion_url)
        if page_text:
            # create a file for each champion and save the content
            file_path = os.path.join(output_folder, f"{champion.replace(' ', '_')}.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(page_text)
            print(f"Saved page {i}/{len(champions)}: {champion}")
        else:
            print(f"Failed to scrape page {i}/{len(champions)}: {champion_url}")
        
        time.sleep(2)  # add a delay to allow server to scrape and breathe
    
    print("scraping complete. data saved in the 'ragcategories' folder!!!")

if __name__ == "__main__":
    main()
