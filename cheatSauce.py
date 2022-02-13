#Version 2.2

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import hashlib

def get_file_content_chrome(driver, uri):
  result = driver.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
  if type(result) == int :
    raise Exception("Request failed with status %s" % result)
  else:
      return result
  
    
def openFile():
    with open("cheatSauce.json", "r") as file:
        return json.load(file)

def saveFile(dictionnaire):
    with open("cheatSauce.json", "w") as file:
        json.dump(dictionnaire, file)
        
def writeSolution(solution, driver):
    joinGame = driver.find_element_by_class_name("join")
    if joinGame.get_attribute("hidden") == None:
        joinGame.click()
    
    time.sleep(3)
    inputSolution = driver.find_element_by_class_name("guessing").find_element_by_xpath("input")
    inputSolution.send_keys(solution)
    time.sleep(1)
    inputSolution.send_keys("\n")
    
    
    

link = "https://jklm.fun/WCAZ"
nomUser = "Jean Lassalle"


browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get(link)
time.sleep(2)
myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'nickname')))
item = browser.find_element_by_class_name('nickname')
item.clear()
item.send_keys(nomUser)
ok_button = item.find_element_by_xpath('../button')
ok_button.click()
print(">> Clic sur ok")
time.sleep(8)
browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
item = browser.find_element_by_class_name("joinRound")
item.click()
print(">> Clic sur rejoindre")

#jeu


dictionnaire = openFile()

imageLink = browser.find_element_by_class_name("actual").get_attribute("style")
texte = browser.find_element_by_class_name("text").get_attribute("innerHTML")
while(True):
    time.sleep(1)
    imageBalise = browser.find_element_by_class_name("actual")
    texteBalise = browser.find_element_by_class_name("text")
    
    if imageLink != imageBalise.get_attribute("style") or texte != texteBalise.get_attribute("innerHTML"):
        if imageLink != imageBalise.get_attribute("style"):
            imageLink = imageBalise.get_attribute("style")
            result = get_file_content_chrome(browser, imageLink.split("\"")[1])
            print("Image detectee")
        elif texte != texteBalise.get_attribute("innerHTML"):
            texte = texteBalise.get_attribute("innerHTML")
            result = texte
            print("Texte detecte")
        else:
            print("!!! ERROR, changement est ni image, ni texte !!!")
            break
        hashResult = hashlib.sha256(result.encode('utf-8')).hexdigest()
        
        if hashResult in dictionnaire:
            print("!!!!! TROUVE !!!!! " + dictionnaire[hashResult])
            writeSolution(dictionnaire[hashResult], browser)

        value = browser.find_element_by_class_name("value").get_attribute("innerHTML")
        while value == browser.find_element_by_class_name("value").get_attribute("innerHTML"): #Attendre que la reponse s'affiche
            continue
        value = browser.find_element_by_class_name("value").get_attribute("innerHTML")
        
        #prendre la bonne réponse écrie par un autre de taille minimum
        listeUsers = browser.find_elements_by_class_name("hasFoundSource")
        if len(listeUsers) > 0 and listeUsers != None:
            for user in listeUsers:
                try:
                    guessBalise = user.find_element_by_class_name("guess")
                
                    if guessBalise != None:
                        guess = guessBalise.get_attribute("innerHTML")
                        if len(guess) < len(value) and len(guess)>0:
                            value = guess
                except Exception:
                    print("l'erreur de merde incompréhensible")
                
        
        if not hashResult in dictionnaire:
            print("added " + value + " : " + hashResult)
        else:
            print("in db: " + value)
        dictionnaire[hashResult] = value
        saveFile(dictionnaire)

        
        
            