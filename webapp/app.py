import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

# Load your dataset
property_data = pd.read_csv('../data/raw/property_data1.csv')  # Make sure the path is correct

# Vectorize the property descriptions
vectorizer = TfidfVectorizer()

# Extract the 'description' column
X_description = vectorizer.fit_transform(property_data['description'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user input from the form
        user_description = request.form.get("description")
        user_location = request.form.get("location")  # Add location input
        user_price = float(request.form.get("price"))  # Add price input

        # Vectorize the user input description
        user_input_vectorized = vectorizer.transform([user_description])

        # Calculate cosine similarity for the description
        description_similarity = cosine_similarity(user_input_vectorized, X_description).flatten()

        # Calculate similarity based on location (exact match or string similarity)
        location_similarity = property_data['location'].apply(lambda x: 1 if user_location.lower() in x.lower() else 0)

        # Normalize prices to be between 0 and 1 for fair comparison
        property_data['normalized_price'] = (property_data['price'] - property_data['price'].min()) / (property_data['price'].max() - property_data['price'].min())
        user_normalized_price = (user_price - property_data['price'].min()) / (property_data['price'].max() - property_data['price'].min())

        # Calculate price similarity (closer price has higher similarity)
        price_similarity = 1 - np.abs(property_data['normalized_price'] - user_normalized_price)

        # Combine all similarity scores (description, location, price) with weights
        total_similarity = (0.5 * description_similarity) + (0.3 * location_similarity) + (0.2 * price_similarity)

        # Get the top 5 most similar properties
        top_5_similar_indices = total_similarity.argsort()[-5:][::-1]
        top_5_properties = property_data.iloc[top_5_similar_indices]

        # Display the top 5 similar properties
        return render_template('index.html', properties=top_5_properties.to_dict(orient='records'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
