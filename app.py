import os
import streamlit as st
from PIL import Image
from ultralytics import YOLO

# Load YOLO model
model_path = os.getenv("best.pt")  # Set YOLO_MODEL_PATH environment variable
model = YOLO(model_path)

# Function to track objects in a video
def track_objects(video_path, output_dir):
    result = model.track(video_path, save=True, save_dir=output_dir)
    # Find the latest track folder
    latest_track_folder = max([os.path.join(output_dir, d) for d in os.listdir(output_dir)], key=os.path.getmtime)
    tracked_video_path = os.path.join(latest_track_folder, "tracked_video.mp4")
    return tracked_video_path

# Streamlit UI
st.title('Object Tracking')

# Video tracking section
st.header('Video Tracking')
video_file = st.file_uploader("Upload a video", type=['mp4'])

if video_file is not None:
    st.video(video_file)
    if st.button('Track Objects'):
        with st.spinner('Tracking objects...'):
            # Save uploaded video to a temporary location
            video_path = os.path.join("temp", "temp_video.mp4")
            output_dir = os.path.join("temp", "runs", "detect")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            with open(video_path, "wb") as f:
                f.write(video_file.read())
            tracked_video_path = track_objects(video_path, output_dir)
            if tracked_video_path:
                st.video(tracked_video_path)
            else:
                st.error("Error occurred while tracking objects.")

# Cleanup temporary files
if os.path.exists(video_path):
    os.remove(video_path)