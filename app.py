from flask import Flask, render_template,request
import pickle
import pandas as pd
import numpy as np

popular_df = pickle.load(open('popular_df1.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values),

                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    distances = similarity_scores[index]
    suggestions = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in suggestions:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        data.append(temp_df.drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-M']])
    df_rec = pd.concat(data)
    print(df_rec)

    return render_template('recommend.html',
                           book_name=list(df_rec['Book-Title'].values),
                           author=list(df_rec['Book-Author'].values),
                           image=list(df_rec['Image-URL-M'].values),
                           )

if __name__=='__main__':
    app.run(debug=True)