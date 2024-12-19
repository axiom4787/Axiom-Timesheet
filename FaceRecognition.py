import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime, timedelta
import pandas as pd
import argparse
import sys
import logging

# WARNING: DO NOT UPLOAD PICTURES OF MEMBERS TO GITHUB

# Devlogs:
#
# This script logs to csv file
# Either directly implement sheets api or grab from the csv file.
#
# TODO: Implement the sheets api
# TODO: Implement the checkin, checkout, add_time functions
# TODO: Implement the update_total_time function

# This script is based on the face_recognition library by Adam Geitgey
# Run this script to start the face recognition program.
# The program will grab images from robotics_people folder and upload them to the AI model
# The AI model will then recognize the faces and log them to a csv file

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Real-time Face Recognition with OpenCV and face_recognition",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--known_people_dir',
        type=str,
        default='robotics_people',
        help='Directory containing images of known individuals.'
    )

    parser.add_argument(
        '--scale_factor',
        type=float,
        default=1.0,
        help='Scaling factor for frame resizing (e.g., 0.5 for 50%).'
    )

    parser.add_argument(
        '--log_file',
        type=str,
        default='face_recognition_log.csv',
        help='Path to the CSV file for logging recognized faces.'
    )

    parser.add_argument(
        '--camera_index',
        type=int,
        default=1,
        help='Index of the webcam to use (0 is default).'
    )

    parser.add_argument(
        '--upsample_times',
        type=int,
        default=2,
        help='Number of times to upsample the image when detecting faces.'
    )

    parser.add_argument(
        '--no_display',
        action='store_true',
        help='Run the script without displaying the video window.'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output for debugging purposes.'
    )

    return parser.parse_args()


def setup_logging(verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def load_known_faces(known_people_dir):
    known_face_encodings = []
    known_face_names = []

    # Verify that the directory exists
    if not os.path.isdir(known_people_dir):
        logging.error(f"The directory '{known_people_dir}' does not exist. Please check the path.")
        sys.exit(1)

    logging.info(f"Loading known faces from directory: {known_people_dir}")

    for filename in os.listdir(known_people_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(known_people_dir, filename)
            logging.debug(f"Loading image file: {image_path}")
            try:
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    known_face_encodings.append(face_encodings[0])
                    name = os.path.splitext(filename)[0]
                    known_face_names.append(name)
                    logging.info(f"Loaded and encoded face for: {name}")
                else:
                    logging.warning(f"No faces found in image {filename}.")
            except Exception as e:
                logging.error(f"Error processing file {filename}: {e}")

    logging.info(f"Total known faces loaded: {len(known_face_names)}")
    return known_face_encodings, known_face_names


def initialize_log(log_file):
    logged_names_today = set()
    today_str = datetime.now().strftime("%Y-%m-%d")

    if os.path.isfile(log_file):
        try:
            df = pd.read_csv(log_file)
            # Filter entries for today
            today_entries = df[df['Date'] == today_str]
            logged_names_today = set(today_entries['Name'].tolist())
            logging.info(f"Loaded {len(logged_names_today)} logged entries for today.")
        except Exception as e:
            logging.error(f"Error reading log file: {e}")
            sys.exit(1)
    else:
        # Create the CSV file with headers if it doesn't exist
        try:
            with open(log_file, 'w') as f:
                f.write('Name,Date,Time\n')
            logging.info(f"Created new log file: {log_file}")
        except Exception as e:
            logging.error(f"Error creating log file: {e}")
            sys.exit(1)

    return logged_names_today


def log_recognition(name, log_file):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    try:
        with open(log_file, 'a') as f:
            f.write(f'{name},{date_str},{time_str}\n')
        logging.info(f"Logged recognition of {name} at {date_str} {time_str}.")
    except Exception as e:
        logging.error(f"Failed to log recognition for {name}: {e}")


def main():
    args = parse_arguments()
    setup_logging(args.verbose)

    # Load known faces
    known_face_encodings, known_face_names = load_known_faces(args.known_people_dir)

    if not known_face_encodings:
        logging.error("No known faces loaded. Exiting...")
        sys.exit(1)

    # Initialize logged names for today
    logged_names_today = initialize_log(args.log_file)

    # Initialize variables
    face_names = []
    process_this_frame = True
    detection_start_times = {}

    # Open a connection to the webcam
    logging.info(f"Attempting to access the webcam with index {args.camera_index}...")
    video_capture = cv2.VideoCapture(args.camera_index)
    if not video_capture.isOpened():
        logging.error("Could not open webcam. Please ensure that a webcam is connected and accessible.")
        sys.exit(1)
    logging.info("Webcam successfully accessed.")

    logging.info("Starting face recognition. Press 'q' to quit.")

    try:
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            if not ret:
                logging.warning("Failed to grab frame from webcam. Exiting...")
                break

            # Resize frame for faster processing using the scaling factor
            if args.scale_factor != 1.0:
                small_frame = cv2.resize(frame, (0, 0), fx=args.scale_factor, fy=args.scale_factor)
            else:
                small_frame = frame.copy()
            # Convert the image from BGR color (which OpenCV uses) to RGB color
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            if process_this_frame:
                # Find all the faces and face encodings in the current frame
                face_locations = face_recognition.face_locations(rgb_small_frame,
                                                                 number_of_times_to_upsample=args.upsample_times)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face matches any of the known faces
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # Use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

                    # Process known faces
                    if name != "Unknown":
                        now = datetime.now()
                        if name in detection_start_times:
                            # Check if the face has been recognized for at least 1 second
                            if now - detection_start_times[name] >= timedelta(seconds=1):
                                # Log the recognized face with date and time if not already logged today
                                if name not in logged_names_today:
                                    log_recognition(name, args.log_file)
                                    logged_names_today.add(name)
                                # Remove the name from the dictionary to prevent re-logging
                                del detection_start_times[name]
                        else:
                            # Record the time when the face was first recognized
                            detection_start_times[name] = now
                            logging.debug(f"Detected {name}. Recording detection start time.")
                    else:
                        # Remove "Unknown" entries from the dictionary
                        if name in detection_start_times:
                            del detection_start_times[name]
                            logging.debug("Removed 'Unknown' from detection_start_times if present.")

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame was resized
                if args.scale_factor != 1.0:
                    top = int(top / args.scale_factor)
                    right = int(right / args.scale_factor)
                    bottom = int(bottom / args.scale_factor)
                    left = int(left / args.scale_factor)

                # Choose color based on recognition
                if name == "Unknown":
                    color = (0, 0, 255)  # Red for unknown
                else:
                    color = (0, 255, 0)  # Green for known

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image if not in no_display mode
            if not args.no_display:
                cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if not args.no_display and (cv2.waitKey(1) & 0xFF == ord('q')):
                logging.info("Quit signal received. Exiting...")
                break

    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Exiting...")

    finally:
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        logging.info("Webcam released and all windows closed.")
        logging.info("Face recognition terminated gracefully.")


if __name__ == "__main__":
    main()
