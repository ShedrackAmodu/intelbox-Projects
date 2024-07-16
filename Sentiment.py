from textblob import TextBlob

def SentOriginal(text):
    # Calculate polarity and subjectivity
    polarity = TextBlob(text).sentiment.polarity
    subjectivity = TextBlob(text).sentiment.subjectivity

    # Determine sentiment based on polarity
    if polarity >= 0.5:
        polar_text = "highly positive sentiment"
    elif polarity <= -0.5:
        polar_text = "highly negative sentiment"
    else:
        polar_text = "neutral sentiment"

    # Determine perspective based on subjectivity
    if subjectivity < 0.5:
        subj_text = "more objective perspective"
    else:
        subj_text = "more subjective perspective"

    # Construct analysis result
    analysis_original = f'The text is written with a {polar_text} from a {subj_text}'
    
    return analysis_original

def SentParaphrased():
    text = "It was a good movie"

    # Calculate polarity and subjectivity
    polarity = TextBlob(text).sentiment.polarity
    subjectivity = TextBlob(text).sentiment.subjectivity

    # Determine sentiment based on polarity
    if polarity >= 0.5:
        polar_text = "highly positive sentiment"
    elif polarity <= -0.5:
        polar_text = "highly negative sentiment"
    else:
        polar_text = "neutral sentiment"

    # Determine perspective based on subjectivity
    if subjectivity < 0.5:
        subj_text = "more objective perspective"
    else:
        subj_text = "more subjective perspective"

    # Construct analysis result
    analysis_paraphrased = f'The text is written with a {polar_text} from a {subj_text}'
    
    return analysis_paraphrased

