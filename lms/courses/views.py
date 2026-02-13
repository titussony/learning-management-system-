from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
import os


@login_required(login_url='accounts:login')
def upload_course(request):
    """Handle note file uploads"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        uploaded_file = request.FILES.get('file')
        
        # Validation
        if not title:
            messages.error(request, 'Please enter a note title.')
            return render(request, 'courses/upload_note.html')
        
        if not uploaded_file:
            messages.error(request, 'Please select a file to upload.')
            return render(request, 'courses/upload_note.html')
        
        # Check file size (max 10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            messages.error(request, 'File size must be less than 10MB.')
            return render(request, 'courses/upload_note.html')
        
        try:
            # Create and save the note
            note = Note.objects.create(
                title=title,
                content=uploaded_file,
                uploader=request.user
            )
            messages.success(request, f'Note "{title}" uploaded successfully!')
            return redirect('core:dashboard')
        except Exception as e:
            messages.error(request, f'Error uploading file: {str(e)}')
            return render(request, 'courses/upload_note.html')
    
    return render(request, 'courses/upload_note.html')


def note_list(request):
    """Display all available notes"""
    notes = Note.objects.all()
    return render(request, 'courses/note_list.html', {'notes': notes})


@login_required(login_url='accounts:login')
def download_note(request, note_id):
    """Download a note file"""
    note = get_object_or_404(Note, id=note_id)
    
    if note.content:
        response = FileResponse(note.content.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{note.title}-{os.path.basename(note.content.name)}"'
        return response
    else:
        messages.error(request, 'File not found.')
        return redirect('core:dashboard')


@login_required(login_url='accounts:login')
def delete_note(request, note_id):
    """Delete a note (only by the uploader)"""
    note = get_object_or_404(Note, id=note_id)
    
    # Only allow the user who uploaded the note to delete it
    if request.user != note.uploader:
        messages.error(request, "You don't have permission to delete this note.")
        return redirect('core:dashboard')
    
    try:
        # Delete the file from storage
        if note.content:
            note.content.delete(save=False)
        # Delete the database record
        note.delete()
        messages.success(request, "Note deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting note: {str(e)}")
    
    return redirect('core:dashboard')