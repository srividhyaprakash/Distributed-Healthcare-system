from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__, template_folder='template')

patient_id  = "global_variable"

@app.route('/')
def main_page():
	print("entered here")
	return render_template('main_page.html')

@app.route('/new_user',methods = ['POST', 'GET'])
def new_user():
	if (request.method == 'POST'):
		return render_template("new_user.html")

@app.route('/existing_user',methods = ['POST', 'GET'])
def existing_user():
	if (request.method == 'POST'):
		return render_template("input.html")

@app.route('/success',methods = ['POST', 'GET'])
def success():
	return redirect(url_for('main_page'))

@app.route('/book_appointment',methods = ['POST', 'GET'])
@app.route('/result',methods = ['POST', 'GET'])
def result():
	if (request.method == 'POST'):
		try:
			conn = sql.connect('db_1.0.db')
			print("Opened database successfully")
			username = request.form['uname']
			print("Username is: %s" % username)
			password = request.form['psw']
			print("password is: %s" % password)
			dict_login = {'username':username, 'password' : password}
			print("created the dictionary")
			cur = conn.cursor()
			print("created the cursor")
			cur.execute("select * from login")
			print("executed the query")
			rows = cur.fetchall()
			print("the type of rows is", type(rows))
			print(rows)
			for row in rows:
				print("the row in consideration is", row)
				if row[0] == username and row[2] == password:
					print("username present in the database")
					if(row[0][0] == 'p'):
						return render_template("patient.html", result = row)
					elif (row[0][0] == 'd'):
						return render_template("doctor.html", result = row)
					elif (row[0][0] == 'i'):
						return render_template("insurance.html", result = row)
					elif (row[0][0] == 'a'):
						return render_template("admin.html", result = row)
			print("Username incorrect")
			return redirect(url_for('main_page'))

		except:
			print("error in database connection or access")
		finally:
			print("closing database connection")
			conn.close()

@app.route('/insert_patient_data',methods = ['POST', 'GET'])
def insert_patient_data():
	if request.method == 'POST':
		try:
			conn = sql.connect('db_1.0.db')
			print("Opened database successfully")
			p_id = request.form['id_of_user']			# have username field as uname in html code
			ssn = request.form['ssn_of_user']				# have ssn field as myssn in html code
			password = request.form['psw_of_user']			# have password field as pswd in html code
			name = request.form['name_of_user']			# have password field as pswd in html code
			email_id = request.form['email_of_user']			# have password field as pswd in html code

			print("id Value properly received", p_id)
			cur = conn.cursor()	
			cur.execute("INSERT INTO patient (p_id,p_password,p_name,p_email,p_ssn) VALUES (?,?,?,?,?)",(p_id,password,name,email_id,ssn) )
			cur.execute("INSERT INTO login (health_id,username, password) VALUES (?,?,?)", (p_id,name, password))
			conn.commit()
			print("successfully inserted value in database")
			msg = "Your record has been updated in the database."
		except:
			print("error in database connection or access")
			msg = "error in insert operation"
			conn.rollback()
		finally:
			print("closing connection")
			conn.close()
			return render_template('new_user_success.html', msg = msg)		# go back to patient.html and render with the msg block dynamically


@app.route('/check_insurance',methods = ['POST', 'GET'])
def check_insurance():
	print("Entered the check insurance flask function")
	if (request.method == 'POST'):
		return render_template("check_insurance.html")


@app.route('/check_insurance_result',methods = ['POST', 'GET'])
def check_insurance_result():
	print("Entered the check insurance result flask function")
	if request.method == 'POST':
		try:
			conn = sql.connect('db_1.0.db')
			print("Opened database successfully")
			i_name = request.form['insurance_comp_name']
			print("company name received is", i_name)
			cur = conn.cursor()
			cur.execute("select patient.p_name from patient, insurance where insurance.i_company_name = ? and insurance.i_p_id = patient.p_id", (i_name,))
			print("executed the function successfully")
			rows = cur.fetchall()
			print("fetched all rows")
			print("length of rows is", len(rows))
			print("type of rows is", type(rows))
			# check the type here and print accordingly or append to a list and send that to check_insurance_result.html
		except:
			print("error in database connection or access")
		finally:
			print("closing database connection")
			conn.close()
			return render_template("check_insurance_result.html", result = rows)

@app.route('/scan_report',methods = ['POST', 'GET'])
def scan_report():
	if(request.method == 'POST'):
		print("Python code to send an email should go here")
		fromaddr = "srividhyaprakash029@gmail.com"
		toaddr = "srividhyaprakash029@gmail.com"
		filename = "d4ecb063-7ece-40b5-b92b-a3a1f04ada34-original.jpeg"
		body = "Your scan report has been attached along with this mail. \
				Hope you liked your stay at our hospital."
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "Python scripted email"


		msg.attach(MIMEText(body, 'plain'))


		try:
			attachment = open(filename, 'rb')
			msg_send = "Your scan report has been successfully sent to you!"
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment;filename=%s" % filename)
			msg.attach(part)
			# 'your host address', 'your port number'
			server = smtplib.SMTP('smtp.gmail.com', 587)
			# security function used to protect your password
			server.starttls()

			server.login(fromaddr, "007029svp1") # password should be changed here

			msg = msg.as_string()

			# "my email", "email address to send to", "msg"
			server.sendmail(fromaddr, toaddr, msg)
			server.quit()
		except:
			msg_send = "Sorry, your scan report was not found in the database"

		finally:
			return render_template("scan_report_success.html", msg = msg_send)

@app.route('/update_patient_info', methods = ['GET', 'POST'])
def update_patient_info():
	return render_template('update_patient_info_page.html')

@app.route('/update_patient_email',methods = ['POST', 'GET'])
def update_patient_email():	
	return render_template('update_patient_email.html')


@app.route('/update_patient_email_success',methods = ['POST', 'GET'])
def update_patient_email_success():	
	if request.method == 'POST':
		try:
			conn = sql.connect('db_1.0.db')
			print("Opened database successfully")
			p_id = request.form["id_of_user"]
			email = request.form["email_of_user"]
			cur = conn.cursor()
			print("created the cursor")
			cur.execute("UPDATE patient SET p_email = ? where p_id = ?",(email,p_id))
			conn.commit()
			msg = "Your Email is successfully updated"
		except:
			msg = "Error in updating your Email, login and try again"
		finally:
			return render_template("scan_report_success.html", msg = msg)


@app.route('/update_patient_ssn',methods = ['POST', 'GET'])
def update_patient_ssn():	
	return render_template('update_patient_ssn.html')


@app.route('/update_patient_ssn_success',methods = ['POST', 'GET'])
def update_patient_ssn_success():	
	if request.method == 'POST':
		try:
			conn = sql.connect('db_1.0.db')
			print("Opened database successfully")
			p_id = request.form["id_of_user"]
			ssn = request.form["ssn_of_user"]
			cur = conn.cursor()
			print("created the cursor")
			cur.execute("UPDATE patient SET p_ssn = ? where p_id = ?",(ssn,p_id))
			conn.commit()
			msg = "Your SSN is successfully updated"
		except:
			msg = "Error in updating SSN, login and try again"
		finally:
			return render_template("scan_report_success.html", msg = msg)			

@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    	pass
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # # if user does not select file, browser also
        # # submit a empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('uploaded_file',
        #                             filename=filename))
    return render_template("uploadFile.html")

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)