# Seekh - AI Pose Comparison & Performance Analysis System

## Overview

Seekh is an AI-powered pose comparison and performance analysis platform developed using Python and Streamlit.

The application compares a user's exercise or dance performance video against a reference video using pose estimation techniques. It analyzes body movements, measures pose similarity, and provides performance scores and visual feedback to help users improve their technique.

## Features

- AI-based pose comparison
- Exercise performance evaluation
- Dance movement analysis
- Video-to-video similarity scoring
- Performance trend visualization
- Interactive Streamlit interface
- Upload and compare custom videos
- Progress tracking through score analysis

## Technology Stack

Frontend:
- Streamlit

Backend:
- Python

Computer Vision:
- Pose Estimation
- Video Processing

Data Visualization:
- Matplotlib

Supporting Libraries:
- OpenCV
- NumPy

## Project Structure

seekh/

app.py

pose_compare.py

uploads/

reference dance.mp4

practise dance.mp4

reference excercise.mp4

practise excercise.mp4

exercise1.mp4

excercise 2.mp4

score_trend.png

README.md

## How It Works

1. Upload or select a practice video.
2. Select a reference exercise or dance video.
3. The system extracts body pose landmarks from both videos.
4. Movements are compared frame-by-frame.
5. A similarity score is generated.
6. Performance trends and visual analytics are displayed.

## Applications

Exercise Training

Compare workout videos against reference demonstrations to evaluate posture and movement accuracy.

Dance Learning

Analyze dance performance by comparing practice videos with professional reference videos.

Skill Improvement

Track progress over multiple attempts using generated scores and performance trends.

## Installation

Clone the repository:

git clone https://github.com/ykoritala-debug/seekh.git

Navigate to the project folder:

cd seekh

Install required dependencies:

pip install streamlit opencv-python mediapipe numpy matplotlib

## Running the Application

Start the Streamlit server:

streamlit run app.py

Open the application in your browser:

http://localhost:8501

## Output

The system generates:

- Pose Similarity Score
- Movement Accuracy Analysis
- Performance Reports
- Trend Visualization Graphs

Example:

Pose Match Score: 87%

Performance Rating: Good

## Future Enhancements

- Real-time webcam analysis
- AI-based improvement suggestions
- Personalized training recommendations
- Multi-user dashboard
- Cloud deployment
- Mobile integration

## Demo Video

🎥 Watch the complete project demonstration here:

https://drive.google.com/file/d/1uSBsB0418iUJ-7luUDRPxxND2CKzuM-Y/view?usp=drivesdk

## Author

Yamini Koritala

## License

This project is intended for educational, research, and demonstration purposes.
