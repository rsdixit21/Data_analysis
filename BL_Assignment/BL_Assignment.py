import pandas as pd
from bs4 import BeautifulSoup
import requests  # Requests using Python
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
from google.colab import drive


df = pd.read_excel('/content/Input.xlsx')
links = df['URL'].values

# function to extract data

def extract_data():
    output = []
    # fetching data
    df = pd.read_excel('/content/Input.xlsx')
    links = df['URL'].values
    for i in range(150):
        url = links[i]
        # URL Fatching
        url_id = i+1

        # URL Request
        page_request = requests.get(url, headers={"User-Agent": "XY"})

        # Beautifulsoup
        soup = BeautifulSoup(page_request.content, 'html.parser')

        # 1. Sentimental Analysis

        # title
        title_tag = soup.find('h1', class_="entry-title")
        title = title_tag.text.replace('\n', " ")

        # content

        content_tag = soup.findAll(attrs={'class': 'td-post-content'})
        content_initial = content_tag[0].text.replace('\n', " ")  # removing new lines
        content_without_punc = re.sub(r'[^\w\s]', '', content_initial)  # removing punctuation

        with open('/content/StopWords_Auditor.txt', 'r') as f:
            stws_1 = f.readlines()
        stws_1 = [x.lower() for x in stws_1]
        for count, ele in enumerate(stws_1):
            if '  |' in ele or '\n' in ele:
                stws_1[count] = ele.split('\n')[0].strip()
                stws_1[count] = ele.split(' |')[0].strip()

        with open('/content/StopWords_Currencies.txt', 'r', encoding='latin-1') as f:
            stws_2 = f.readlines()
        stws_2 = [x.lower() for x in stws_2]
        for count, ele in enumerate(stws_2):
            if '  |' in ele or '\n' in ele:
                stws_2[count] = ele.split('\n')[0].strip()
                stws_2[count] = ele.split(' |')[0].strip()
        with open('/content/StopWords_DatesandNumbers.txt', 'r') as f:
            stws_3 = f.readlines()
        stws_3 = [x.lower() for x in stws_3]
        for count, ele in enumerate(stws_3):
            if '  |' in ele or '\n' in ele:
                stws_3[count] = ele.split('\n')[0].strip()
                stws_3[count] = ele.split(' |')[0].strip()

        with open('/content/StopWords_Generic.txt', 'r') as f:
            stws_4 = f.readlines()
        stws_4 = [x.lower() for x in stws_4]
        for count, ele in enumerate(stws_4):
            if '  |' in ele or '\n' in ele:
                stws_4[count] = ele.split('\n')[0].strip()
                stws_4[count] = ele.split(' |')[0].strip()

        with open('/content/StopWords_GenericLong.txt', 'r') as f:
            stws_5 = f.readlines()
        stws_5 = [x.lower() for x in stws_5]
        for count, ele in enumerate(stws_5):
            if '  |' in ele or '\n' in ele:
                stws_5[count] = ele.split('\n')[0].strip()
                stws_5[count] = ele.split(' |')[0].strip()

        with open('/content/StopWords_Geographic.txt', 'r') as f:
            stws_6 = f.readlines()
        stws_6 = [x.lower() for x in stws_6]
        for count, ele in enumerate(stws_6):
            if '  |' in ele or '\n' in ele:
                stws_6[count] = ele.split('\n')[0].strip()
                stws_6[count] = ele.split(' |')[0].strip()
        with open('/content/StopWords_Names.txt', 'r') as f:
            stws_7 = f.readlines()
        stws_7 = [x.lower() for x in stws_7]
        for count, ele in enumerate(stws_7):
            if '  |' in ele or '\n' in ele:
                stws_7[count] = ele.split('\n')[0].strip()
                stws_7[count] = ele.split(' |')[0].strip()
        my_stop_words_list = stws_1 + stws_2 + stws_3 + stws_4 + stws_5 + stws_6 + stws_7

        with open("/content/MasterDictionary/negative-words.txt", "r", encoding="ISO-8859-1") as negative:
            negatives = negative.read().split("\n")
        with open("/content/MasterDictionary/positive-words.txt", "r") as positive:
            positives = positive.read().split("\n")
        master_dictionary = dict({'neg_words':
                                      [word for word in negatives],
                                  'pos_words':
                                      [word for word in positives]})

        # tokenizing
        text_tokens_0 = word_tokenize(content_without_punc)
        text_tokens = [x.lower() for x in text_tokens_0]
        # removing stopwords
        tokens_without_stops = [word for word in text_tokens if not word in my_stop_words_list]
        # Positive_score
        Positive_score_list = [word for word in tokens_without_stops if word in master_dictionary['pos_words']]
        Positive_score = len(Positive_score_list)
        # Negative_score
        Negative_score_list = [word for word in tokens_without_stops if word in master_dictionary['neg_words']]
        Negative_score = len(Negative_score_list)

        # Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)

        Polarity_score = (Positive_score - Negative_score) / ((Positive_score + Negative_score) + 0.000001)

        # Subjectivity Score
        Subjectivity_score = (Positive_score + Negative_score) / ((len(tokens_without_stops)) + 0.000001)
        Subjectivity_score

        # 2 Analysis of Readability

        # Sentences tokenizing

        sentences_tokens = sent_tokenize(content_initial)
        num_sentences = len(sentences_tokens)
        num_words = len(text_tokens)

        # Average Sentence Length = the number of words / the number of sentences

        average_sentence_length = num_words / num_sentences
        

        # 4  calculate Complex_Words consedring word not ending from "ed" or "es"

        Complex_Words = []
        total_Syllable_count = 0
        for word in text_tokens:
            if (len(word) > 2 and (word.endswith("es" or "ed"))):
                continue
            count = 0
            vowels = ['a', 'e', 'i', 'o', 'u']
            for x in word:
                if (x in vowels):
                    count = count + 1
            total_Syllable_count += count
            if (count > 2):
                Complex_Words.append(word)
            else:
                continue

        Complex_Word_Count = len(Complex_Words)

        # Percentage of Complex Words = the number of complex words / the number of words
        Percentage_of_Complex_Words = ((Complex_Word_Count) / (num_words)) * 100

        # Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)

        Fog_Index = 0.4 * (average_sentence_length + (Percentage_of_Complex_Words))

        # 6   Syllable Count Per Word

        Syllable_Per_Word = (total_Syllable_count) / (num_words)

        # 3    Average Number of Words Per Sentence (with stopwords)

        # (the total number of words / the total number of sentences)
        total_number_of_words = len(text_tokens)
        total_number_of_sentences = len(sent_tokenize(content_initial))
        

        Average_Number_of_Words_Per_Sentence = (total_number_of_words) / (total_number_of_sentences)

        # 5    Word_Count

        # cleanng Data
        nltk_stop_words = set(stopwords.words('english'))

        tokens_without_stops_nltk = [word for word in text_tokens if not word in nltk_stop_words]
        Word_Count = len(tokens_without_stops_nltk)
        Word_Count

        # 7   calculate proper noun

        
        personal_pn = ['I', 'i', 'we', 'We', 'WE', 'my', 'My', 'MY', 'ours', 'Ours', 'OURS', 'us', 'Us']
        Personal_Pronouns = 0
        for word in personal_pn:
          if word in text_tokens_0:
            Personal_Pronouns += 1
         

        # 8   Average Word Length (formula : Sum of the total number of characters in each word/Total number of words)
        total_word_length = 0
        for word in text_tokens:
          total_word_length += len(word)
        Average_Word_Length = (total_word_length) / (len(text_tokens))

        output.insert(i, [url_id, url, Positive_score, Negative_score, Polarity_score, Subjectivity_score,
                          
                          average_sentence_length, Percentage_of_Complex_Words,

                          Fog_Index, Average_Number_of_Words_Per_Sentence, Complex_Word_Count, Word_Count, Syllable_Per_Word,

                          Personal_Pronouns, Average_Word_Length])
    return(output)
data = extract_data()

df = pd.DataFrame(data,
                  columns=['URL ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
                           'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
                           'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',
                           'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'])


drive.mount('/content/drive')
with open('/content/drive/My Drive/Assignment/Blackcoffer/assignment_output.xlsx', 'w') as f:
  df.to_csv(f)
