from textblob import TextBlob

def analyze_comments(comments):
    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    positive_comments = []
    negative_comments = []

    for comment in comments:
        analysis = TextBlob(comment)
        if analysis.sentiment.polarity > 0:
            sentiments['positive'] += 1
            positive_comments.append(comment)
        elif analysis.sentiment.polarity < 0:
            sentiments['negative'] += 1
            negative_comments.append(comment)
        else:
            sentiments['neutral'] += 1

    most_positive_comment = max(positive_comments, key=lambda c: TextBlob(c).sentiment.polarity)
    most_negative_comment = max(negative_comments, key=lambda c: TextBlob(c).sentiment.polarity)

    return sentiments, most_positive_comment, most_negative_comment
