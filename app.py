
import os

from flask import Flask, flash, render_template, request, url_for, redirect, session
import mysql.connector
from werkzeug.utils import secure_filename

from mpld3 import fig_to_html
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import warnings
warnings.filterwarnings('ignore')
from statsmodels.tsa.arima.model import ARIMA




conn = mysql.connector.connect(
    host="forestock.mysql.pythonanywhere-services.com",
    user="forestock",
    password="adiancar",
    database="forestock$forecast",
    autocommit='true')

app = Flask(__name__)
app.secret_key = "forestock"
app.config['UPLOAD_FOLDER'] = 'uploads'




# @app.route('/register.html', methods=['POST', 'GET'])
# def register():
#     if request.method=='GET':
#         return render_template('register.html')
#     else :
#         fname = request.form['firstname']
#         lname = request.form['lastname']
#         name = fname+" "+lname
#         email = request.form['email']
#         password = request.form['password'].encode('utf-8')
#         confpass = request.form['confpass'].encode('utf-8')

#         if password == confpass:
#             hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

#             query = "INSERT INTO tb_user (nama,email,password) VALUES (%s,%s,%s)"
#             value = (name, email, hash_password)
#             cur = conn.cursor()
#             cur.execute(query, value)
#             # flash('Registered Successfully! \n', 'success')
#             return redirect(url_for('login'))
#         else :
#             print("Password is not same as above! \n")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['password']
        query = "SELECT * FROM tb_admin WHERE username=%s"
        val = (uname,)
        cur = conn.cursor()
        cur.execute(query, val)
        admin = cur.fetchone()
        if admin is not None and len(admin) > 0:
            if (password) == admin[2]:
                session['login'] = True
                session['nama'] = admin [1]
                if admin[1] == "admin":
                    return redirect(url_for('admin'))
                else :
                    return redirect(url_for('main'))
            else :
                flash("Gagal, Email dan Password Tidak Cocok")
                return redirect(url_for('login'))
        else :
            flash("Gagal, User Tidak Ditemukan")
            return redirect(url_for('login'))
    else:
        return render_template("login.html")

@app.route("/inputemiten", methods=['POST', 'GET'])
def inputemiten():
    if request.method == 'GET':
        return render_template('emiten.html')
    else:
        code = request.form['stockscode']
        name = request.form['stocksname']

        query = "INSERT INTO tb_emiten (emt_code,emt_name) VALUES (%s,%s)"
        val = (code, name)
        cur = conn.cursor()
        cur.execute (query, val)

        return redirect(url_for('emiten'))

@app.route("/emiten")
def emiten():
    query = "SELECT * FROM tb_emiten"
    cur = conn.cursor()
    cur.execute(query)
    emiten = cur.fetchall()
    return render_template('admin/pages/emiten.html', data = emiten)

@app.route("/delemtien")
def delemiten():
    sql = "DELETE FROM `tb_emiten` WHERE emt_id=%s"
    val = request.args.get('emtid')
    cur = conn.cursor()
    cur.execute(sql, (val,))
    return redirect(url_for('emiten'))

@app.route("/editemiten", methods=['POST','GET'])
def editemiten():
    cur = conn.cursor()
    if request.method == 'POST':
        id = request.form['id']
        new_code = request.form['stockscode']
        new_name = request.form['stocksname']
        sql = "UPDATE `tb_emiten` SET `emt_code`=%s,`emt_name`=%s WHERE `emt_id`=%s"
        val = (new_code, new_name, id)
        cur.execute(sql, val)

        return redirect(url_for('emiten'))
    else:
        sql = "SELECT * FROM tb_emiten WHERE emt_id=%s"
        val = request.args.get('emtid')
        cur.execute(sql, (val,))
        emt = cur.fetchone()
        id = emt[0]
        code = emt[1]
        name = emt[2]

        return render_template('admin/pages/ed_emiten.html', id=id, code=code, name=name)

@app.route("/user")
def user():
    # if session == True :
        query = "SELECT * FROM tb_user WHERE level != 'admin'"
        cur = conn.cursor()
        cur.execute(query)
        user = cur.fetchall()
        return render_template('admin/pages/user.html', data = user)

    # else :
    #     return render_template('login.html')

@app.route("/status", methods=['POST','GET'])
def status():
    query  = "SELECT * FROM tb_user WHERE user_id = %s"
    val = request.args.get('userid')
    cur = conn.cursor()
    cur.execute(query, (val,))
    user = cur.fetchone()
    # print(user[0])
    # return "test"

    if user[4] == 'active' :
        sql = "UPDATE tb_user SET status = 'inactive' WHERE user_id = %s"
        cur.execute(sql, (user[0],))

        return redirect(url_for('user'))
    else :
        sql = "UPDATE tb_user SET status = 'active' WHERE user_id = %s"
        cur.execute(sql,  (user[0],))
        return redirect(url_for('user'))


###
@app.route("/inputprice")
def iprice():
    # if session == True :
        sql = "SELECT * FROM tb_emiten"
        cur = conn.cursor()
        cur.execute(sql)
        stock = cur.fetchall()
        return render_template('admin/pages/iprice.html', data = stock)

    # else :
    #     return render_template('login.html')

@app.route("/upload", methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        emt_id = request.form['emiten']
        f = request.files['file']
        filename = secure_filename(f.filename)
        name = f.filename
        pathh = "/home/adityayafi/mysite/uploads/"+name
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        sql = "INSERT INTO tb_uploads (emt_id,filename,path) VALUES (%s,%s,%s)"
        val = (emt_id, name, pathh)
        cur = conn.cursor()
        cur.execute(sql, val)
        # print(pathh)
        return redirect(url_for('iprice'))
    else :
        return render_template('admin/pages/iprice.html')




@app.route("/stock")
def stock():
    sql = "SELECT * FROM tb_emiten"
    cur = conn.cursor()
    cur.execute(sql)
    stock = cur.fetchall()
    return render_template('stock.html', data = stock)

@app.route("/test")
def test():
    # print ("test", file=sys.stderr)
    return "Check your console"

@app.route("/admin", methods=['POST', 'GET'])
def admin():
    sql = "SELECT COUNT(*) FROM tb_emiten"
    cur = conn.cursor()
    cur.execute(sql)
    stk = cur.fetchone()
    print(stk[0])
    x = 1

    if x == 1 :
        sql = "SELECT COUNT(*) from tb_uploads"
        cur.execute(sql)
        ups = cur.fetchone()
        return render_template('admin/index.html', stk=stk[0], ups=ups[0])
    else:
        return render_template('admin/index.html', stk=stk[0], ups=ups[0])

@app.route("/")
def main():
    # if session == True :
        return render_template('index.html')
    # else :
    #     return render_template('login.html')

@app.route("/index.html")
def index():
    # if session == True :
        return render_template('index.html')
    # else :
    #     return render_template('login.html')

@app.route("/buttons")
def buttons():
    return render_template('buttons.html')

@app.route("/forgot-password.html")
def forgotpass():
    return render_template('forgot-password.html')

@app.route("/charts.html")
def charts():
    return render_template('charts.html')

@app.route("/ua")
def ua():
    return render_template('utilities-animation.html')

@app.route("/ub")
def ub():
    return render_template('utilities-border.html')

@app.route("/uc")
def uc():
    return render_template('utilities-color.html')

@app.route("/huploads", methods=['POST','GET'])
def huploads():
    if request.method == 'GET':
        sql = "SELECT * FROM tb_uploads WHERE emt_id=%s"
        emtid= request.args.get('emtid')
        val = (emtid)
        cur = conn.cursor()
        cur.execute (sql, (val,))
        emt = cur.fetchall()
        return render_template('admin/pages/huploads.html', data = emt)
    else:
        return redirect(url_for('emiten'))

@app.route("/hudelete", methods=['POST','GET'])
def hudelete():
    if request.method == 'GET':
        sql = "DELETE FROM tb_uploads WHERE uploads_id=%s"
        val = request.args.get('upid')
        cur = conn.cursor()
        cur.execute(sql, val)
        return redirect(url_for('huploads'))
    else:
        return redirect(url_for('huploads'))

@app.route("/blank.html")
def blank():
    return render_template('blank.html')

@app.route("/conf_arima")
def confarima():
    sql = "SELECT * FROM tb_emiten"
    cur = conn.cursor()
    cur.execute(sql)
    arima = cur.fetchall()
    i = 0

    if i == 0:
        sql1 = "SELECT * FROM tb_uploads"
        cur = conn.cursor()
        cur.execute(sql1)
        dataset = cur.fetchall()

    return render_template('admin/pages/arima.html', data = arima, data1 = dataset)

@app.route("/addconf", methods=['POST', 'GET'])
def addconf():
    if request.method == 'POST' :
        emt_id = request.form['emiten']
        uploads_id = request.form['dataset']
        p = request.form['p']
        d = request.form['d']
        q = request.form['q']

        # print(emt_id, uploads_id, p, d, q)
        sql = "INSERT INTO tb_arima (emt_id, uploads_id, p, d, q) VALUES (%s,%s,%s,%s,%s)"
        val = (emt_id, uploads_id, p, d, q)
        cur = conn.cursor()
        cur.execute(sql, val)


        return redirect(url_for('confarima'))
    else :
        return redirect(url_for('confarima'))

@app.route("/hprice", methods=['POST', 'GET'])
def hprice():
    sql = "SELECT * FROM tb_emiten"
    cur = conn.cursor()
    cur.execute(sql)
    stock = cur.fetchall()

    if request.method == 'POST' :
        emt_id = request.form['emiten']
        sql = "SELECT * FROM tb_uploads WHERE emt_id = %s"
        val = (emt_id)
        cur.execute (sql, (val,))
        emt = cur.fetchone()
        print(emt[2])
        with open(emt[3]) as file :
            return render_template('admin/pages/hprice.html', data = stock, data1 = file)
    else :
        return render_template('admin/pages/hprice.html', data = stock)


@app.route("/history", methods=['POST', 'GET'])
def history():

    if request.method == 'GET':
        sql = "SELECT * FROM tb_uploads WHERE emt_id=%s"
        emtid= request.args.get('emtid')
        val = (emtid)
        cur = conn.cursor()
        cur.execute(sql, (val,))
        emt = cur.fetchone()

        with open(emt[3]) as file:
            return render_template('history.html', data = file)
    else:
        return redirect(url_for('stock'))

@app.route("/forecast", methods=['POST','GET'])
def forecast():
    if request.method == 'GET':
        sql = "SELECT tb_emiten.emt_name, tb_uploads.filename, tb_uploads.path, tb_arima.p, tb_arima.d, tb_arima.q FROM tb_emiten, tb_uploads, tb_arima WHERE tb_emiten.emt_id=tb_uploads.emt_id AND tb_emiten.emt_id=tb_arima.emt_id AND tb_emiten.emt_id=%s"
        emtid = request.args.get('emtid')
        val = (emtid)
        cur = conn.cursor()
        cur.execute(sql, (val,))
        emt = cur.fetchone()
        name = emt[0]
        filename = emt[1]
        path = emt[2]
        p = emt[3]
        d = emt[4]
        q = emt[5]

        # print(p,d,q)

        ###READ DATA###
        df = pd.read_csv(path, index_col='Date', parse_dates=True)
        df = df.dropna()
        # print('Shape of Data', df.shape)
        # df.head()
        # df['Close'].plot(figsize=(12,5))

        ###SPLIT DATA
        train = df[0:int(len(df)*0.8)]
        test = df[int(len(df)*0.8):]

        model = ARIMA(train['Close'], order=(p,d,q), trend='t')
        fitted = model.fit()
        fitted.summary()

        start = len(train)
        end = len(train)+len(test)-1

        # if d == 0:
        #     pred = fitted.predict(start=start, end=end)
        #     pred.index = df.index[start:end+1]
        # else:
        #     pred = fitted.predict(start=start, end=end, typ='levels')
        #     pred.index = df.index[start:end+1]


        pred = fitted.forecast(len(test))
        pred.index = df.index[start:end+1]

        mape = np.mean(np.abs(pred - test['Close'])/np.abs(test['Close']))*100
        mape = "{:.2f}".format(mape)
        pred = round(pred,2)

        # Forecast using 95% confidence interval
        # fc, se, conf = fitted.forecast(50, alpha=0.05)

        # Make as pandas series
        # fc_series = pd.Series(fc, index=test.index)
        # lower_series = pd.Series(conf[:, 0], index=test.index)
        # upper_series = pd.Series(conf[:, 1], index=test.index)

        # Plot
        plt.figure(figsize=(12,5), dpi=100)
        # train['Close'].plot(legend=True, label='Train')
        # pred.plot(legend=True, label='Forecast')
        # test['Close'].plot(legend=True, label='Test')
        plt.plot(train['Close'], label='training')
        plt.plot(test['Close'], label='actual')
        plt.plot(pred, label='forecast')
        plt.title('Forecast vs Actuals : '+ name)
        plt.legend(loc='upper left', fontsize=8)
        plt.savefig('/home/forestock/mysite/static/plot/'+filename+'.png')
        # plt.show()
        return render_template('forecast.html', pred = pred, filename=filename, name=name, emtid=emtid, mape=mape)
    else:
        return render_template('forecast.html')


@app.route("/futureforecast", methods=['POST','GET'])
def futureforecast():

    if request.method == 'POST':
        n_periods = request.form['n']
        sql = "SELECT tb_emiten.emt_name, tb_uploads.filename, tb_uploads.path, tb_arima.p, tb_arima.d, tb_arima.q FROM tb_emiten, tb_uploads, tb_arima WHERE tb_emiten.emt_id=tb_uploads.emt_id AND tb_emiten.emt_id=tb_arima.emt_id AND tb_emiten.emt_id=%s"
        emtid = request.form['emtid']
        val = (emtid)
        cur = conn.cursor()
        cur.execute(sql, (val,))
        emt = cur.fetchone()
        name = emt[0]
        filename = emt[1]
        path = emt[2]
        p = emt[3]
        d = emt[4]
        q = emt[5]

        ### READ DATA ###
        df = pd.read_csv(path, parse_dates=True)
        ### DATA CLEANING ###
        df = df.dropna()
        ### DATA SELECTION ###
        ### SPLIT DATA ###
        # train = df[0:int(len(df)*0.8)]
        # test = df[int(len(df)*0.8):]

        model = ARIMA(df['Close'], order=(p,d,q), trend='t')
        fitted = model.fit()
        # fitted.summary()

        # start = len(df)
        # end = len(df)+int(n)-1
        # if d == 0:
        #     pred = fitted.predict(start=start, end=end)
        # else:
        #     pred = fitted.predict(start=start, end=end, typ='levels')
        # print(pred)

        pred = fitted.forecast(steps=int(n_periods))
        pred = round(pred,2)


        # Forecast using 95% confidence interval
        # fc, se, conf = fitted.forecast(50, alpha=0.05)

        # Make as pandas series
        # fc_series = pd.Series(fc, index=test.index)
        # lower_series = pd.Series(conf[:, 0], index=test.index)
        # upper_series = pd.Series(conf[:, 1], index=test.index)

        # Plot Forecast
        pltt = plt.figure(figsize=(12,5), dpi=100)
        plt.plot(pred, label='Forecast')
        plt.plot(df['Close'], label='History')
        plt.legend(loc='upper left', fontsize=8)

        # Plot
        # plt.figure(figsize=(12,5), dpi=100)
        # df['Close'].plot(legend=True, label='Actual')
        # pred.plot(legend=True, label='Forecast')

        plt.title('Forecast vs Actuals : '+ name)
        # plt.savefig('/home/forestock/mysite/static/plot/future'+filename+'.png')
        plot=fig_to_html(pltt)
        return render_template('futureforecast.html', pred = pred, name = name, filename = filename, emtid = emtid, graph = plot)

    return render_template('futureforecast.html')


if __name__ == "__main__":
    app.run(debug = True)

