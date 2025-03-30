import cv2
import numpy as np
from matplotlib import pyplot as plt

def preprocess_image(image_path):
    """Advanced preprocessing with multiple techniques"""
    try:
        print(f"🖼️ Loading {image_path.split('/')[-1]}")
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image not found")
        
        # Convert to grayscale and enhance contrast
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Adaptive thresholding with inversion
        binary = cv2.adaptiveThreshold(enhanced, 255, 
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 2)
        
        # Morphological operations
        kernel = np.ones((3,3), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Debug save
        cv2.imwrite('debug_processed.jpg', processed)
        return processed
        
    except Exception as e:
        print(f"❌ Preprocessing failed: {str(e)}")
        return None

def detect_nodes_edges(processed_img):  # Changed from detect_elements to detect_nodes_edges
    """Comprehensive node and edge detection"""
    nodes = []
    edges = []
    
    # Detect both nodes and letters
    contours, _ = cv2.findContours(processed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Parameters (adjust based on your image)
    node_area_range = (100, 3000)  # Area range for nodes
    letter_area_range = (50, 500)   # Area range for letters
    min_edge_length = 20
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        aspect_ratio = w/h
        
        # Node detection (circular/compact shapes)
        if node_area_range[0] < area < node_area_range[1] and 0.7 < aspect_ratio < 1.3:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                nodes.append((cx, cy))
        
        # Edge detection (long thin contours)
        elif area > min_edge_length and max(w,h)/min(w,h) > 3:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if len(approx) >= 2:
                pt1 = tuple(approx[0][0])
                pt2 = tuple(approx[-1][0])
                edges.append((pt1, pt2))
    
    print(f"🔵 Nodes: {len(nodes)} | 📏 Edges: {len(edges)}")
    return nodes, edges
