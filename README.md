Drone Detection using YOLOv5
In this project, I collected images of drones from the internet, annotated them, and trained a YOLOv5 object detection model to detect drones in images. The files in this repository are Drone_detection.ipynb, GUI application.py, and Drone_Detection.pt model.

Prerequisites
Python 3
PyTorch
OpenCV
Pillow
Matplotlib
NumPy
Collecting and Annotating Data
I collected images of drones from the internet and annotated them using LabelImg. The annotated images are in the data/images directory.

Training the Model
I used the YOLOv5 object detection model and trained it on the annotated drone images using the Drone_detection.ipynb notebook. The trained model is saved as Drone_Detection.pt.

Running the GUI Application
The GUI application GUI application.py allows you to select an image and detect drones in it using the trained model. To run the application, run GUI application.py using Python. The application will open a window where you can select an image to detect drones in. The detected drones will be highlighted in the image.

Acknowledgments
This project was inspired by The AI Guy's YouTube tutorial on Object Detection with YOLOv5.
