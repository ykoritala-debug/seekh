import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Video paths
ref_path = r"C:\\Users\\YAMINI\\OneDrive\\Desktop\\seekh\\practise dance.mp4"
perf_path = r"C:\\Users\\YAMINI\\OneDrive\\Desktop\\seekh\\reference dance.mp4"
ref_cap = cv2.VideoCapture(ref_path)
perf_cap = cv2.VideoCapture(perf_path)

# Get frame rate and dimensions
fps = ref_cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps) if fps > 0 else 33
width = int(ref_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(ref_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Joint names for feedback
joint_names = [lm.name.lower().replace("_", " ") for lm in mp_pose.PoseLandmark]

# Score history for live graph
score_history = deque(maxlen=100)
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')
ax.set_ylim(0, 50)
ax.set_xlim(0, 100)
ax.set_xlabel('Frame')
ax.set_ylabel('Deviation Score')
ax.set_title('Performance Over Time')

# Extract pose landmarks from a frame
def get_landmarks(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)
    if results.pose_landmarks:
        h, w, _ = frame.shape
        return np.array([[lm.x * w, lm.y * h] for lm in results.pose_landmarks.landmark])
    return None
   
# Compare two sets of landmarks
def compare_poses(ref_landmarks, perf_landmarks):
    if ref_landmarks is None or perf_landmarks is None:
        return None, None
    ref_centered = ref_landmarks - np.mean(ref_landmarks, axis=0)
    perf_centered = perf_landmarks - np.mean(perf_landmarks, axis=0)
    distances = np.linalg.norm(ref_centered - perf_centered, axis=1)
    score = np.mean(distances)
    worst_joint_index = np.argmax(distances)
    return score, worst_joint_index

# Feedback based on deviation score
def get_feedback(score):
    if score < 10:
        return "Excellent! Keep it up!"
    elif score < 20:
        return "Good effort! Try refining your movements."
    elif score < 30:
        return "Noticeable differences. Focus on posture and timing."
    else:
        return "Significant mismatch. Practice the steps more carefully."

# Main loop
while True:
    ref_ret, ref_frame = ref_cap.read()
    perf_ret, perf_frame = perf_cap.read()
    if not ref_ret or not perf_ret:
        print("End of one or both videos.")
        break

    # Resize frames to match
    ref_frame = cv2.resize(ref_frame, (width, height))
    perf_frame = cv2.resize(perf_frame, (width, height))

    # Get landmarks
    ref_landmarks = get_landmarks(ref_frame)
    perf_landmarks = get_landmarks(perf_frame)
    deviation_score, worst_joint_index = compare_poses(ref_landmarks, perf_landmarks)

    # Update score history and plot
    if deviation_score is not None:
        score_history.append(deviation_score)
        line.set_ydata(score_history)
        line.set_xdata(range(len(score_history)))
        ax.set_xlim(0, max(100, len(score_history)))
        fig.canvas.draw()
        fig.canvas.flush_events()

    # Create overlay canvas
    overlay = np.zeros_like(ref_frame)

    # Draw reference pose in green
    ref_results = pose.process(cv2.cvtColor(ref_frame, cv2.COLOR_BGR2RGB))
    if ref_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            overlay,
            ref_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
        )

    # Draw performance pose in blue
    perf_results = pose.process(cv2.cvtColor(perf_frame, cv2.COLOR_BGR2RGB))
    if perf_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            overlay,
            perf_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )

    # Highlight worst joint in red
    joint_tip = ""
    if deviation_score is not None and worst_joint_index is not None and perf_landmarks is not None:
        x, y = int(perf_landmarks[worst_joint_index][0]), int(perf_landmarks[worst_joint_index][1])
        cv2.circle(overlay, (x, y), 10, (0, 0, 255), -1)
        joint_tip = f"Check your {joint_names[worst_joint_index]} alignment."

    # Add feedback text
    if deviation_score is not None:
        feedback = get_feedback(deviation_score)
        cv2.putText(overlay, f'Deviation Score: {deviation_score:.2f}', (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(overlay, feedback, (30, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(overlay, joint_tip, (30, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Combine all three views
    combined = np.hstack((ref_frame, perf_frame, overlay))
    cv2.imshow('Reference | Performance | Merged Feedback', combined)

    # Exit on 'q' key
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

# Cleanup
ref_cap.release()
perf_cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.savefig("score_trend.png")