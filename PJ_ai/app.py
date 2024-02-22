from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
app = Flask(__name__)

# โหลดข้อมูล: ไฟล์ CSV
data = pd.read_csv('Obesity Classification.csv')

# ลบข้อมูลที่ไม่จำเป็นในการทำ model
data = data.drop('ID', axis=1)
data = data.drop('Gender', axis=1)
data = data.drop('Age', axis=1)
data = data.drop('BMI', axis=1)

#เลือก features และ target variable โดยกำหนด X เป็น features (ทุกคอลัมน์ยกเว้น 'Label') และ y เป็น target variable ('Label')
X = data.drop('Label', axis=1)
y = data['Label']

# ทดสอบโมเดลด้วย Random Forest Classifier
RF_clf = RandomForestClassifier()
RF_clf.fit(X, y)

# ทำการคำนวณค่า BMI จาก ส่วนสูง และ น้ำหนัก โดยมีสูตรเป็น น้ำหนัก / ส่วนสูง(เมตร)ยกกำลัง 2
def cal_bmi(height, weight):
    return weight / ((height / 100) ** 2)

# ทำการเปรียบเทียบค่า BMI โดยการจำแนกประเภทน้ำหนัก
def classify_weight(bmi):
    if bmi < 18.5: # BMI ตำกว่า 18.5 น้ำหนักน้อยเกินไป (Underweight)
        return 'Underweight','Underweight.jpg' 
    elif bmi < 24.9: # BMI 18.5-24.9 น้ำหนักปกติ (Normal Weight)
        return 'Normal Weight','Normal.jpg'
    elif bmi < 29.9: # BMI 24.9-29.9 น้ำหนักเกิน (Overweight)
        return 'Overweight','Overweight.jpg'
    else: # BMI มากกว่า 29.9 อ้วน (Obese)
        return 'Obese','Obese.jpg'

# ใช้ Flask เป็น root path โดยส่งไปยัง home.html 
@app.route('/')
def home():
    return render_template('home.html')
# ใช้ Flask สร้าง api เพื่อส่งข้อมูลการคำนวณ BMI ไปยัง path ที่ชื่อว่า /calculate_bmi
@app.route('/calculate_bmi', methods=['POST'])
def calculate(): # ทำการนำค่าที่ input เข้ามาเพื่อคำนวณหา BMI
    height = float(request.form['height']) 
    weight = float(request.form['weight'])
    bmi = cal_bmi(height, weight)
    weight_category = classify_weight(bmi)

    return render_template('result.html', bmi=bmi, weight_category=weight_category)
if __name__ == '__main__':
    app.run(debug=True)

