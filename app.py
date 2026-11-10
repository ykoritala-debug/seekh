import streamlit as st
import os
import subprocess
from PIL import Image

st.set_page_config(page_title="Pose Comparison", layout="wide")
st.title("💃 Dance Pose Comparison Tool")

# Upload section
st.sidebar.header("Upload Videos")
ref_video = st.sidebar.file_uploader("Reference Video", type=["mp4"])
perf_video = st.sidebar.file_uploader("Performance Video", type=["mp4"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if ref_video and perf_video:
    ref_path = os.path.join(UPLOAD_DIR, "reference.mp4")
    perf_path = os.path.join(UPLOAD_DIR, "performance.mp4")

    with open(ref_path, "wb") as f:
        f.write(ref_video.read())
    with open(perf_path, "wb") as f:
        f.write(perf_video.read())

    if st.sidebar.button("Run Pose Comparison"):
        with st.spinner("Processing videos..."):
            subprocess.run(["python", "pose_compare.py", ref_path, perf_path])
        st.success("✅ Comparison complete!")

        # Show score trend
        if os.path.exists("score_trend.png"):
            st.image(Image.open("score_trend.png"), caption="Deviation Score Over Time", use_column_width=True)
        else:
            st.warning("Score trend image not found.")
else:
    st.sidebar.info("Please upload both videos to begin.")