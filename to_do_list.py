input_message = """Options:
"add" or "a" to add a new task
"show" or "s" to show all tasks
"mark" or "m" to mark a task as completed
"delete" or "d" to delete a task
"delete completed" or "dc" to delete all completed tasks
"quit" or "q" to exit
=> """

options = ["add","a","show","s","mark","m","delete","d","delete completed","dc","quit","q"]

import sqlite3
from termcolor import colored

db = sqlite3.connect("tasks.db")
cr = db.cursor()

cr.execute("create table if not exists tasks(name text, status text)")

def commit_and_close():
	db.commit()
	db.close()


def add_task():
	task = input("Enter the name of the task you want to add: ").strip().capitalize()
	cr.execute(f"select * from tasks where name = '{task}'")
	result = cr.fetchone()
	if result == None:
		cr.execute(f"insert into tasks values('{task}','Pending')")
		print("Task added successfully!")
	else:
		print("This task already exists!")

	user_add_input = input("Do you want to show the current tasks? <Y,N> ").strip().upper()
	if user_add_input == "Y":
		show_tasks()
	elif user_add_input == "N":
		pass
	else:
		print("Invalid choice!")


def show_tasks():
	cr.execute("select * from tasks")
	result = cr.fetchall()
	print(f"You have {len(result)} tasks")
	if len(result) > 0:
		for row in result:
			print(f"Task => {row[0]} , Status => {row[1]}")

	else:
		user_input_if_add = input("Do you want to add one? <Y,N> ").strip().upper()
		if user_input_if_add == "Y":
			add_task()
		elif user_input_if_add == "N":
			pass
		else:
			print("Invalid choice!")

def mark_task():
	task = input("Enter the name of the task you want to mark as completed: ").strip().capitalize()
	cr.execute(f"select * from tasks where name = '{task}'")
	result = cr.fetchone()
	if result == None:
		user_mark_input = input("This task doesn't exsist in your tasks do you want to add it? <Y,N> ").strip().upper()
		if user_mark_input == "Y":
			cr.execute(f"insert into tasks values('{task}','Completed')")
			print("Task added successfully and marked as completed!")
		elif user_mark_input == "N":
			pass
		else:
			print("Invalid choice!")
	else:
		cr.execute(f"select * from tasks where name = '{task}' and status = 'Completed'")
		result = cr.fetchone()
		if result == None:
			cr.execute(f"update tasks set status = 'Completed' where name = '{task}'")
			print("Task marked as completed!")
		else:
			user_mark_input = input("This task is already marked as completed do you want to show your tasks? <Y-N> ").strip().upper()
			if user_mark_input == "Y":
				show_tasks()
			elif user_mark_input == "N":
				pass
			else:
				print("Invalid choice!")

def delete_task():
	task = input("Enter the name of the task you want to delete: ").strip().capitalize()
	cr.execute(f"select * from tasks where name = '{task}'")
	result = cr.fetchone()
	if result == None:
		print("This task doesn't exist")
	else:
		cr.execute(f"delete from tasks where name = '{task}'")
		print("Task deleted successfully!")

def delete_completed():
	cr.execute(f"select * from tasks where status ='Completed'")
	result = cr.fetchone()
	if result == None:
		print("You don't have any completed tasks to delete!")
	else:
		cr.execute("delete from tasks where status = 'Completed'")
		print("Completed tasks deleted successfully!")

while True:
	user_input = input(colored(input_message, "blue")).strip().lower()

	if user_input in options:
		if user_input in ["add","a"]:
			add_task()

		elif user_input in ["show","s"]:
			show_tasks()

		elif user_input in ["mark","m"]:
			mark_task()

		elif user_input in ["delete","d"]:
			delete_task()

		elif user_input in ["delete completed","dc"]:
			delete_completed()

		else:
			print("Closed")
			commit_and_close()
			break
	else:
		print("Please select a valid option!")
