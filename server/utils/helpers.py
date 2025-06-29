import re
import nltk
import torch
from transformers import pipeline, AutoTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer



#loads HuggingFace’s pretrained summarization model,
#the pipeline automatically sets up the model and tokenizer for
#summarization
summarizer = pipeline(
    "summarization",  
    model="sshleifer/distilbart-cnn-12-6"
)
    
#loads the correct tokenizer based on the model specified.
#"sshleifer/distilbart-cnn-12-6" is a pretrained summarization model
#based on a distilled version of BART fine-tuned.
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")


def get_data(soup):
    all_reviews = []

    # Extract main container (assuming soup is already parsed HTML)
    div = soup.find('div', class_='a-row cm_cr_grid_center_container')

    # Extract Customer Names
    names = div.find_all('span', class_='a-profile-name')

    customer_names = [name.get_text(strip=True) for name in names]

    # Extract Star Ratings
    stars = div.find_all('span', class_='a-icon-alt')
    ratings = [star.get_text(strip=True) for star in stars]

    # Extract Review Titles (titles in the 'a' tag without a class)
    all_spans = div.find_all("a", class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")
    titles = []


    #Loops through each review block in all_spans
    for review in all_spans:
        #within each review block find the <span> element
        spans = review.find_all("span")
        #filters out spans that have a lass 
        for span in spans:
            if not span.has_attr("class"):
                titles.append(span.text.strip())

    #finds all elements that contain the review body using a very specific set of class
    divs = soup.find_all('div', class_='a-expander-content reviewText review-text-content a-expander-partial-collapse-content')
    descriptions = []
    #finds all span elements inside those divs.
    for div in divs:
        #then finds all span elements inside those divs.
        for span in div.find_all("span"):
            descriptions.append(span.get_text(strip=True))


    for i in range(len(titles)):
        review_data = {
            'title': titles[i] if i < len(titles) else '',
            'stars': ratings[i] if i < len(ratings) else '',
            'customer_name': customer_names[i] if i < len(customer_names) else '',
            'description': descriptions[i] if i < len(descriptions) else ''
        }
        all_reviews.append(review_data)

    return all_reviews

def get_stars(soup):
    #get list of reviews dictionaries.
    reviews = get_data(soup)

    star_vallues = []

    #looping through every review, check if the star key exist
    #then use regular expression
    for review in reviews:
        match = re.search(r'(\d+(\.\d+)?) out of 5', review['stars'])
        if match:
            star_value = float(match.group(1))
            star_vallues.append(star_value)

    if not star_vallues:
        return 0


    #calculate the Average    
    average_star = sum(star_vallues)/len(star_vallues)
        

    return average_star


def get_top_word(soup):
    reviews = get_data(soup)

    #gets a list of stop words and make the list a set.
    stop_words = set(stopwords.words('english'))


    #combine all the descriptions
    all_description = " ".join([review["description"] for review in reviews])

    clean_text = re.sub(r'[^a-zA-Z\s]', '', all_description.lower())

    words = word_tokenize(clean_text)
    filtered_words = [word for word in words if word not in stop_words]

    #count word frequency 

    word_counts = Counter(filtered_words)

    top_words = word_counts.most_common(10)
    

    return top_words


def Sentiment(soup):
    reviews = get_data(soup)
    sia = SentimentIntensityAnalyzer()

    combined_text = " ".join([review["description"] for review in reviews])


    overall_sentiment=sia.polarity_scores(combined_text)

    return {
        
        'overall_sentiment':overall_sentiment
    }


# Takes all scraped reviews, summarize them in manageable chunks using
# pretrained NLP model, and return a concise final summary.
def summarise(soup):
    reviews = get_data(soup)
    
    #concatenate all the reviews texs into One big String
    all_review = " ".join([review["description"] for review in reviews])

    #maximum number o tokens that the model can process at once.
    max_chunck_length = 1024

    #split the large review string into sntences
    sentences = all_review.split(". ")
    current_chunk = ""
    chunks = []

    #break text into safe chunks
    for sentence in sentences :
        tentative_chunk = sentence+". "
        tokenized = tokenizer.encode(tentative_chunk, add_special_tokens=False)

        if len(tokenized)<max_chunck_length:
            current_chunk += tentative_chunk
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    #ensures remaining chunk is added
    if current_chunk:
        chunks.append(current_chunk.strip())

    summaries = []
    #Runs the HuggingFace summarization pipeline on each chunk
    for text in chunks:
        #returns a list of dictionaris each containing a summary of the input text.
        output = summarizer(text, max_length=130, min_length=30, do_sample=False)
        summaries.append(output[0]["summary_text"])

    if len(summaries) == 1:
        return summaries[0]
    
    else:
        final = summarizer(" ".join(summaries), max_length=130, min_length=30, do_sample=False)
        return final[0]["summary_text"]

