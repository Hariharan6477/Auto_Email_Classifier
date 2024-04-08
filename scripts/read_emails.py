from simplegmail import Gmail
import pickle,re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
import nltk,joblib,os
import matplotlib.pyplot as plt
from textblob import TextBlob
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')




marked={}
label_encoder=LabelEncoder()
categories={1:'Financial',2:'Pharmaceutical',4:'Travel',0:'Energy',3:'Technology'}
labelss=list(categories.values())+['Growth','Neutral','Volatility']


def predict_sentiment(email_text):
    # Create a TextBlob object
    blob = TextBlob(email_text)
    
    # Get the sentiment polarity
    polarity = blob.sentiment.polarity
    
    # Determine the sentiment based on the polarity
    if polarity > 0:
        return 'Growth'
    elif polarity < 0:
        return 'Volatility'
    else:
        return 'Neutral'



global first_time
first_time=True
# Assuming df_train is your DataFrame containing the 'pre_text' and 'post_text' columns

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove punctuation, convert to lowercase, and remove stopwords
    tokens = [word.lower() for word in tokens if word.isalnum() and word not in stopwords.words('english')]

    # Remove numbers and replace with <NUM>
    tokens = [re.sub(r'\d+', '<NUM>', word) for word in tokens]

    # Remove special characters
    tokens = [re.sub(r'[^a-zA-Z0-9]', '', word) for word in tokens]

    # Remove parentheses and their contents
    tokens = [re.sub(r'\([^)]*\)', '', word) for word in tokens]

    tokens = [word for word in tokens if word != '<NUM>']
    tokens = [word.replace('NUM', '') for word in tokens]

    # Lemmatize the tokens
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join the tokens back into a single string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text



def read_messages():
    gmail=Gmail()
    s=[i.snippet for i in gmail.get_unread_inbox()]
    s1=[i for i in gmail.get_unread_inbox()]
    for i in s1:
        i.mark_as_read()
    try:
        print(s1)
        if s1!=[]:
            labels = gmail.list_labels()

            vectorizer=joblib.load(r'C:\Users\jai61\Desktop\PLS DONT TOUCH IT 1\v3\scripts\vect.pkl')
            with open(r'C:\Users\jai61\Desktop\PLS DONT TOUCH IT 1\v3\scripts\nb_model.pkl','rb') as file:
                nb_model=pickle.load(file)
            print("model_loaded")
            for i in s:
                print(i)
                print()
            
            print(s1)
            if s1:
                for i in range(len(s)):
                    print('s1:',s1)
                    print()
                    print('i:',i)
                    email_text=s[i]
                    email_text=preprocess_text(email_text)
                    sentiment = predict_sentiment(email_text)
                    sentiment_label = list(filter(lambda x: x.name == sentiment, labels))[0]
                    s1[i].add_label(sentiment_label)
                    print("Sentiment:", sentiment)
                    
                    if sentiment=='Volatility':
                        print(12521)
                        params={
                            "to":s1[i].sender,
                            "sender":"barclaysmailreader@gmail.com",
                            "subject":"Response",
                            "msg_html": "<h2>Hello!</h2><br><p>Your mail has been acknowledged and our team will look into it.</p>",
                        }
                        gmail.send_message(**params)

                    preprocessed=[preprocess_text(s[i])]
                    x_new =vectorizer.transform(preprocessed)
                    x_new_reshaped=x_new.reshape(1,-1)
                    print('x_new_reshaped:',x_new_reshaped)
                    find = nb_model.predict(x_new_reshaped)[0]
                    print(find)
                    predicted_category = categories[find]
                    print(predicted_category)
                    f = 0
                    if predicted_category in categories.values():
                        f=1
                    if f:
                        print("Predicted Category:", predicted_category)
                        banking_label = list(filter(lambda x: x.name == predicted_category, labels))[0]
                        if s1:
                            x = s1[i]
                            cur_msg_labels=[i for i in x.label_ids if i in categories.values()]
                            if len(cur_msg_labels)==0:
                                x.add_label(banking_label)
                                xx={
                            'Financial':'hariharans6477@gmail.com',
                            'Technology':'hariharansd11@gmail.com',
                            'Travel':'sek615987@gmail.com',
                            'Energy':'sekirai14@gmail.com',
                            'Pharmaceutical':'loopdead78@gmail.com'
                                    }
                                params={
                                'to':xx[predicted_category],
                                'sender':'barclaysmailreader@gmail.com',
                                'msg_plain':s[i]
                            }
                                gmail.send_message(**params)
                        else:
                            if s1:
                                banking_label = list(filter(lambda x: x.name == 'Uncategorized', labels))[0]
                                x = s1[i]
                                x.add_label(banking_label)
            return ['Success']
        return ['Empty Inbox']


    except Exception as e:
        return "wdgweh"


