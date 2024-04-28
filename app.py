from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', selected_date='', no_data=False)

@app.route('/detection', methods=['POST'])
def facedetect():
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    conn = sqlite3.connect('detectface.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, time FROM facedetect WHERE date = ?", (formatted_date,))
    face_data = cursor.fetchall()

    conn.close()

    if not face_data:
        return render_template('index.html', selected_date=selected_date, no_data=True)
    
    return render_template('index.html', selected_date=selected_date, face_data=face_data)

if __name__ == '__main__':
    app.run(debug=True)
