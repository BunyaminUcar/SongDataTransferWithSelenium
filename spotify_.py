from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

def start_driver():
    driver = webdriver.Chrome("C:\chromewebdriver\chromedriver.exe")
    driver.maximize_window()
    return driver

def login(driver, username, password):
    driver.get("https://open.spotify.com")
    driver.implicitly_wait(10)
    log = driver.find_element(By.XPATH,"//*[@id='main']/div/div[2]/div[1]/header/div[5]/button[2]")
    log.click()
    username_input = driver.find_element(By.XPATH,"//*[@id='login-username']")
    username_input.send_keys(username)
    password_input = driver.find_element(By.XPATH,"//*[@id='login-password']")
    password_input.send_keys(password)
    login_button = driver.find_element(By.XPATH,"//*[@id='login-button']/span[1]")
    login_button.click()
    time.sleep(5)

def tracks_save(driver):
    driver.get("https://open.spotify.com/collection/tracks")
    time.sleep(5)
    
    if driver.title == "Spotify – Beğenilen Şarkılar":
        driver.implicitly_wait(10)

    # Sözlük oluştur
        songs = {}
    
    # Tüm şarkıları yükle
        while True:
        # Şarkıları, sıraları ve sanatçıları bul
            song_elems = driver.find_elements(By.XPATH, "//div[@class='Type__TypeElement-sc-goli3j-0 kHHFyx t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line']")
            rank_elems = driver.find_elements(By.XPATH, "//span[@class='Type__TypeElement-sc-goli3j-0 eRYMpa VrRwdIZO0sRX1lsWxJBe']")
            artist_elems = driver.find_elements(By.XPATH, "//span[@class='Type__TypeElement-sc-goli3j-0 dvSMET rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line']/a[1]")
        
        # Şarkı adı, sıra numarası ve sanatçı adı bilgilerini sözlüğe ekle
            for song, rank, art in zip(song_elems, rank_elems,artist_elems):
                song_name = song.text
                artist_name = art.text
                rank_num = rank.text
                songs[song_name] = {'artist': artist_name, 'rank': rank_num}
            
            with open('songs.txt', 'w', encoding='utf-8') as f:
                for song in songs:
                    song_info = songs[song]
                    song_name = song
                    artist_name = song_info['artist']
                    rank_num = song_info['rank']
                    f.write(f'{song_name} {artist_name}\n')
        
        # Son sıra numarasını kontrol et
            last_rank = rank_elems[-1].text
            
            if last_rank == "301":
                print("Tüm şarkılar yüklendi.")
                break

        # Sayfayı kaydırarak daha fazla şarkı yükle
            driver.execute_script("arguments[0].scrollIntoView();", rank_elems[-1])
            time.sleep(1)


    # WebDriver'ı kapat
        driver.quit()

    else:
        print("Test başarısız")
        driver.quit()



if __name__ == '__main__':
    driver = start_driver()
    login(driver, "", "")
    tracks_save(driver)
    driver.quit()
