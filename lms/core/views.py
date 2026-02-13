from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Note

def home(request):
    """Render the home page"""
    return render(request, 'core/home.html')

@login_required(login_url='accounts:login')
def dashboard(request):
    """Render user dashboard based on role"""
    user = request.user
    # Determine which dashboard to show based on user role
    try:
        role = user.profile.role
        if role == 'teacher':
            # Fetch only notes uploaded by this teacher
            notes = Note.objects.filter(uploader=user)
            return render(request, 'core/teacher_dashboard.html', {'notes': notes})
        else:
            # For students, show all notes
            notes = Note.objects.all()
            return render(request, 'core/student_dashboard.html', {'notes': notes})
    except:
        # Fallback to student dashboard with all notes
        notes = Note.objects.all()
        return render(request, 'core/student_dashboard.html', {'notes': notes})
