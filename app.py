from flask import Flask, request, jsonify
import json
import uuid

app = Flask(__name__)
DATA_FILE = "reviews.json"

# Load all reviews from the JSON file
def load_reviews():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save reviews back to the JSON file
def save_reviews(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# GET all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    return jsonify(load_reviews())

# POST a new review
@app.route('/reviews', methods=['POST'])
def add_review():
    data = load_reviews()
    new_review = request.json
    new_review['id'] = str(uuid.uuid4())
    data.append(new_review)
    save_reviews(data)
    return jsonify(new_review), 201

# PUT (update) a review by ID
@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    data = load_reviews()
    for review in data:
        if review['id'] == review_id:
            review.update(request.json)
            save_reviews(data)
            return jsonify(review)
    return jsonify({'error': 'Review not found'}), 404

# DELETE a review by ID
@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    data = load_reviews()
    updated_data = [r for r in data if r['id'] != review_id]
    if len(updated_data) == len(data):
        return jsonify({'error': 'Review not found'}), 404
    save_reviews(updated_data)
    return jsonify({'message': 'Review deleted'})

if __name__ == '__main__':
    app.run(debug=True)
