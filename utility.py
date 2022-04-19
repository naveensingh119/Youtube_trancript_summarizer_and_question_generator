# importing modules
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import networkx as nx
from youtube_transcript_api import YouTubeTranscriptApi
# using the srt variable with the list of dictonaries
# obtained by the the .get_transcript() function
def get_text(s):
    cnt=0;
    s=s.split('=')[-1]
    to_ret=""
    srt = YouTubeTranscriptApi.get_transcript(s)
    #print(srt[0]['text'])
    #print(len(srt))
# creating or overwriting a file "subtitles.txt" with
# the info inside the context manager
    with open("subtitles.txt", "w") as f:

     ##iterating through each element of list srt
        for i in srt:
        # writing each element of srt on a new line
            f.write("{}\n".format(i))
    with open("only_subtitles.txt", "w") as f:

     ##iterating through each element of list srt
        for i in range(len(srt)):
        # writing each element of srt on a new line
            f.write(str(srt[i]['text']))
            f.write(". ")
            to_ret+=srt[i]['text']
            to_ret+=". "
            cnt=cnt+1;
    for i in range(10):
        to_ret+="\n"
    return (to_ret,cnt);
########################################################################################################################
def read_article(s):
    sentences=sent_tokenize(s)
    #print(sentences)
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)
    #print(sentences)
    #print(sentences)
    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],i,s) for i,s in enumerate(sentences)), reverse=True)    
    #print("Indexes of top ranked_sentence order are ", ranked_sentence)    
    ranked_sentence=ranked_sentence[0:top_n]
    ranked_sentence.sort(key = lambda x: x[1])
    for i in range(top_n):
        summarize_text.append("".join(ranked_sentence[i][2]))
    
    # Step 5 - Offcourse, output the summarize texr
    text=""
    text=text.join(summarize_text)
    #print(text)
    #print(summarize_text)
    #summarize_text=".".join(summarize_text)
    #print("Summarize Text: \n", ".".join(summarize_text))

    return text
###############################################################################################################################
def make_text(s):
    text=s;
# Input text - to summarize
    # Tokenizing the text
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

# Creating a frequency table to keep the
# score of each word
##print(words)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

# Creating a dictionary to keep the score
# of each sentence
#print(text)
    sentences = sent_tokenize(text)
    #print(sentences[0])
    sentenceValue = dict()
#print(sentences)
    for sentence in sentences:
        #print(sentence)
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
            



    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

# Average value of a sentence from the original text

    average = int(sumValues / len(sentenceValue))

    print(average)
    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
        #print(sentenceValue[sentence])
        #print(sentence)
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.0 * average)):
            summary += " " + sentence
    
    return summary

########################################################################################################
def get_me_text(s):
    p=get_text(s)
    #return p[0]
    s1=""
    s1=make_text(p[0]);
    r=p[1]
    r/=4
    #return 
    s2=generate_summary(p[0],int(r));
    #print(s2)
    s=p[0]
    for i in range(10):
        s+="             ";
    s+="SUMMURIZED VERSION 1:\n"
    s=s+s1
    for i in range(10):
        s+='                \n';
    s+="SUMMURIZED VERSION 2:\n"
    s+=s2
    return s
print(get_me_text("https://www.youtube.com/watch?v=sv5hK4crIRc"))
if __name__ == "__main__":
    print("it is running.........")