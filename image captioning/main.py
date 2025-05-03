import numpy as np
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
import os
import argparse

# === CONFIGURATION ===
MODEL_PATH = "model/caption_model.h5"
TOKENIZER_PATH = "model/tokenizer.pkl"
MAX_LENGTH = 34

# === FEATURE EXTRACTOR ===
def extract_features(img_path):
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image file not found: {img_path}")
        
    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x, verbose=0)
    return features

# === CAPTION GENERATOR ===
def generate_caption(model, tokenizer, photo_feature):
    in_text = 'startseq'
    for _ in range(MAX_LENGTH):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=MAX_LENGTH)
        yhat = model.predict([photo_feature, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = tokenizer.index_word.get(yhat)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text.replace('startseq', '').replace('endseq', '').strip()

# === MAIN ===
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate captions for images')
    parser.add_argument('--image', type=str, help='Path to the image file')
    args = parser.parse_args()

    # Check if image path is provided
    if not args.image:
        print("❌ Error: No image path provided.")
        print("Usage: python main.py --image path/to/your/image.jpg")
        exit()

    # Check model files
    if not os.path.exists(MODEL_PATH) or not os.path.exists(TOKENIZER_PATH):
        print("⚠️ Error: Model or tokenizer file not found.")
        print("Please make sure you have the following files in the 'model/' directory:")
        print(f"- {MODEL_PATH}")
        print(f"- {TOKENIZER_PATH}")
        exit()

    try:
        print("🔄 Loading model and tokenizer...")
        model = load_model(MODEL_PATH)
        with open(TOKENIZER_PATH, 'rb') as f:
            tokenizer = pickle.load(f)

        print(f"📷 Processing image: {args.image}")
        features = extract_features(args.image)
        caption = generate_caption(model, tokenizer, features)

        print("\n📝 Generated Caption:")
        print(caption)

    except FileNotFoundError as e:
        print(f"❌ Error: {str(e)}")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
