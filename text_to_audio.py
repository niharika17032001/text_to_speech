import os
import re
import json
import base64
import requests
from time import sleep
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from moviepy.editor import AudioFileClip
import pandas as pd

from google_chromeSetup import setup_google_chrome_driver

# ------------------------------------------
# Utility Functions
# ------------------------------------------

def wait_time(seconds):
    for _ in tqdm(range(seconds), desc=f"Waiting {seconds} sec"):
        sleep(1)

def select_voice(select_element, target_voice="Neerja English (India)"):
    select = Select(select_element)
    for option in select.options:
        if option.text.strip() == target_voice:
            print(f"Selecting voice: {target_voice}")
            option.click()
            return
    raise ValueError(f"Voice '{target_voice}' not found.")

def download_audio(audio_url, audio_location, retries=3):
    print("Downloading:", audio_url[15])
    os.makedirs(os.path.dirname(audio_location), exist_ok=True)

    for attempt in range(retries):
        try:
            if audio_url.startswith("http"):
                with requests.get(audio_url, stream=True, timeout=15) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get('content-length', 0))
                    with open(audio_location, "wb") as f, tqdm(
                        total=total_size, unit='iB', unit_scale=True, desc="Downloading"
                    ) as progress_bar:
                        for chunk in response.iter_content(1024):
                            if chunk:
                                f.write(chunk)
                                progress_bar.update(len(chunk))
            elif audio_url.startswith("data:audio"):
                header, encoded = audio_url.split(",", 1)
                with open(audio_location, "wb") as f:
                    f.write(base64.b64decode(encoded))
            else:
                raise ValueError("Unsupported audio URL format.")
            return  # Success
        except Exception as e:
            print(f"Download attempt {attempt + 1} failed: {e}")
            sleep(2)

    raise RuntimeError("Failed to download audio after retries.")

def process_audio(audio_location):
    try:
        audio_clip = AudioFileClip(audio_location)
        duration = audio_clip.duration
        print(f"Audio duration: {duration:.2f} seconds")
    except Exception as e:
        print(f"Error processing audio: {e}")

def close_popup_if_exists(driver):
    try:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".close, .popup-close, .ad-close, .overlay-close"))
        ).click()
        print("Popup closed.")
        wait_time(1)
    except Exception:
        print("No popup detected.")

def login_to_new_site(driver, url, text, audio_location, voice="Neerja English (India)"):
    try:
        driver.get(url)
        wait_time(2)

        text_area = driver.find_element(By.CSS_SELECTOR, "#promptText")
        text_area.send_keys(text)
        wait_time(2)

        select_element = driver.find_element(By.ID, "voices")
        select_voice(select_element, target_voice=voice)

        close_popup_if_exists(driver)

        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#action_submit"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        wait_time(1)

        try:
            print("Clicking submit...")
            submit_button.click()
        except Exception as e:
            print(f"Standard click failed: {e}, using JS click...")
            driver.execute_script("arguments[0].click();", submit_button)

        download_link = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#generatedVoice > a"))
        )

        audio_url = download_link.get_attribute("href")
        download_audio(audio_url, audio_location)
        process_audio(audio_location)

        wait_time(2)

    except Exception as e:
        print(f"[ERROR]: {e}")

def text_to_audio(driver, text, audio_location,voice):
    url = "https://crikk.com/text-to-speech/"
    login_to_new_site(driver, url=url, text=text, audio_location=audio_location,voice=voice)

def split_text(text, max_length=1200):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def text_to_audio_in_chunks(full_text, base_path="voices", voice="Neerja English (India)"):
    os.makedirs(base_path, exist_ok=True)
    chunks = split_text(full_text)
    driver = setup_google_chrome_driver()  # Start once
    for i, chunk in enumerate(chunks):
        filename = os.path.join(base_path, f"audio_chunk_{i + 1}.wav")
        print(f"\nProcessing chunk {i + 1}/{len(chunks)}...")
        text_to_audio(driver, chunk, filename,voice=voice)
        wait_time(2)
    driver.quit()

# ------------------------------------------
# Main Execution
# ------------------------------------------

def main():
    hinglish_story = '''
    Ek choti si gaav mein rehti thi ek ladki jiska naam Gudiya tha. Uski aankhon mein bade sapne the. Har din vo school jaate bachchon ko dekhti aur sochti, "Kaash main bhi school jaa pati."

    Uske papa Ramlaal kheton mein mazdoori karte the, aur maa gharon mein kaam karti thi. Paise ki kami ke kaaran Gudiya kabhi school nahi gayi.

    Par Gudiya ko padhne ka bahut shauk tha. Vo school ke bahar khadi ho kar chupke se class sunti. Ek din Masterji ne use dekh liya. Unhone kaha, “Beta, tumhare jaise hoshiyaar bachchey kam hote hain. Tumhara admission main karaunga.”

    Pehle to Ramlaal ne mana kiya, lekin baad mein maan gaye. Aur is tarah Gudiya ki zindagi badal gayi. Vo har roz school jaane lagi, naye doston ke saath padhne lagi. Dheere dheere usne class mein top karna shuru kiya.

    Ek din usne socha, "Main teacher banungi, taaki aur ladkiyon ko bhi padha saku jo school nahi jaa sakti."

    Aur phir usne yeh sapna poora bhi kiya. Aaj Gudiya ek school mein principal hai. Uska gaav us par garv karta hai.
    
    
    Ek choti si gaav mein rehti thi ek ladki jiska naam Gudiya tha. Uski aankhon mein bade sapne the. Har din vo school jaate bachchon ko dekhti aur sochti, "Kaash main bhi school jaa pati."

    Uske papa Ramlaal kheton mein mazdoori karte the, aur maa gharon mein kaam karti thi. Paise ki kami ke kaaran Gudiya kabhi school nahi gayi.

    Par Gudiya ko padhne ka bahut shauk tha. Vo school ke bahar khadi ho kar chupke se class sunti. Ek din Masterji ne use dekh liya. Unhone kaha, “Beta, tumhare jaise hoshiyaar bachchey kam hote hain. Tumhara admission main karaunga.”

    Pehle to Ramlaal ne mana kiya, lekin baad mein maan gaye. Aur is tarah Gudiya ki zindagi badal gayi. Vo har roz school jaane lagi, naye doston ke saath padhne lagi. Dheere dheere usne class mein top karna shuru kiya.

    Ek din usne socha, "Main teacher banungi, taaki aur ladkiyon ko bhi padha saku jo school nahi jaa sakti."

    Aur phir usne yeh sapna poora bhi kiya. Aaj Gudiya ek school mein principal hai. Uska gaav us par garv karta hai.
    
    
    Ek choti si gaav mein rehti thi ek ladki jiska naam Gudiya tha. Uski aankhon mein bade sapne the. Har din vo school jaate bachchon ko dekhti aur sochti, "Kaash main bhi school jaa pati."

    Uske papa Ramlaal kheton mein mazdoori karte the, aur maa gharon mein kaam karti thi. Paise ki kami ke kaaran Gudiya kabhi school nahi gayi.

    Par Gudiya ko padhne ka bahut shauk tha. Vo school ke bahar khadi ho kar chupke se class sunti. Ek din Masterji ne use dekh liya. Unhone kaha, “Beta, tumhare jaise hoshiyaar bachchey kam hote hain. Tumhara admission main karaunga.”

    Pehle to Ramlaal ne mana kiya, lekin baad mein maan gaye. Aur is tarah Gudiya ki zindagi badal gayi. Vo har roz school jaane lagi, naye doston ke saath padhne lagi. Dheere dheere usne class mein top karna shuru kiya.

    Ek din usne socha, "Main teacher banungi, taaki aur ladkiyon ko bhi padha saku jo school nahi jaa sakti."

    Aur phir usne yeh sapna poora bhi kiya. Aaj Gudiya ek school mein principal hai. Uska gaav us par garv karta hai.
    
    
    Ek choti si gaav mein rehti thi ek ladki jiska naam Gudiya tha. Uski aankhon mein bade sapne the. Har din vo school jaate bachchon ko dekhti aur sochti, "Kaash main bhi school jaa pati."

    Uske papa Ramlaal kheton mein mazdoori karte the, aur maa gharon mein kaam karti thi. Paise ki kami ke kaaran Gudiya kabhi school nahi gayi.

    Par Gudiya ko padhne ka bahut shauk tha. Vo school ke bahar khadi ho kar chupke se class sunti. Ek din Masterji ne use dekh liya. Unhone kaha, “Beta, tumhare jaise hoshiyaar bachchey kam hote hain. Tumhara admission main karaunga.”

    Pehle to Ramlaal ne mana kiya, lekin baad mein maan gaye. Aur is tarah Gudiya ki zindagi badal gayi. Vo har roz school jaane lagi, naye doston ke saath padhne lagi. Dheere dheere usne class mein top karna shuru kiya.

    Ek din usne socha, "Main teacher banungi, taaki aur ladkiyon ko bhi padha saku jo school nahi jaa sakti."

    Aur phir usne yeh sapna poora bhi kiya. Aaj Gudiya ek school mein principal hai. Uska gaav us par garv karta hai.
    
    
    Ek choti si gaav mein rehti thi ek ladki jiska naam Gudiya tha. Uski aankhon mein bade sapne the. Har din vo school jaate bachchon ko dekhti aur sochti, "Kaash main bhi school jaa pati."

    Uske papa Ramlaal kheton mein mazdoori karte the, aur maa gharon mein kaam karti thi. Paise ki kami ke kaaran Gudiya kabhi school nahi gayi.

    Par Gudiya ko padhne ka bahut shauk tha. Vo school ke bahar khadi ho kar chupke se class sunti. Ek din Masterji ne use dekh liya. Unhone kaha, “Beta, tumhare jaise hoshiyaar bachchey kam hote hain. Tumhara admission main karaunga.”

    Pehle to Ramlaal ne mana kiya, lekin baad mein maan gaye. Aur is tarah Gudiya ki zindagi badal gayi. Vo har roz school jaane lagi, naye doston ke saath padhne lagi. Dheere dheere usne class mein top karna shuru kiya.

    Ek din usne socha, "Main teacher banungi, taaki aur ladkiyon ko bhi padha saku jo school nahi jaa sakti."

    Aur phir usne yeh sapna poora bhi kiya. Aaj Gudiya ek school mein principal hai. Uska gaav us par garv karta hai.
    '''
    text_to_audio_in_chunks(hinglish_story)

if __name__ == "__main__":
    main()
