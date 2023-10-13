from app import app, scheduler

# pip freeze > requirements.txt
# When you gonna start, pip install -r requirements.txt

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)