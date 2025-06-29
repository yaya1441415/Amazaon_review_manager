from flask import  Blueprint, request, jsonify
from bs4 import BeautifulSoup
import validators
from utils.helpers import get_stars, get_top_word, Sentiment, summarise
import requests


analyze_bp = Blueprint('analyze', __name__)  #Blueprint for analyze routes

@analyze_bp.route("/analyze", methods=['POST'])
def analyze():
    #get the data sent from the front-end
    data = request.get_json()
    #access the url key
    url = data.get('url')

    #header 
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
              'Accept-Language': 'en-US, en;q=0.5',}
    

    if not url:
        return jsonify({'error':'No URL provided'}), 400
    
    if not validators.url(url):
        return jsonify({'error':'Invalid URL'}), 400
    
   
    response = requests.get(url,headers=header)

    soup= BeautifulSoup(response.text, 'html.parser')
    soup1 = BeautifulSoup(soup.prettify(), "html.parser")
    
    average_stars = get_stars(soup1)
    
    top_words = get_top_word(soup1)


    
    sentiment = Sentiment(soup1)
    
    summary = summarise(soup1)

    
    
     
    return jsonify({
        'average_stars': average_stars,
        'top_words': top_words,
        'sentiment': sentiment, 
        'summary' : summary,
        'message': f'Analyzed reviews for: {url}'
    })


