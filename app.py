from flask import Flask,render_template,request
import pickle
import pandas
import numpy as np

popular_df=pickle.load(open('Popular.pkl','rb'))
pivot_table=pickle.load(open('pivot_table.pkl','rb'))
popular_book=pickle.load(open('popular_book.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))
famous_A_books=pickle.load(open('famous_A_books.pkl','rb'))
famous_C_books=pickle.load(open('famous_C_books.pkl','rb'))
famous_Y_books=pickle.load(open('famous_Y_books.pkl','rb'))
famous_S_books=pickle.load(open('famous_S_books.pkl','rb'))


app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Title'].values),
                           Author_name=list(popular_df['Author'].values),
                           publisher_name=list(popular_df['Publisher'].values),
                           image=list(popular_df['Image_URL_M'].values),
                           votes=list(popular_df['Rating_count'].values),
                           rating=list((popular_df['Average_Rating'].values.round(2)))
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index = np.where(pivot_table.index == user_input)[0][0]  # fetching the index of book_name
    similar_book = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[
                   1:6]  # for that index finding similarity score with high values

    data = []
    for i in similar_book:
        item = []
        tem_df = popular_book[popular_book['Title'] == pivot_table.index[i[0]]]
        item.extend(list(tem_df.drop_duplicates("Title")['Title'].values))
        item.extend(list(tem_df.drop_duplicates("Title")['Author'].values))
        item.extend(list(tem_df.drop_duplicates("Title")['Image_URL_M'].values))

        data.append(item)
    print(data)

    return render_template('recommend.html',data=data)

@app.route('/Age_Recommendation')
def Age_Recommendation_ui():
    return render_template('Age_Recommendation.html')



@app.route('/Age_Recommendation/Children')
def Age_Recommendation_Children():
    return render_template('Age_Recommendation.html',
                           book_name=list(famous_C_books['Title'].values),
                           Author_name=list(famous_C_books['Author'].values),
                           publisher_name=list(famous_C_books['Publisher'].values),
                           image=list(famous_C_books['Image_URL_M'].values),
                           votes=list(famous_C_books['Rating_count'].values),
                           rating=list((famous_C_books['Avg_Rating'].values.round(2)))
                           )

@app.route('/Age_Recommendation/Youth')
def Age_Recommendation_Youth():
    return render_template('Age_Recommendation.html',
                           book_name=list(famous_Y_books['Title'].values),
                           Author_name=list(famous_Y_books['Author'].values),
                           publisher_name=list(famous_Y_books['Publisher'].values),
                           image=list(famous_Y_books['Image_URL_M'].values),
                           votes=list(famous_Y_books['Rating_count'].values),
                           rating=list((famous_Y_books['Avg_Rating'].values.round(2)))
                           )

@app.route('/Age_Recommendation/Adult')
def Age_Recommendation_Adult():
    return render_template('Age_Recommendation.html',
                           book_name=list(famous_A_books['Title'].values),
                           Author_name=list(famous_A_books['Author'].values),
                           publisher_name=list(famous_A_books['Publisher'].values),
                           image=list(famous_A_books['Image_URL_M'].values),
                           votes=list(famous_A_books['Rating_count'].values),
                           rating=list((famous_A_books['Avg_Rating'].values.round(2)))
                           )
@app.route('/Age_Recommendation/Senior')
def Age_Recommendation_Senior():
    return render_template('Age_Recommendation.html',
                           book_name=list(famous_S_books['Title'].values),
                           Author_name=list(famous_S_books['Author'].values),
                           publisher_name=list(famous_S_books['Publisher'].values),
                           image=list(famous_S_books['Image_URL_M'].values),
                           votes=list(famous_S_books['Rating_count'].values),
                           rating=list((famous_S_books['Avg_Rating'].values.round(2)))
                           )






if __name__=='__main__':
    app.run(debug="True")

