from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from send_email import sendemail
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:660808@localhost/data_collector'
db = SQLAlchemy(app)

class DataBase(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Float)

    def __init__(self, email, height):
        self.email = email
        self.height = height

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/success', methods=['post'])
def success():
    print(request)
    if request.method == 'POST':
        global file
        file = request.files["file"]
        file.save(secure_filename("uploaded" + file.filename))
        print(1)
        print(request.form)
        email = request.form["useremail"]
        height = request.form["userinput"]
        print(email, height)

        if db.session.query(DataBase).filter(DataBase.email == email).count() == 0:
            input = DataBase(email, height)
            db.session.add(input)
            db.session.commit()
            avereage_height = db.session.query(func.avg(DataBase.height)).scalar()
            count = db.session.query(DataBase.height).count()
            '''.scalar()这个方法与.one_or_none()的效果一样。如果查询到很多结果，抛出sqlalchemy.orm.exc.MultipleResultsFound异常。如果只有一个结果，返回它，没有结果返回None。'''
            print(avereage_height)
            sendemail(email, height, avereage_height, count)
            if file.filename != '':
                return render_template("success.html", btn="download.html")
            else:
                return render_template("success.html", btn="")
        else:
            input = db.session.query(DataBase).filter(DataBase.email == email).first()
            '''input = DataBase.query.filter(DataBase.email == email).first()'''
            print(input.height)
            input.height = height
            db.session.commit()
            avereage_height = db.session.query(func.avg(DataBase.height)).scalar()
            count = db.session.query(DataBase.height).count()
            print(avereage_height)
            sendemail(email, height, avereage_height, count)
            if file.filename != '':
                return render_template("success.html", text="You've already made the submission with the same email address, so we updated your submission", btn="download.html")
            else:
                return render_template("success.html", text="You've already made the submission with the same email address, so we updated your submission", btn="")


@app.route('/download')
def download():
    print(file.filename)
    return send_file("uploaded" + file.filename, as_attachment=True)

if __name__ == "__main__":
    db.create_all()  # 如果数据库表已存在现有数据库中，那么 db.create_all() 不会执行任何更新操作或重建这个表
    app.debug = True
    app.run(debug=True)
    '''gmail password: vzdlalwjdserdfcc'''

