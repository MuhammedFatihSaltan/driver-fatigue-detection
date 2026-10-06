import cv2
import numpy as np

class HeadPoseEstimator:
    def __init__(self):
        self.model_points = np.array([
            (0.0, 0.0, 0.0),             
            (0.0, 330.0, -65.0),         
            (-225.0, -170.0, -135.0),    
            (225.0, -170.0, -135.0),     
            (-150.0, 150.0, -125.0),     
            (150.0, 150.0, -125.0)       
        ], dtype=np.float64)

    def estimate_pose(self, image_points, frame_shape):
        h, w, c = frame_shape
        focal_length = w
        center = (w / 2, h / 2)
        
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )
        
        dist_coeffs = np.zeros((4, 1))
        image_points = np.array(image_points, dtype="double")
        
        (success, rotation_vector, translation_vector) = cv2.solvePnP(
            self.model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        rmat, _ = cv2.Rodrigues(rotation_vector)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
        
        pitch = angles[0] 
        yaw = angles[1]   
        
        direction = "On"
        
        # Sınırlar yeniden düzenlendi:
        # > 70 veya < -70: Arka
        # 30 ile 70 arası: Sağ/Sol
        if yaw < -70 or yaw > 70:
            direction = "Arka"
        elif yaw < -30:
            direction = "Sol"
        elif yaw > 30:
            direction = "Sag"
        elif pitch < -20:
            direction = "Asagi"
        elif pitch > 20:
            direction = "Yukari"
            
        return direction, pitch, yaw