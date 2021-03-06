from django.shortcuts import render,redirect,render_to_response

from django.template import loader,RequestContext
from django.http import HttpResponse

from django import forms

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

#from notes_forms import LoginForm
from models import Note,NoteForm

# Create your views here.
	

@login_required(login_url="/notes/index/")
def dashboard(request):
    from django.forms.models import inlineformset_factory
    # InlineFormSet with parent_model=User and model=Note
    NoteFormSet=inlineformset_factory(User,Note,can_delete=True,extra=1,form=NoteForm)
    if request.method=="POST":
        formset=NoteFormSet(request.POST,request.FILES,instance=request.user)
        if formset.is_valid():
            # updates and deletes Note objects based on user inputs
            formset.save()
        return redirect("dashboard")
    else:
        formset=NoteFormSet(instance=request.user)
        return render_to_response("dashboard.html",
        {'form':NoteForm(),'formset':formset},RequestContext(request))

@login_required(login_url="/notes/index/")
def dashboard_old(request):
	if request.method=="POST":
		#this is pulling a copy of the post
		d=request.POST.copy()
		#this will add the user id as the owner of the post
		d.update({'owner':request.user.id})
		form=NoteForm(d)
		if not form.is_valid():
		#if form is not valid return to the dashboard with errors
			template=loader.get_template("dashboard.html")
			rc=RequestContext(request,{'form':form})
			return HttpResponse(template.render(rc))
		note=form.save(commit=False)
		note.owner=request.user
		note.save()
		return redirect("dashboard")
	else:	
		template=loader.get_template("dashboard.html")
		rc=RequestContext(request,{"form":NoteForm()})
		return HttpResponse(template.render(rc))


def index(request):    
    if request.method=="POST":
        print "Received POST"
        form=LoginForm(request.POST)
        if form.is_valid():
            print "FORM is Valid"
            # user registration or login code
            username,pwd=request.POST.get("username",None),request.POST.get("password")
            if not username or not pwd:
                return HttpResponse("Username or password not present")
            try:
                user=User.objects.get(username__exact=username)
            except ObjectDoesNotExist,ex:
                print "Creating new user..."
                user=User.objects.create_user(username,username,pwd)
            if user:
                print "Authenticating..."
                user=authenticate(username=username,password=pwd)
            print "Logging in user"
            login(request,user)
            return redirect("dashboard")
        else:
            print "FORM is NOT VALID"
            template=loader.get_template("index.html")
            rc=RequestContext(request,{'form':form})
            return HttpResponse(template.render(rc))
    else:
        template=loader.get_template("index.html")
        rc=RequestContext(request,{'form':LoginForm()})
        return HttpResponse(template.render(rc))


class LoginForm(forms.Form):
	username=forms.EmailField()
	password=forms.CharField(widget=forms.PasswordInput())
		

def dologout(request):
	logout(request)
	return redirect("index")


def example(request):
	#return HttpResponse("Hello, Notes")
	template=loader.get_template("example.html")
	temp=72
	rc=RequestContext(request,{'fruits':["apples","oranges","bananas"], "username":"Courtney", "temp":temp})
	return HttpResponse(template.render(rc))