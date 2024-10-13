from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from collections import Counter
import skimage.morphology
import uuid
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Configuration
app.config['UPLOAD_FOLDER'] = './static/output'

# Enable CORS
CORS(app)

def process_images(image1_path, image2_path, output_dir):
    print('[INFO] Reading Images ...')
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Resize Images
    print('[INFO] Resizing Images ...')
    new_size = (image1.shape[0] // 5 * 5, image1.shape[1] // 5 * 5)  # Ensure dimensions are multiples of 5
    image1 = cv2.resize(image1, (new_size[1], new_size[0])).astype(int)
    image2 = cv2.resize(image2, (new_size[1], new_size[0])).astype(int)

    # Difference Image
    print('[INFO] Computing Difference Image ...')
    diff_image = abs(image1 - image2)
    cv2.imwrite(os.path.join(output_dir, 'difference.jpg'), diff_image)
    diff_image = diff_image[:, :, 1]

    # PCA and Feature Vector Space
    print('[INFO] Performing PCA ...')
    pca = PCA()
    vector_set, mean_vec = find_vector_set(diff_image, new_size)
    pca.fit(vector_set)
    EVS = pca.components_

    print('[INFO] Building Feature Vector Space ...')
    FVS = find_FVS(EVS, diff_image, mean_vec, new_size)
    components = 3

    # Clustering
    print('[INFO] Clustering ...')
    least_index, change_map = clustering(FVS, components, new_size)
    change_map[change_map == least_index] = 255
    change_map[change_map != 255] = 0
    change_map = change_map.astype(np.uint8)
    change_map_path = os.path.join(output_dir, 'ChangeMap.jpg')
    cv2.imwrite(change_map_path, change_map)

    # Morphological Operations
    print('[INFO] Performing Closing ...')
    kernel = skimage.morphology.disk(6)
    CloseMap = cv2.morphologyEx(change_map, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(os.path.join(output_dir, 'CloseMap.jpg'), CloseMap)

    print('[INFO] Performing Opening ...')
    OpenMap = cv2.morphologyEx(CloseMap, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(os.path.join(output_dir, 'OpenMap.jpg'), OpenMap)

    # Convert to URL format for change_map_path
    change_map_url = change_map_path.replace('\\', '/').replace('./static/', 'http://127.0.0.1:5000/static/')

    return change_map_url

def find_vector_set(diff_image, new_size):
    vector_set = []
    for j in range(0, new_size[0], 5):
        for k in range(0, new_size[1], 5):
            block = diff_image[j:j + 5, k:k + 5]
            if block.shape == (5, 5):  # Ensure block is of shape 5x5
                feature = block.ravel()
                vector_set.append(feature)
    
    vector_set = np.array(vector_set)
    mean_vec = np.mean(vector_set, axis=0)
    vector_set = vector_set - mean_vec
    return vector_set, mean_vec

def find_FVS(EVS, diff_image, mean_vec, new_size):
    feature_vector_set = []
    for i in range(2, new_size[0] - 2):
        for j in range(2, new_size[1] - 2):
            block = diff_image[i-2:i+3, j-2:j+3]
            if block.shape == (5, 5):  # Ensure block is of shape 5x5
                feature = block.flatten()
                feature_vector_set.append(feature)

    FVS = np.dot(feature_vector_set, EVS)
    FVS = FVS - mean_vec
    return FVS

def clustering(FVS, components, new_size):
    kmeans = KMeans(components, verbose=0)
    kmeans.fit(FVS)
    output = kmeans.predict(FVS)
    count = Counter(output)
    least_index = min(count, key=count.get)
    change_map = np.reshape(output, (new_size[0] - 4, new_size[1] - 4))
    return least_index, change_map

@app.route('/process', methods=['POST'])
def process():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "No file part"}), 400

    image1_file = request.files['image1']
    image2_file = request.files['image2']

    if image1_file.filename == '' or image2_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if image1_file and image2_file:
        # Save files locally temporarily
        image1_filename = str(uuid.uuid4()) + "_" + image1_file.filename
        image2_filename = str(uuid.uuid4()) + "_" + image2_file.filename
        image1_path = os.path.join(app.config['UPLOAD_FOLDER'], image1_filename)
        image2_path = os.path.join(app.config['UPLOAD_FOLDER'], image2_filename)
        image1_file.save(image1_path)
        image2_file.save(image2_path)

        change_map_url = process_images(image1_path, image2_path, app.config['UPLOAD_FOLDER'])

        # Return the URL instead of the absolute path
        return jsonify({
            "image1_url": image1_path.replace('\\', '/').replace('./static/', 'http://127.0.0.1:5000/static/'),
            "image2_url": image2_path.replace('\\', '/').replace('./static/', 'http://127.0.0.1:5000/static/'),
            "change_map_url": change_map_url
        })

    return jsonify({"error": "Something went wrong"}), 500

@app.route('/', methods=['GET'])
def Home():
    return "Hello From Home Page"

if __name__ == '__main__':
    app.run(debug=True)
