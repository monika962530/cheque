from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Signs, Mvouchar, Bill
from django.contrib.auth import logout as dj_logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse
#from django import forms
# Create your views here.

@csrf_protect
def login(request):
		if request.user.is_authenticated:
				return HttpResponseRedirect("/home/")
		else:
				return render(request, "login.html", {})
def register(request):
		if request.method == "POST":
			user = request.POST["username"]
			last_name = request.POST['lastname']
			passwd = request.POST['password']
			cfm_passwd = request.POST['cfmpasswd']
			if cfm_passwd == passwd:
				all_users = []
				user_data = User.objects.all()
				for i in user_data:
						all_users.append(i.username)
				if user not in all_users:
						User.objects.create_user(user, password=passwd)
						data = User.objects.get(username=user)
						data.last_name = last_name
						data.save()
						dept = request.POST['department1']
						mob = request.POST['mobilenumber']
						Signs.objects.create(department=dept, mobile=mob, relation_id = data.id)
						messages.success(request, mark_safe("Your Account is created Please Login Now"))
						return HttpResponseRedirect("/login/")
				else:
						messages.error(request, "Create User with another username")
						return HttpResponseRedirect("/register/")
			else:
					messages.error(request, "Password does not match")
					return HttpResponseRedirect("/register/")
		return render(request, "register.html", {})
def forget(request):
		return render(request, "forget.html", {})
@csrf_protect	
def authlogin(request):
		if request.method == "POST":
			user = request.POST['username']
			passwd = request.POST['password']
			check_login = authenticate(username=user, password=passwd)
			if check_login is not None:
					auth_login(request, check_login)
					return HttpResponseRedirect("/home/")
			else:
					messages.error(request, "Password wrong try again to login")
					return HttpResponseRedirect("/login/")
def logout(request):
		for i in request.session.keys():
				del request.session[i]
				return HttpResponseRedirect("/login/")
		return HttpResponseRedirect("/login/")
		
def home(request):
	if request.user.is_authenticated:
		return render(request, 'home.html', {})
	return redirect('/login/')
@login_required(login_url="/login/")	
def all_reports(request):
	reports = []
	userdata = User.objects.get(username=request.user).id
	accountdata = Signs.objects.get(relation_id=userdata)
	for report_obj in Mvouchar.objects.filter(related_id=accountdata.id).order_by("cheque_date"):
			reports.append({'topay': report_obj.to_pay, 'chequeno': report_obj.cheque_no, 'chequedate': report_obj.cheque_date, 'date': report_obj.dated})
	return render(request, 'cheque/report.html', {'reports': reports})
@login_required(login_url="/login/")	
def all_duplicates(request):
    duplicates = []
    user_auth = User.objects.get(username=request.user).id
    datadb1 = Signs.objects.get(relation_id=user_auth)
    for duplicate_obj in Mvouchar.objects.filter(related_id=datadb1.id).order_by("cheque_date"):
	      duplicates.append({'topay': duplicate_obj.to_pay, 'amount1': duplicate_obj.amount, 'amount_string': duplicate_obj.amount_in_words, 'chequeno': duplicate_obj.cheque_no, 'accountno': duplicate_obj.account_no, 'chequedate': duplicate_obj.cheque_date})
    return render(request, 'cheque/duplicatecheque.html', {'duplicates': duplicates})	

@login_required(login_url="/login/")
def user_profile(request):
	signs = []
	user_aut = User.objects.get(username=request.user).id
	for sign_obj in Signs.objects.filter(relation_id=user_aut):
                signs.append({'department': sign_obj.department, 'mobilenumber': sign_obj.mobile})
	return render(request, 'cheque/profile.html', {'signs': signs})	
 # class mvouchar	
@csrf_exempt
@login_required(login_url="/login/")
def mvouchar(request):
			if request.method == "POST":
				userdata = request.user
				accountdata = userdata.signs
				t_p1 = request.POST.get('pay')
				chq_no = request.POST.get('chequeno')
				chq_d = request.POST.get('chequedate')
				vouch_no = request.POST.get('voucharno')
				at1 = request.POST.get('amount1')
				at_in_words = request.POST.get('amount_string')
				a_no = request.POST.get('accountno')
				table_data = json.loads(request.POST.get('MyData'))
				print(request.POST.get('MyData'))
				#create a cheque
				if len(chq_no)==6 and chq_no.isdigit():
						if Mvouchar.objects.filter(cheque_no =chq_no).exists():
							return JsonResponse({ 
								'success': False, 
								'msg': 'Cheque No. Already Exists', 
							}) 
						
						mini = Mvouchar(related_id=accountdata.id, to_pay = t_p1, cheque_no = chq_no, vouchar_no=vouch_no, amount = at1, amount_in_words=at_in_words, account_no=a_no, cheque_date=chq_d)
						#print(mini.cheque_no)
						#mini.full_clean()
						mini.save()
						
						messages.success(request, "Your Cheque is Created")	
				else:
					return JsonResponse({ 
							'success': False, 
							'msg': 'Invalid Cheque Number', 
					}) 
					# Now add bills to cheque 
				for data in table_data: 
					Bill.objects.create(voucher=mini, bill_no=data['BillNo'], bill_details=data['BillDetails'], am=data['Amount']) 

				return JsonResponse({ 
					'success': True, 
					'msg': 'Cheque and bills created successfully', 
				}) 

			if request.method == 'GET': 
				return render(request, 'cheque/mvouchar.html', {})
			return HttpResponseRedirect("/mvouchar/")

"""@csrf_exempt			
def jsdata(request):
	if request.method == "POST":
		userdata = request.user
		accountdata = userdata.signs
		table_data = json.loads(request.POST.get('MyData'))
			# print(table_data)
		r_data = {
				'success': True,
			}
		for data in table_data:
				# Since you are just creating objects you don't need to save created object in a variable.
					Bill.objects.create(vouchar=accountdata.id,bill_no = data['BillNo'], bill_details=data['BillDetails'],am=data['Amount'])
				   # r_data['success'] = False

			# IMO Views responding to ajax requests should send JsonResponse
		if r_data['success']:
				r_data['msg'] = 'Data Saved'
		else:
				r_data['msg'] = 'Not all Data Saved'
		return JsonResponse(r_data)
				"""