# Image Captioning System

This is an image captioning system that generates captions for images using a pre-trained ResNet50 model and a custom caption generation model.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `model` directory and place the following files in it:
   - `caption_model.h5` - The trained caption generation model
   - `tokenizer.pkl` - The tokenizer used for text processing

3. Place your test image in the root directory as `test.jpg` or update the `IMAGE_PATH` in `main.py`

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Load the model and tokenizer
2. Process the test image
3. Generate and display a caption for the image 