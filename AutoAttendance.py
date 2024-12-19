# # WARNING: DEPRECATED
# # WARNING: DEPRECATED
# # WARNING: DEPRECATED
# # WARNING: DEPRECATED
# # WARNING: DEPRECATED
# # WARNING: DEPRECATED
# # WARNING: DEPRECATED
# # WARNING: DEPRECATED





# import face_recognition
# import cv2
# import numpy as np
# import os
# from datetime import datetime, timedelta
# import pandas as pd
# import argparse
# import sys
#
#
#
# def parse_arguments():
#     parser = argparse.ArgumentParser(
#         description="Real-time Face Recognition with OpenCV and face_recognition",
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter
#     )
#
#     parser.add_argument(
#         '--known_people_dir',
#         type=str,
#         default='robotics_people',
#         help='Directory containing images of known individuals.'
#     )
#
#     parser.add_argument(
#         '--scale_factor',
#         type=float,
#         default=0.75,
#         help='Scaling factor for frame resizing (e.g., 0.5 for 50%).'
#     )
#
#     parser.add_argument(
#         '--log_file',
#         type=str,
#         default='face_recognition_log.csv',
#         help='Path to the CSV file for logging recognized faces.'
#     )
#
#     parser.add_argument(
#         '--camera_index',
#         type=int,
#         default=1,
#         help='Index of the webcam to use (0 is default).'
#     )
#
#     parser.add_argument(
#         '--upsample_times',
#         type=int,
#         default=2,
#         help='Number of times to upsample the image when detecting faces.'
#     )
#
#     parser.add_argument(
#         '--no_display',
#         action='store_true',
#         help='Run the script without displaying the video window.'
#     )
#
#     parser.add_argument(
#         '--verbose',
#         action='store_true',
#         help='Enable verbose output for debugging.'
#     )
#
#     return parser.parse_args()
#
#
# def load_known_faces(known_people_dir, verbose=False):
#     known_face_encodings = []
#     known_face_names = []
#
#     # Verify that the directory exists
#     if not os.path.isdir(known_people_dir):
#         raise ValueError(f"The directory '{known_people_dir}' does not exist. Please check the path.")
#
#     if verbose:
#         print(f"Loading known faces from directory: {known_people_dir}")
#
#     for filename in os.listdir(known_people_dir):
#         if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#             image_path = os.path.join(known_people_dir, filename)
#             if verbose:
#                 print(f"Loading image file: {image_path}")
#             try:
#                 image = face_recognition.load_image_file(image_path)
#                 face_encodings = face_recognition.face_encodings(image)
#                 if face_encodings:
#                     known_face_encodings.append(face_encodings[0])
#                     name = os.path.splitext(filename)[0]
#                     known_face_names.append(name)
#                     if verbose:
#                         print(f"Loaded and encoded face for: {name}")
#                 else:
#                     print(f"Warning: No faces found in image {filename}.", file=sys.stderr)
#             except Exception as e:
#                 print(f"Error processing file {filename}: {e}", file=sys.stderr)
#
#     if verbose:
#         print(f"Total known faces loaded: {len(known_face_names)}")
#
#     return known_face_encodings, known_face_names
#
#
# def has_logged_today(name, log_file, verbose=False):
#     if os.path.isfile(log_file):
#         try:
#             df = pd.read_csv(log_file)
#             today = datetime.now().strftime("%Y-%m-%d")
#             logged = not df[(df['Name'] == name) & (df['Date'] == today)].empty
#             if verbose:
#                 print(f"Checked log for {name} on {today}: {'Found' if logged else 'Not found'}")
#             return logged
#         except Exception as e:
#             print(f"Error reading log file: {e}", file=sys.stderr)
#             return False
#     return False
#
#
# def main():
#     args = parse_arguments()
#
#     # Load known faces
#     known_face_encodings, known_face_names = load_known_faces(args.known_people_dir, verbose=args.verbose)
#
#     if not known_face_encodings:
#         print("No known faces loaded. Exiting...", file=sys.stderr)
#         sys.exit(1)
#
#     # Initialize variables
#     face_names = []
#     process_this_frame = True
#     detection_start_times = {}
#
#     # Open a connection to the webcam
#     if args.verbose:
#         print("Attempting to access the webcam...")
#     video_capture = cv2.VideoCapture(args.camera_index)
#     if not video_capture.isOpened():
#         print("Could not open webcam. Please ensure that a webcam is connected and accessible.", file=sys.stderr)
#         sys.exit(1)
#
#     if args.verbose:
#         print("Webcam successfully accessed.")
#
#     # Create or open the CSV file for logging
#     log_file = args.log_file
#     if not os.path.isfile(log_file):
#         try:
#             with open(log_file, 'w') as f:
#                 f.write('Name,Date,Time\n')
#             if args.verbose:
#                 print(f"Created new log file: {log_file}")
#         except Exception as e:
#             print(f"Error creating log file: {e}", file=sys.stderr)
#             sys.exit(1)
#     else:
#         if args.verbose:
#             print(f"Using existing log file: {log_file}")
#
#     print("Starting face recognition. Press 'q' to quit.")
#
#     while True:
#         # Grab a single frame of video
#         ret, frame = video_capture.read()
#
#         if not ret:
#             print("Failed to grab frame from webcam. Exiting...", file=sys.stderr)
#             break
#
#         # Resize frame for faster processing using the scaling factor
#         small_frame = cv2.resize(frame, (0, 0), fx=args.scale_factor, fy=args.scale_factor)
#         # Convert the image from BGR color (which OpenCV uses) to RGB color
#         rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
#
#         if process_this_frame:
#             # Find all the faces and face encodings in the current frame
#             face_locations = face_recognition.face_locations(rgb_small_frame,
#                                                              number_of_times_to_upsample=args.upsample_times)
#             face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#
#             face_names = []
#             for face_encoding in face_encodings:
#                 # See if the face matches any of the known faces
#                 matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#                 name = "Unknown"
#
#                 # Use the known face with the smallest distance to the new face
#                 face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)
#                 if matches[best_match_index]:
#                     name = known_face_names[best_match_index]
#
#                 face_names.append(name)
#
#                 # Process known faces
#                 if name != "Unknown":
#                     now = datetime.now()
#                     if name in detection_start_times:
#                         # Check if the face has been recognized for at least 1 second
#                         if now - detection_start_times[name] >= timedelta(seconds=1):
#                             # Log the recognized face with date and time if not already logged today
#                             if not has_logged_today(name, log_file, verbose=args.verbose):
#                                 date_str = now.strftime("%Y-%m-%d")
#                                 time_str = now.strftime("%H:%M:%S")
#                                 try:
#                                     with open(log_file, 'a') as f:
#                                         f.write(f'{name},{date_str},{time_str}\n')
#                                     print(f"Logged recognition of {name} at {date_str} {time_str}.")
#                                     if args.verbose:
#                                         print(f"Successfully logged {name}.")
#                                 except Exception as e:
#                                     print(f"Failed to log recognition for {name}: {e}", file=sys.stderr)
#                             # Remove the name from the dictionary to prevent re-logging
#                             del detection_start_times[name]
#                             if args.verbose:
#                                 print(f"Removed {name} from detection_start_times after logging.")
#                     else:
#                         # Record the time when the face was first recognized
#                         detection_start_times[name] = now
#                         if args.verbose:
#                             print(f"Detected {name}. Recording detection start time.")
#                 else:
#                     # Remove "Unknown" entries from the dictionary
#                     if name in detection_start_times:
#                         del detection_start_times[name]
#                         if args.verbose:
#                             print("Removed 'Unknown' from detection_start_times if present.")
#
#         process_this_frame = not process_this_frame
#
#         # Display the results
#         for (top, right, bottom, left), name in zip(face_locations, face_names):
#             # Scale back up face locations since the frame was resized
#             # Using the SCALE_FACTOR variable for consistency
#             top = int(top / args.scale_factor)
#             right = int(right / args.scale_factor)
#             bottom = int(bottom / args.scale_factor)
#             left = int(left / args.scale_factor)
#
#             # Choose color based on recognition
#             if name == "Unknown":
#                 color = (0, 0, 255)  # Red for unknown
#             else:
#                 color = (0, 255, 0)  # Green for known
#
#             # Draw a box around the face
#             cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#
#             # Draw a label with a name below the face
#             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#
#             # Optional: Display face coordinates
#             # Uncomment the following lines to show coordinates
#             # coord_text = f"({left}, {top})"
#             # cv2.putText(frame, coord_text, (left, top - 10), font, 0.5, (255, 255, 255), 1)
#
#         # Display the resulting image if not in no_display mode
#         if not args.no_display:
#             cv2.imshow('Video', frame)
#
#         # Hit 'q' on the keyboard to quit!
#         if not args.no_display and (cv2.waitKey(1) & 0xFF == ord('q')):
#             print("Quit signal received. Exiting...")
#             break
#
#     # Release handle to the webcam
#     video_capture.release()
#     cv2.destroyAllWindows()
#     if args.verbose:
#         print("Webcam released and all windows closed.")
#     print("Face recognition terminated gracefully.")
#
#
# if __name__ == "__main__":
#     main()
