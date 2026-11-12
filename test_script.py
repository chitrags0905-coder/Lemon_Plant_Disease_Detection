import cv2
import numpy as np
import urllib.request
from skimage import measure, morphology
from app import DiseaseDetectionSystem

# Fetch a sample lemon disease image using a user agent
sys = DiseaseDetectionSystem()

image = cv2.imread(r"d:\2year\dip\dip3\disease_detection_system\uploads\20260304_025157_IMG20260101170304.jpg")
preprocessed = sys.preprocess_image(image)
original = preprocessed.copy()

def segment_custom(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 1. Create a robust leaf mask
    # Leaves usually have some saturation and are not completely black or white
    # S > 20 and V > 20 and V < 245
    lower_leaf = np.array([0, 20, 20])
    upper_leaf = np.array([180, 255, 245])
    leaf_mask = cv2.inRange(hsv, lower_leaf, upper_leaf)
    
    # Fill holes in leaf mask and keep only the largest component(s)
    # Morphological closing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    leaf_mask = cv2.morphologyEx(leaf_mask, cv2.MORPH_CLOSE, kernel)
    leaf_mask = cv2.morphologyEx(leaf_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    
    # Find contours to keep only major leaf areas (remove small noise)
    contours, _ = cv2.findContours(leaf_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    clean_leaf_mask = np.zeros_like(leaf_mask)
    if contours:
        # Sort by area and keep the largest ones (e.g., > 5000 pixels depending on image size)
        img_area = img.shape[0] * img.shape[1]
        for cnt in contours:
            if cv2.contourArea(cnt) > img_area * 0.01: # larger than 1% of image
                cv2.drawContours(clean_leaf_mask, [cnt], -1, 255, -1)
    
    # 2. Identify healthy green regions
    # Green hue is roughly 35 to 85. We can expand slightly if needed.
    lower_green = np.array([30, 30, 30])
    upper_green = np.array([90, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # 3. Diseased region = Leaf but NOT Green
    diseased_mask = cv2.bitwise_and(clean_leaf_mask, cv2.bitwise_not(green_mask))
    
    return diseased_mask

sys.segment_disease_regions = segment_custom

initial_mask = sys.segment_disease_regions(preprocessed)
cv2.imwrite('test_mask_initial.jpg', initial_mask)

refined_mask = sys.apply_morphological_operations(initial_mask)
cv2.imwrite('test_mask_refined.jpg', refined_mask)

features, labeled_mask = sys.extract_features(refined_mask, original)
severity_info = sys.calculate_severity(refined_mask, original.shape)

out = sys.create_severity_map(original, refined_mask, severity_info, features)
cv2.imwrite('test_out.jpg', out)

print(f"Features mapped: {len(features)}")
print(f"Severity: {severity_info}")
