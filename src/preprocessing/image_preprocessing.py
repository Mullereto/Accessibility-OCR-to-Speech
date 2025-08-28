import cv2

def Hough_transform(image):
    import numpy as np
    edges = cv2.Canny(image, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    angles = []
    for rho, theta in lines[:,0]:
        angle = (theta - np.pi/2) * 180/np.pi
        angles.append(angle)
    median_angle = np.median(angles)

    # Rotate image
    (h, w) = image.shape
    M = cv2.getRotationMatrix2D((w//2, h//2), median_angle, 1.0)
    deskewed = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)
    return deskewed


def preprocess_pipeline(image):
    
    # Bilateral filter (edges sharp)
    image = cv2.bilateralFilter(image, 9, 75, 75)
    
    
    # Deblurring (Enhance edges)
    blurred = cv2.GaussianBlur(image, (9, 9), 10)
    image = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
    
    
    # Contrast Enhancement
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    image = clahe.apply(gray)
    
    # Hough transform
    image = Hough_transform(image)

    return image


if __name__ == '__main__':
    
    image = preprocess_pipeline('docs\Screenshot 2025-08-25 172211.png')
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    

    

