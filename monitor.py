import time
import MySQLdb as mysql
import os
import psutil

##connect database
db = mysql.connect(user="root", passwd="oracle", db="ops_info", host="localhost")
db.autocommit(True)
cur = db.cursor()
##get mem_use and put the data into the database
def getmem():
	mem_autotunning = open('control_files/mem_autotunning', 'r')
	log_file = open("log/log", "a+")
	mem_threshold = open("control_files/mem_threshold", "r")
        mem_behavior = open("control_files/mem_behavior", "r")
	f = open('/proc/meminfo', 'r')
	
	total = int(f.readline().split()[1].split()[0])
        free = int(f.readline().split()[1].split()[0])
        f.readline()
        buffer = int(f.readline().split()[1].split()[0])
        cache = int(f.readline().split()[1].split()[0])
        mem_used = total - free - cache - buffer
        t = int(time.time())
        sql = 'insert into memory(memory,time) values(%s,%s)'%(mem_used/1024, t)        
	cur.execute(sql)
        print(sql)
        print(mem_used/1024)
	print("ok")
	
	#threshold alarm
	mem_threshold.readline()
	mem_threshold.readline()
	threshold = mem_threshold.readline().split("\n")[0]
	if mem_used/total*100 >= eval(threshold):
		print("warning!!!")
		log_file.writelines("[memory]hitting the threshold!may generate OOM! [current value]"+str(mem_used/total*100)+" [threshold%]"+threshold+"\n")
	
	#autotunning according the behavior
	if str(mem_autotunning.readlines()[0].split('\n')[0]) == '1':
		commands = mem_behavior.readlines()
		for i in commands:
			os.system(i.split('\n')[0])
	
	mem_behavior.close()
	mem_autotunning.close()
	log_file.close()
	f.close()
	mem_threshold.close()

##get cpu_used data and put them into the database
def getcpu(interval):
	cpu_used = psutil.cpu_percent(interval)
	t = int(time.time())
	sql = 'insert into cpu(cpu_used,time) values(%s,%s)'%(cpu_used, t)
	cur.execute(sql)
	print(sql)

while True:
        time.sleep(1)
        getmem()
	getcpu(1)

