import cv2
import os

def video_to_frames(video_path, output_dir):
    cap = cv2.VideoCapture(video_path) # Opens video file stream
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # Gets total frame count from video metadata
    frame_count = 0
    
    while cap.isOpened():
        # Loops while video is open, reads frames one by one. ret is success flag, frame contains image data
        ret, frame = cap.read() 
        if not ret: break # Exits if frame read fails
        
        # Here frame_count:0Xd can be adjusted based on how many frames you have in the file
        cv2.imwrite(f'{output_dir}/{frame_count:05d}.png', frame)
        if frame_count % 100 == 0:
            print(f'Processed {frame_count}/{total_frames} frames')
        frame_count += 1
        
    cap.release()

# Usage: video path, output folder path
video_to_frames('stock_video_base_1.mp4', 'raw_frames_2')