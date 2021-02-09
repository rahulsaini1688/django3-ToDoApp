from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import ToDoForm
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required



def todoshome(request):
	return render(request, 'todos/todoshome.html')


def signupuser(request):
	if request.method == 'GET':

		return render(request, 'todos/signupuser.html', {'form': UserCreationForm()})

	else :
		try:
			if request.POST['password1'] == request.POST['password2']:
				user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('currenttasks')
			else :

				return render(request, 'todos/signupuser.html', {'form': UserCreationForm(), 'pswd_mismatch_msg': 'Passwords did not match. Please try again.'})

		except IntegrityError :
			return render(request, 'todos/signupuser.html', {'form': UserCreationForm(), 'usrname_taken_msg': 'Sorry that username is already taken. Please signup with a different username.'})
 		
@login_required
def currenttasks(request):
	current_tasks = ToDo.objects.filter(user = request.user, date_completed__isnull = True)
	return render(request, 'todos/currenttasks.html',{'Current_tasks': current_tasks} )

@login_required
def completedtasks(request):
	completed_tasks = ToDo.objects.filter(user = request.user, date_completed__isnull = False).order_by('-date_completed')
	return render(request, 'todos/completedtasks.html',{'completed_tasks': completed_tasks } )

def loginuser(request):
	if request.method == 'GET':

		return render(request, 'todos/loginuser.html', {'form': AuthenticationForm()})
	else :
		user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
		if user is not None:
			login(request, user)
			return redirect('currenttasks')
		else:
			return render(request, 'todos/loginuser.html', {'form': AuthenticationForm(), 'login_fail_msg': 'Sorry we didnt find a match for the username and password. Try with existing username and password OR Signup'})

@login_required
def logoutuser(request):
	if request.method == 'POST':
		logout(request)
		return redirect('todoshome')

@login_required
def createtodos(request):
	if request.method == 'GET':

		return render(request, 'todos/createtodos.html', {'form': ToDoForm()})

	else :
		try:
			form = ToDoForm(request.POST)
			new_to_do = form.save(commit =False)
			new_to_do.user = request.user
			new_to_do.save()
			return redirect('currenttasks')
			
		except ValueError :
			return render(request, 'todos/createtodos.html', {'form': ToDoForm(), 'bad_data_error': 'Bad Data entered, please try again!'})
 	
@login_required
def viewtodos(request, todo_pk):
	todo = get_object_or_404(ToDo, pk=todo_pk, user =request.user)
	if request.method == 'GET':
		
		form = ToDoForm(instance = todo)

		return render(request, 'todos/viewtodos.html', {'todo': todo, 'form': form })

	else :
		try:
			form = ToDoForm(request.POST, instance = todo)
			form.save()
			
			return redirect('currenttasks')
			
		except ValueError :
			return render(request, 'todos/viewtodos.html', {'form': ToDoForm(), 'bad_data_error': 'Bad Data entered, please try again!'})

@login_required
def completetodo(request, todo_pk):
	todo = get_object_or_404(ToDo, pk=todo_pk, user =request.user)
	if request.method == 'POST':
		
		todo.date_completed = timezone.now() 
		todo.save()

		return redirect('currenttasks')

@login_required
def deletetodo(request, todo_pk):
	todo = get_object_or_404(ToDo, pk=todo_pk, user =request.user)
	if request.method == 'POST':
		
		
		todo.delete()

		return redirect('currenttasks')


