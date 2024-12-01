# import necessary libraries
import requests
import json
import gtts
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# url to send the GET request to
url = "https://webhook-test.com/api/webhooks/1fe62779acb39e5bcd97c9eadacf992e"

# bearer token (replace with your actual token)
bearer_token = os.getenv("BEARER_TOKEN")

#bearer headers
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

amogus = []

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        #print each payload in the payloads list but only the first 15 so that we can get recent
        for i, payload in enumerate(data.get("payloads", [])[:15], start=1):  # limit to the first 15 payloads
            payload_data = payload.get("payload", "")
            if payload_data:
                try:
                    # parse the json string
                    payload_json = json.loads(payload_data)
                    
                    # check if segment is in the payload
                    if 'segments' in payload_json:
                        for segment in payload_json['segments']:
                            print(segment.get("text"))
                            amogus.append(str(segment.get("text")))

                except json.JSONDecodeError as e:
                    print(f"Error parsing payload {i}: {e}")
            else:
                print(f"Payload {i} is empty.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print("Response:", response.text)  # Print the response text for more details
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

output_folder = 'ragcategories'

# list of champion names
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

def get_champion_from_question(question):
    # use regex to extract champion name from the question
    for champion in champions:
        if re.search(rf'\b{re.escape(champion)}\b', question, re.IGNORECASE):
            return champion
    return None

def read_champion_file(champion):
    file_path = os.path.join(output_folder, f"{champion.replace(' ', '_')}.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return None

def get_answer_from_text(text, question):
    # use Gemini API to generate an answer based on the text and question
    prompt = f"Given the following text about {question}:\n\n{text}\n\nAnswer the question: {question}"
    response = model.generate_content(prompt)
    return response.text

def main():
    global  answer

    while True:
        question = " ".join(amogus)
        if question.lower() == 'exit':
            break
        
        champion = get_champion_from_question(question)
        if champion:
            text = read_champion_file(champion)
            if text:
                answer = get_answer_from_text(text, question)
                print(f"Answer: {answer}")
            else:
                print(f"Could not find information for {champion}.")
        else:
            print("Could not identify a champion in your question. Please try again.")
# Text to Speech output which can be hosted on a website in the future
output = gtts(text=answer, lang = 'en', slow = False)
output.save("output.mp3")
os.system(" start output.mp3")


if __name__ == "__main__":
    
    main()