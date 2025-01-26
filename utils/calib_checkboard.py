import numpy as np
import cv2 as cv
import glob
import os

# Termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points for an 8x8 chessboard with square size 1.7 cm
# square_size = 1.7
objp = np.zeros((7 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2) 

# Arrays to store object points and image points from all the images
objpoints = []  # 3D points in real-world space
imgpoints = []  # 2D points in image plane

# Get the list of calibration images
images = glob.glob(os.path.join(os.path.dirname(os.getcwd()), 'data/calib_image', '*.jpg'))

if not images:
    print("No images found in the directory. Please check the path.")
    exit()

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, (7, 7), None)

    # If found, add object points and image points (after refining them)
    if ret:
        objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (7, 7), corners2, ret)

        # Save the image with corners drawn
        base_name = os.path.basename(fname)
        save_name = os.path.join(os.path.dirname(fname), base_name.split('.')[0] + '_calib.jpg')
        cv.imwrite(save_name, img)

cv.destroyAllWindows()

# Camera calibration
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Save calibration parameters
camera_matrix_path = os.path.join(os.path.dirname(os.getcwd()), 'data/calib_image', 'camera_matrix.npy')
dist_coeffs_path = os.path.join(os.path.dirname(os.getcwd()), 'data/calib_image', 'dist_coeffs.npy')

np.save(camera_matrix_path, mtx)
np.save(dist_coeffs_path, dist)


# Perform undistortion on all images
for fname in images:
    img = cv.imread(fname)
    h, w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # Undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)

    # Crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    print(f"w: {w}, h: {h}")

    # Save the undistorted image
    base_name = os.path.basename(fname)
    save_name = os.path.join(os.path.dirname(fname), base_name.split('.')[0] + '_undistorted.jpg')

    cv.imwrite(save_name, dst)

# Calculate total reprojection error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
    mean_error += error

print("Total error: {:.4f}".format(mean_error / len(objpoints)))
