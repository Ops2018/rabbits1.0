from flask import Flask,render_template,request
import MySQLdb as mysql
import json
import os

#conn = mysql.connect(user='root', passwd='oracle', host='localhost', db='ops_info')
#conn.autocommit(True)
app = Flask(__name__)

#index page
@app.route('/',methods=['POST','GET'])
def  index():
	return render_template('index.html')

@app.route('/wrong')
def wrong():
	return render_template('wrong_passwd.html')
#login page
@app.route('/login',methods=['POST','GET'])
def login():
	conn = mysql.connect(user='root', passwd='oracle', host='localhost', db='ops_info')
        conn.autocommit(True)
        cur = conn.cursor()
	if request.method == 'POST':
		username = request.form['username']
		passwd = request.form['userpwd']
		sql = "select password from auth where username='" + username +"'"
		cur.execute(sql)
		arr = []
		for i in cur.fetchall():
		        arr.append(i[0])
		os.system("touch /root/1.txt")
		if arr[0] == passwd:
			return render_template('index.html')
		else:
			return render_template('wrong_passwd.html')
		
		return render_template('wrong_passwd.html')
#                username = request.form['username']
#                passwd = request.form['userpwd']
#                sql = 'select password from auth where ' + username + "=" + username
#                cur.execute(sql)
#                arr = []
#                for i in cur.fetchall():
#                        arr.append(i[0])
#                if arr[0] == passwd:
#                        if request.form['login'] == 'ok':
#                                return redirect(url_for('app.index'))
#                        else:
#                                print("wrong passwd")
#                                return redirect(url_for('app.wrong'))
	return render_template('login.html')
#memory_monitor page
@app.route('/memory_monitor')
def memory_monitor():
	return render_template('memory_monitor.html')
#cpu_monitor page
@app.route('/cpu_monitor')
def cpu_monitor():
	return render_template('cpu_monitor.html')

#cpu_behavior page
@app.route('/cpu_behavior')
def cpu_behavior():
	behavior = open('control_files/cpu_behavior', 'w+')
	cpu_autotunning = open('control_files/cpu_autotunning','w+')
	cpu_threshold = open("control_files/cpu_threshold", "w+")
	cpu_threshold.writelines("#this file defines the threshold(%) of the memory. Whenever the mem_used data hit the threshold, it will generate a warning message.\n")
        cpu_threshold.writelines("#You can define the behavior whenever the mem_used data hit the threshold by editing the mem_behavior file.\n")
	if request.method =='POST':
		if request.form['saving_behavior'] == "save":
			command = request.form['orders']
                        threshold = request.form['threshold']
			cpu_threshold.writelines(threshold)
                        behavior.writelines(str(command))
			cpu_autotunning.writelines("0")
	cpu_autotunning.close()
        cpu_threshold.close()
        behavior.close()
        return render_template('cpu_behavior_define.html')

#mem_behavior page
@app.route('/mem_behavior',methods=['POST','GET'])
def memory_behavior():
	behavior = open('control_files/mem_behavior', 'w+')
	mem_autotunning = open('control_files/mem_autotunning','w+')
	mem_threshold = open("control_files/mem_threshold", "w+")
	mem_threshold.writelines("#this file defines the threshold(%) of the memory. Whenever the mem_used data hit the threshold, it will generate a warning message.\n")
	mem_threshold.writelines("#You can define the behavior whenever the mem_used data hit the threshold by editing the mem_behavior file.\n")
	if request.method =='POST':
                if request.form['saving_behavior'] == "save":
                        command = request.form['orders']
			threshold = request.form['threshold']
			#if threshold != "":
			#	mem_threshold.writelines(threshold)
			#else:
			mem_threshold.writelines(threshold)
                        behavior.writelines(str(command))
			#if request.form['autotunning'] == 'ok':
			#	mem_autotunning.writelines("1")
			#else:
			mem_autotunning.writelines("0")
	mem_autotunning.close()
	mem_threshold.close()
	behavior.close()
	return render_template('mem_behavior_define.html')

#memory one_click tunning
@app.route('/tunning', methods=['POST','GET'])
def tunning():
	behavior = open('control_files/mem_behavior', 'r')
	if request.method =='POST':
		if request.form['one_click_tunning'] == "one_click_tunning":
			commands = behavior.readlines()
			for com in commands:
				os.system(com.split('\n')[0])
	behavior.close()
	return render_template('memory_monitor.html')


tmp_time = 0
tmp_time_cpu = 0
#####below is the debug page###########
@app.route('/data')
def data():
	conn = mysql.connect(user='root', passwd='oracle', host='localhost', db='ops_info')
	conn.autocommit(True)
	cur = conn.cursor()
	global tmp_time
	if tmp_time>0:
		sql = 'select * from memory where time>%s' % (tmp_time/1000)
	else:
		sql = 'select * from memory'
	cur.execute(sql)
	arr = []
	for i in cur.fetchall():
		arr.append([i[1]*1000, i[0]])
	if len(arr)>0:
		tmp_time = arr[-1][0]
	return json.dumps(arr)
	
@app.route('/cpu_data')
def cpu_data():
	conn = mysql.connect(user='root', passwd='oracle', host='localhost', db='ops_info')
	conn.autocommit(True)
	cur = conn.cursor()
	global tmp_time_cpu
	if tmp_time_cpu>0:
                sql = 'select * from cpu where time>%s' % (tmp_time_cpu/1000)
	else:
		sql = 'select * from cpu'
	cur.execute(sql)
        arr = []
        for i in cur.fetchall():
                arr.append([i[1]*1000, i[0]])
        if len(arr)>0:
                tmp_time_cpu = arr[-1][0]
        return json.dumps(arr)

if __name__=="__main__":
	app.run(host="0.0.0.0", port=9092, debug=True)

