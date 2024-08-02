from flask import Flask, render_template, Response, request, jsonify
from camera import Camera
from face_recognition_model import FaceRecognitionModel
from database import Database

app = Flask(__name__)
camera = Camera()
face_model = FaceRecognitionModel()
db = Database()

@app.route('/')
def index():
    courses = db.get_courses()
    return render_template('index.html', courses=courses)

@app.route('/take_attendance')
def take_attendance():
    course = request.args.get('course')
    date = request.args.get('date')
    return render_template('take_attendance.html', course=course, date=date)

def gen_frames():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    date = request.form['date']
    frame = camera.get_frame(as_numpy=True)
    recognized_students = face_model.recognize_faces(frame)
    for student in recognized_students:
        student_id = student.split('_')[0]  # Extract roll number from the image name
        db.mark_attendance(student_id, date)
    return jsonify(success=True, recognized=recognized_students)

@app.route('/export_csv')
def export_csv():
    csv_data = db.export_to_csv()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=attendance.csv"})

# New route for updating the face recognition model
@app.route('/update_model', methods=['POST'])
def update_model():
    face_model.update_model()
    return jsonify({"success": True, "message": "Face recognition model updated successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)