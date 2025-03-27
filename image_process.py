import cv2
import numpy as np

def preprocess_image(image_path):
    """Convert image to grayscale and detect edges."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"❌ ERROR: Could not read image at {image_path}")
        return None

    img = cv2.GaussianBlur(img, (5, 5), 0)  
    edges = cv2.Canny(img, 50, 150)  
    return edges

def detect_nodes_edges(edges):
    """Detect nodes (circles) and edges from processed image."""
    if edges is None:
        print("❌ ERROR: No edge data received for processing.")
        return None, None
    
    # Detect circular nodes using HoughCircles
    circles = cv2.HoughCircles(
        edges, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
        param1=50, param2=30, minRadius=5, maxRadius=30
    )

    # Detect edges using contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    nodes = []
    edge_list = []  # Avoid overwriting 'edges'

    # Process detected circles (nodes)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, r = circle
            nodes.append((x, y))  # Store detected nodes

    # Process detected contours (edges)
    for contour in contours:
        if cv2.contourArea(contour) < 10:  # Filter out small noise
            continue

        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        for i in range(len(approx)):
            pt1 = tuple(approx[i][0])
            pt2 = tuple(approx[(i + 1) % len(approx)][0])
            edge_list.append((pt1, pt2))

    return nodes, edge_list
