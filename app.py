from flask import Flask, render_template, request
import pandas
import numpy as np
popular_df = pandas.read_pickle('popular.pkl')
pt = pandas.read_pickle('pt.pkl')
books = pandas.read_pickle('books.pkl')
similarity_scores = pandas.read_pickle('similarity_scores.pkl')
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',
                           book_name =popular_df['Book-Title'].to_list(),
                           author=popular_df['Book-Author'].to_list(),
                           image=popular_df['Image-URL-M'].to_list(),
                           votes=popular_df['num_ratings'].to_list(),
                           rating=popular_df['avg_ratings'].to_list()

                           )

@app.route("/recommend")
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Check if user_input exists in the index
    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].to_list())
            item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].to_list())
            item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].to_list())

            data.append(item)

        print(data)
        return render_template('recommend.html', data=data)
    else:
        # Handle the case when user_input is not found
        error_message = f"No recommendations found for '{user_input}'."
        return render_template('recommend.html', error=error_message)


if __name__ == "__main__":
    app.run(debug=True)