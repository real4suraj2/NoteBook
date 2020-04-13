import re
import json

from django.shortcuts import render, redirect, get_object_or_404
from .models import NoteCategory, NoteSeries, Note
from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, EditProfileForm, EditUserProfileForm
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
# Create your views here.

def single_slug(request,single_slug):
	category_slugs = [c.category_slug for c in NoteCategory.objects.all()]
	if single_slug in category_slugs:
		matching_series = NoteSeries.objects.filter(note_category__category_slug = single_slug)
		series_urls = {}
		for m in matching_series:
			part_one = Note.objects.filter(note_series__note_series = m.note_series).earliest('note_published')
			series_urls[m] = part_one.note_slug
		return render(request = request,
								template_name = 'main/category.html',
								context = {'note_series':matching_series,'part_ones':series_urls})		
	note_slugs = [n.note_slug for n in Note.objects.all()]
	if single_slug in note_slugs:
		this_note = Note.objects.get(note_slug=single_slug)
		notes_from_series = Note.objects.filter(note_series__note_series=this_note.note_series).order_by('note_published')
		this_note_index = list(notes_from_series).index(this_note)
		
		return render(request=request,
                      template_name='main/note.html',
                      context={"note": this_note,
									   "sidebar": notes_from_series,
									   "index": this_note_index})
	return HttpResponse(f'{single_slug} corresponds to nothing')

def search(request):
	if request.method != 'POST':
		return redirect('main:homepage')
	stop_words = ["a", "able", "about", "across", "after", "all", "almost", "also", "am", "among", "an", "and", "any", "are", "as", "at", "be", "because", "been", "but", "by", "can", "cannot", "could", "dear", "did", "do", "does", "either", "else", "ever", "every", "for", "from", "get", "got", "had", "has", "have", "he", "her", "hers", "him", "his", "how", "however", "i", "if", "in", "into", "is", "it", "its", "just", "least", "let", "like", "likely", "may", "me", "might", "most", "must", "my", "neither", "no", "nor", "not", "of", "off", "often", "on", "only", "or", "other", "our", "own", "rather", "said", "say", "says", "she", "should", "since", "so", "some", "than", "that", "the", "their", "them", "then", "there", "these", "they", "this", "tis", "to", "too", "twas", "us", "wants", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "would", "yet", "you", "your", "ain't", "aren't", "can't", "could've", "couldn't", "didn't", "doesn't", "don't", "hasn't", "he'd", "he'll", "he's", "how'd", "how'll", "how's", "i'd", "i'll", "i'm", "i've", "isn't", "it's", "might've", "mightn't", "must've", "mustn't", "shan't", "she'd", "she'll", "she's", "should've", "shouldn't", "that'll", "that's", "there's", "they'd", "they'll", "they're", "they've", "wasn't", "we'd", "we'll", "we're", "weren't", "what'd", "what's", "when'd", "when'll", "when's", "where'd", "where'll", "where's", "who'd", "who'll", "who's", "why'd", "why'll", "why's", "won't", "would've", "wouldn't", "you'd", "you'll", "you're", "you've","learnt","learn"]
	keys = request.POST.get('search')
	keys = re.split('\W+',keys)
	valid_keys = []
	for key in keys:
		if len(key) > 3 and key not in stop_words:
			valid_keys.append(key.lower())
	valid_keys.extend(['c++','c'])
	print(valid_keys)
	matching_series = {}
	matching_notes = {}
	for key in valid_keys:
		series = list(NoteSeries.objects.all())
		for s in series:
			a = str(s.note_series).lower().split()  + str(s.series_summary).lower().split()
			if key in a :
				matching_series[s.note_series] = s
		notes = list(Note.objects.all())
		for n in notes:
			b = str(n.note_title).lower().split()
			if key in b:
				matching_notes[n.note_title] = n		
	
		series_urls = {}
		for m in matching_series:
			part_one = Note.objects.filter(note_series__note_series = m).earliest('note_published')
			series_urls[matching_series[m]] = part_one.note_slug
	messages.warning(request,"Search is in alpha mode...So keep your expectations low :)" )
	return render(request = request,
							template_name = 'main/search.html',
							context = {'matching_series':matching_series,'matching_notes':matching_notes,'part_ones':series_urls,'no_series':len(matching_series) == 0,'no_note':len(matching_notes) == 0})

def homepage(request):
	return render(request = request,
							template_name = 'main/categories.html',
							context={"categories":NoteCategory.objects.all})


def account(request):
	return render(request = request,
							template_name = 'main/account.html',
							context = {'user':request.user})	


def register(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			to_email = form.cleaned_data.get('email')
			already_registered = User.objects.filter(email = to_email)
			if len(already_registered) >= 1:
				messages.error(request,'The email is already in use.')
				return redirect("main:register")


			user = form.save(commit = False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your NoteBook account.'
			message = render_to_string('main/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),#.decode(),
                'token':account_activation_token.make_token(user),
            })
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			messages.info(request,f'Verification link sent!')
			return render(request = request,
									  template_name = 'main/confirm_email.html',
									  context = {})
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")
	
	form = NewUserForm()	
	
	return render(request = request,
							template_name = 'main/register.html',
							context = {"form":form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        username = user.username
        messages.success(request, f"New account created: {username}")
        login(request, user)
        messages.info(request, f'You are now logged in as {username}')
        return redirect("main:homepage")
    else:
        return HttpResponse('Activation link is invalid!')


def logout_request(request):
	logout(request)
	messages.info(request,'Logged out successfully!')
	return redirect('main:login')


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        form2 = EditUserProfileForm(request.POST,request.FILES,instance = request.user.userprofile)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            print(form2.cleaned_data.get('image'))
            return redirect(reverse('main:account'))
    else:
        form = EditProfileForm(instance=request.user)
        form2 = EditUserProfileForm(instance = request.user.userprofile)
    return render(request = request,
							template_name = 'main/edit_profile.html',
							context = {'form': form,'form2':form2})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('main:account'))
        else:
            return redirect(reverse('main:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request = request, 
							template_name = 'main/change_password.html', 
							context = {'form': form})

def login_request(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data = request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username') 
			password = form.cleaned_data.get('password')
			user = authenticate(username = username,password = password)
			if user is not None:
				login(request,user)
				messages.info(request, f'You are logged in as {username}')
				return redirect('main:homepage')
			else:
				messages.error(request, 'Invalid username or password')
		else:
				messages.error(request, 'Invalid username or password')
	
	form = AuthenticationForm
	return render(request = request,
							template_name = 'main/login.html',
							context = {'form' : form})
							
@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data and 'body' not in data and 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})
        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        if not user.is_superuser: return JsonResponse(status = 500, data = {"message":"Permission denied"})
        payload = {'head': data['head'], 'body': data['body'],'url':'https://www.google.com'}
        #for u in user: send_user_notification(user = u, payload = payload , ttl = 1000)
        for u in User.objects.all():
            user_id = u.pk
            user_site = get_object_or_404(User, pk = user_id)
            try:
                send_user_notification(user = user_site,payload=payload,ttl=1000)
                print("success!!!")
            except:
                print('Fail')
        #send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
        
        
def push_notifications(request):
	print(request.user.is_superuser)
	if not request.user.is_superuser:
		messages.error(request,'Permission denied')
		return redirect('main:homepage')
	return render(request = request,
							template_name = 'main/push_notifications.html',
							context = {})