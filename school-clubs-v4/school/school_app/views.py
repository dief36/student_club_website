from django.shortcuts import render, get_object_or_404, redirect
from .models import Club, ClubActivity
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
from . forms import ClubActivityForm 
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import Group # type: ignore
from datetime import date

def toggle_activity(request, activity_id):
    activity = get_object_or_404(ClubActivity, id=activity_id)
    activity.activity_is_active = not activity.activity_is_active
    activity.save()
    return JsonResponse({'status': 'success'})



def create_activity(request):
    if request.method == 'POST':
        form = ClubActivityForm(request.POST, request.FILES)
        if form.is_valid():
            
            activity_header = form.cleaned_data['activity_header']
            activity_content = form.cleaned_data['activity_content']
            activity_image = form.cleaned_data['activity_image']
            activity_club = form.cleaned_data['activity_club']
            activity_date = form.cleaned_data['activity_date']
            
            
            club_activity = ClubActivity.objects.create(
                activity_header=activity_header,
                activity_content=activity_content,
                activity_image=activity_image,
                activity_club=activity_club,
                activity_date=activity_date
            )
            
            
    else:
        form = ClubActivityForm()
    return render(request, 'admin/add_activity.html', {'form': form,})



def home(request):
    clubs = Club.objects.all()
    search = request.GET.get('search')
    if search:
        clubs = clubs.filter(Q(club_name__icontains= search),
                             Q(club_description__icontains = search))
    context = {
       'clubs': clubs,
    }
    return render(request, 'home.html', context)

def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    context = {
        'club': club,
    }
    return render(request, 'detail.html', context)

def club_activity(request, club_id):

    club = get_object_or_404(Club, id=club_id)
    activities_in_club = ClubActivity.objects.filter(activity_club=club)
    context = {
        'club': club,
        'activities_in_club': activities_in_club,
    }
    return render(request, 'activities.html', context)

def haberler(request):
    activities = ClubActivity.objects.all()

    context = {
        'activities':activities,
    }
    return render(request, 'haberler.html', context)

def haberler(request):
  # Assuming you want to filter by selected date from a form or URL parameter
  selected_date = request.GET.get('date')  # Example: Accessing date from a URL parameter

  if selected_date:
    try:
      activity_date = date.fromisoformat(selected_date)
      activities = ClubActivity.objects.filter(activity_date__date=activity_date)
    except ValueError:
      # Handle invalid date format (optional)
      activities = []
  else:
    # Default behavior: show all activities
    activities = ClubActivity.objects.all()

  context = {
    'activities': activities,
  }
  return render(request, 'haberler.html', context)

def haberler(request):
  # Assuming you want to filter by selected date from a form or URL parameter
  selected_date = request.GET.get('date')  # Example: Accessing date from a URL parameter

  if selected_date:
    try:
      activity_date = date.fromisoformat(selected_date)
      activities = ClubActivity.objects.filter(activity_date__date=activity_date)
    except ValueError:
      # Handle invalid date format (optional)
      activities = []
  else:
    # Default behavior: show all activities
    activities = ClubActivity.objects.all()

  context = {
    'activities': activities,
  }
  return render(request, 'haberler.html', context)


@login_required
def student_home(request):
    return render(request, 'student/student_home.html')


def student_login(request):
    if request.method == 'POST':
        
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        

        if user is not None and user.groups.filter(name='student').exists():
            
            login(request, user)
            
            return redirect("home")
        else:
            return render(request, 'student/student_login.html', {
                "error": "Kullanıcı adı veya parola yanlış."
            })
    return render(request, 'student/student_login.html')

def student_logout(request):
    logout(request)
    return redirect('home')

@login_required
def admin_home(request):
    return render(request, 'admin/admin_home.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None and user.groups.filter(name='club manager').exists():
            login(request, user)
            return redirect("admin-home")
        else:
            return render(request, 'admin/admin_login.html', {
                "error": "Kullanıcı adı veya parola yanlış."
            })
    return render(request, 'admin/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin-login')

@login_required
def sks_home(request):
    activities = ClubActivity.objects.all()
    activity_formset = [ClubActivityForm(prefix=str(activity.id)) for activity in activities]

    if request.method == 'POST':
        for form in activity_formset:
            if form.is_valid():
                form.save()
        return redirect('sks-home')
    return render(request, 'sks/skss_home.html', {'activities': activities, 'activity_formset': activity_formset})



def sks_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        #Aksi halde None değeri döner.
        if user is not None and user.groups.filter(name='sks admin').exists():
            login(request, user)
            return redirect('sks-home')
        else:
            return render(request, 'sks/sks_login.html', {
                "error": "Kullanıcı adı veya parola yanlış."
            })
    return render(request, 'sks/sks_login.html')
   


def sks_logout(request):
    logout(request)
    return redirect('sks-login')




