from flask import  Blueprint, request, jsonify
from bs4 import BeautifulSoup
import validators
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.helpers import get_stars, get_top_word, Sentiment, summarise
from selenium.webdriver.chrome.service import Service
import time
import undetected_chromedriver as uc
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager


analyze_bp = Blueprint('analyze', __name__)  #Blueprint for analyze routes

@analyze_bp.route("/analyze", methods=['POST'])
def analyze():

    #get the data sent from the front-end
    data = request.get_json()
    url = data.get('url') #access the url key

    if not url:
        return jsonify({'error':'No URL provided'}), 400
    
    if not validators.url(url):
        return jsonify({'error':'Invalid URL'}), 400
    
    #configure Chrome webdriver.
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")#hides that selenuim is controlling the browser
    options.add_argument("--disable-dev-shm-usage")#avoids memory issues
    options.add_argument("--disable-infobars")#removes chrome is being controlled notification
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")#opens chrome without rendering the GUI



    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    ) #initialize the webdriver

    # to make the bot look like a real human browser
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )


    try:
        
        #Scrape the page.
        driver.get(url)
        time.sleep(5)
        
        html = driver.page_source

        #parse  Html
        soup= BeautifulSoup(html, 'html.parser')
        soup1 = BeautifulSoup(soup.prettify(), "html.parser")
        
        #Extract review data
        average_stars = get_stars(soup1)
        top_words = get_top_word(soup1)       
        sentiment = Sentiment(soup1)    
        summary = summarise(soup1)

    finally:
        driver.quit()

    return jsonify({
        'average_stars': average_stars,
        'top_words': top_words,
        'sentiment': sentiment, 
        'summary' : summary,
        'message': f'Analyzed reviews for: {url}'
    })


