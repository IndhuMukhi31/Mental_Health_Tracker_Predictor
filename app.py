from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Make zip and enumerate available in Jinja templates
app.jinja_env.globals.update(zip=zip, enumerate=enumerate)

# 15 Simple Mental Health Questions
questions = [
    {"q": "Do you feel anxious frequently?", "options": ["Yes", "No"], "scores": [2, 0]},
    {"q": "How would you rate your sleep quality?", "options": ["Excellent", "Good", "Poor", "Very Poor"], "scores": [0, 1, 2, 3]},
    {"q": "Do you often overthink?", "options": ["Yes", "No"], "scores": [2, 0]},
    {"q": "How often do you feel sad?", "options": ["Never", "Sometimes", "Often", "Always"], "scores": [0, 1, 2, 3]},
    {"q": "Do you enjoy spending time with others?", "options": ["Always", "Sometimes", "Rarely", "Never"], "scores": [0, 1, 2, 3]},
    {"q": "Do you feel tired even after sleeping?", "options": ["Yes", "No"], "scores": [2, 0]},
    {"q": "How motivated do you feel today?", "options": ["Very", "Moderate", "Low", "None"], "scores": [0, 1, 2, 3]},
    {"q": "Do you avoid social interactions?", "options": ["Yes", "No"], "scores": [2, 0]},
    {"q": "Do you struggle to focus?", "options": ["Never", "Sometimes", "Often", "Always"], "scores": [0, 1, 2, 3]},
    {"q": "Do you feel like a burden to others?", "options": ["Yes", "No"], "scores": [3, 0]},
    {"q": "Do you enjoy your daily activities?", "options": ["Yes", "No"], "scores": [0, 2]},
    {"q": "Do you get easily irritated?", "options": ["Never", "Sometimes", "Often", "Always"], "scores": [0, 1, 2, 3]},
    {"q": "Do you feel hopeless?", "options": ["Yes", "No"], "scores": [3, 0]},
    {"q": "Do you fear the future?", "options": ["Never", "Sometimes", "Often", "Always"], "scores": [0, 1, 2, 3]},
    {"q": "Do you feel mentally relaxed today?", "options": ["Yes", "No"], "scores": [0, 2]}
]

# Homepage - Collects name, age, gender
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['age'] = request.form['age']
        session['gender'] = request.form['gender']
        return redirect('/tracker')
    return render_template('index.html')

# Tracker Page - Collect mood, sleep, stress
@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        session['mood'] = request.form['mood']
        session['sleep'] = request.form['sleep']
        session['stress'] = request.form['stress']
        return redirect('/quiz')
    return render_template('tracker.html')

# Quiz Page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session or 'mood' not in session:
        return redirect('/')
    if request.method == 'POST':
        total_score = 0
        for i, q in enumerate(questions):
            ans = request.form.get(f'q{i}')
            if ans:
                total_score += int(ans)
        return render_template('result.html', score=total_score,
                               mood=session['mood'],
                               sleep=session['sleep'],
                               stress=session['stress'],
                               username=session['username'],
                               age=session['age'],
                               gender=session['gender'])
    return render_template('quiz.html', questions=questions)

# Logout Clears Session
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)