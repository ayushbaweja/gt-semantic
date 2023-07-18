import json
import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch


# Load the cleaned JSON data
with open('coursesclean.json') as file:
    data = json.load(file)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
try:
    embeddings_array = np.stack(np.load('embeddings.npy'))
    with open('index.json') as file:
        index = json.load(file)
except:
    # Create an index and embeddings array
    index = {}
    embeddings = []

    # Iterate over each course
    for course_code, course_info in data.items():
        course_name = course_info['course_name']
        course_desc = course_info['course_desc']

        text = f"{course_name} {course_desc}"

        output = model.encode(text, convert_to_tensor=True)
        course_embeddings = np.array(output)

        # Store the embeddings in the array
        embeddings.append(course_embeddings)

        # Index the embeddings
        index[course_code] = len(embeddings) - 1

    # Convert the embeddings array to a NumPy array
    embeddings_array = np.stack(embeddings)

    np.save('embeddings.npy', embeddings_array)
    with open('index.json', 'w') as file:
        json.dump(index, file, indent=2)

query = 'Big Bang Theory'
query_embedding = model.encode([query], convert_to_tensor=True)

# Calculate cosine similarity
cos_scores = util.cos_sim(query_embedding, embeddings_array)[0]

# Get top-k similar courses
top_k = 5
top_results = torch.topk(cos_scores, k=top_k)

# Print the top-k courses
for idx in top_results[1]:
    course_code = list(index.keys())[idx]
    course_info = data[course_code]
    print(f"Course Code: {course_code}")
    print(f"Course Name: {course_info['course_name']}")
    print(f"Course Description: {course_info['course_desc']}")
    print()