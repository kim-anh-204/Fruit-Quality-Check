from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from ultralytics import YOLO
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt


# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the trained MobileNetV2 model
model = tf.keras.models.load_model('fruit_transfer.keras')

# Load YOLOv8 model (pre-trained for object detection)
yolo_model = YOLO('yolov8m.pt')

# Define class labels for your MobileNetV2 model
class_labels = ['fresh_apple', 'fresh_banana', 'fresh_orange', 'rotten_apple', 'rotten_banana', 'rotten_orange']

# Define YOLO class IDs for fruits (based on COCO dataset used by YOLOv8)
fruit_classes = {
    47: 'apple',  # COCO class ID for apple
    46: 'banana',  # COCO class ID for banana
    49: 'orange'  # COCO class ID for orange
}

def preprocess_image(img, target_size=(224, 224)):
    """Preprocess image for MobileNetV2 model."""
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Rescale pixel values
    return img_array

def classify_fruit(img):
    """Classify an image using the MobileNetV2 model."""
    img_array = preprocess_image(img)
    predictions = model.predict(img_array, verbose=0)  # Suppress prediction logs
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]
    return class_labels[predicted_class], confidence

def draw_annotations(img, detections):
    """Draw bounding boxes and classification labels on the image."""
    annotated_img = img.copy()
    for detection in detections:
        x1, y1, x2, y2 = detection['bbox']
        label = detection['classification']
        confidence = detection['classification_confidence']
        fruit_type = detection['fruit_type']

        # Draw bounding box
        color = (0, 255, 0)  # Green for bounding box
        cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, 2)

        # Prepare label text
        text = f"{fruit_type}: {label} ({confidence:.2f})"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 1
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

        # Draw text background
        text_x, text_y = x1, y1 - 10 if y1 - 10 > 10 else y1 + 20
        text_bg_x2 = text_x + text_size[0] + 4
        text_bg_y2 = text_y + text_size[1] - 4
        cv2.rectangle(annotated_img, (text_x, text_y - text_size[1]), (text_bg_x2, text_bg_y2), color, -1)

        # Draw text
        cv2.putText(annotated_img, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)

    return annotated_img

def add_padding(img, padding=50):

    h, w = img.shape[:2]
    new_img = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    return new_img


def detect_and_classify(image_path, output_dir='cropped_fruits', output_image_path='static/uploads/annotated_image.jpg'):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the input image
    img = cv2.imread(image_path)
    img = add_padding(img, padding=50) 
    if img is None:
        raise ValueError(f"Could not load image at {image_path}")

    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Perform YOLO detection with adjusted thresholds
    results = yolo_model(img, conf=0.5, iou=0.45, verbose=False)
    detections = [result for result in results[0].boxes if int(result.cls) in fruit_classes]

    # Filter overlapping boxes
    def calculate_iou(box1, box2):
        x1, y1, x2, y2 = box1
        x1_, y1_, x2_, y2_ = box2
        inter_x1 = max(x1, x1_)
        inter_y1 = max(y1, y1_)
        inter_x2 = min(x2, x2_)
        inter_y2 = min(y2, y2_)
        inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
        area1 = (x2 - x1) * (y2 - y1)
        area2 = (x2_ - x1_) * (y2_ - y1_)
        return inter_area / (area1 + area2 - inter_area)

    filtered_detections = []
    for i, det in enumerate(detections):
        keep = True
        for j, other_det in enumerate(filtered_detections):
            iou = calculate_iou(det.xyxy[0], other_det.xyxy[0])
            if iou > 0.7 and det.conf < other_det.conf:
                keep = False
                break
        if keep:
            filtered_detections.append(det)

    detections = filtered_detections

    # List to store results
    classifications = []

    if len(detections) == 0:
        print("No fruits detected in the image.")
        return classifications, output_image_path
    elif len(detections) == 1:
        # Single object: Classify the entire image with MobileNetV2
        predicted_label, pred_confidence = classify_fruit(img_pil)

        detection = detections[0]
        class_id = int(detection.cls)
        x1, y1, x2, y2 = map(int, detection.xyxy[0])
        yolo_confidence = detection.conf.item()

        classifications.append({
            'fruit_type': fruit_classes[class_id],
            'yolo_confidence': yolo_confidence,
            'classification': predicted_label,
            'classification_confidence': pred_confidence,
            'cropped_image_path': None,
            'bbox': (x1, y1, x2, y2)
        })
    else:
        # Multiple objects: Crop and classify each fruit
        for i, detection in enumerate(detections):
            class_id = int(detection.cls)
            x1, y1, x2, y2 = map(int, detection.xyxy[0])
            yolo_confidence = detection.conf.item()

            # Crop the detected fruit
            cropped_img = img[y1:y2, x1:x2]
            cropped_img_pil = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))

            # Save cropped image
            cropped_img_path = os.path.join(output_dir, f'fruit_{i}.jpg')
            cropped_img_pil.save(cropped_img_path)

            # Classify the cropped fruit
            predicted_label, pred_confidence = classify_fruit(cropped_img_pil)

            classifications.append({
                'fruit_type': fruit_classes[class_id],
                'yolo_confidence': yolo_confidence,
                'classification': predicted_label,
                'classification_confidence': pred_confidence,
                'cropped_image_path': cropped_img_path,
                'bbox': (x1, y1, x2, y2)
            })

    # Draw annotations on the image
    annotated_img = draw_annotations(img, classifications)

    # Save the annotated image
    cv2.imwrite(output_image_path, annotated_img)

    # Print results
    for result in classifications:
        print(f"Detected: {result['fruit_type']} (YOLO confidence: {result['yolo_confidence']:.2f})")
        print(f"Classified as: {result['classification']} (confidence: {result['classification_confidence']:.2f})")
        if result['cropped_image_path']:
            print(f"Cropped image saved at: {result['cropped_image_path']}")
        print(f"Bounding box: {result['bbox']}")
        print("-" * 50)

    return classifications, output_image_path


@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', results=None)

        file = request.files['file']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        results, annotated_path = detect_and_classify(filepath)
        annotated_filename = os.path.basename(annotated_path)  # annotated_image.jpg

        os.remove(filepath)

        return render_template('index.html', results=results, image_file=annotated_filename)
    
    
    return redirect('/')

@app.route('/send_file/<filename>')
def send_file_route(filename):
    return send_from_directory('static/uploads', filename)



if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(STATIC_FOLDER, exist_ok=True)
    app.run(debug=True)
