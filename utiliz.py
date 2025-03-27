import cv2

def display_graph(image_path, nodes, edges):
    """Display detected nodes and edges on the image."""
    img = cv2.imread(image_path)

    for (x, y) in nodes:
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)  # Green nodes

    for (pt1, pt2) in edges:
        cv2.line(img, pt1, pt2, (255, 0, 0), 2)  # Blue edges

    cv2.imshow("Graph Visualization", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
