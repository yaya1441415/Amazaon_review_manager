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

    review_items = soup.find_all("li", {"data-hook": "review"})
    

    # Extract text and strip whitespace
    

    for item in review_items:
        # Customer name
        name_tag = item.find("span", class_="a-profile-name")
        customer_name = name_tag.get_text(strip=True) if name_tag else ""

        # Star rating
        star_tag = item.find("i", {"data-hook": "review-star-rating"})
        stars = star_tag.get_text(strip=True) if star_tag else ""

        # Review title
        title_tag = item.find("a", {"data-hook": "review-title"})
        title = ""
        if title_tag:
            # title can be inside a <span>
            span = title_tag.find("span")
            title = span.get_text(strip=True) if span else title_tag.get_text(strip=True)

        # Review body
        body_tag = item.find("span", {"data-hook": "review-body"})
        description = body_tag.get_text(strip=True) if body_tag else ""

        review_data = {
            "title": title,
            "stars": stars,
            "customer_name": customer_name,
            "description": description
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

    
    print(reviews)
    
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
        tentative_chunk = (current_chunk + " " +sentence).strip() +". "
        tokenized = tokenizer.encode(tentative_chunk, add_special_tokens=False)

        if len(tokenized) <= max_chunck_length:
            current_chunk = tentative_chunk
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
        output = summarizer(text, max_length=100, min_length=30, do_sample=False)
        summaries.append(output[0]["summary_text"])

    if len(summaries) == 1:
        return summaries[0]
    
    else:
        final = summarizer(" ".join(summaries), max_length=130, min_length=30, do_sample=False)
        return final[0]["summary_text"]

