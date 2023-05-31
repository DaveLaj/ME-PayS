from django.contrib.auth import get_user_model
from me_pays_app.models.users import *
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

@require_GET
def validate_SID(request):
    student_id = request.GET.get('school_id')
    
    try:
        if EndUser.objects.filter(school_id=student_id, user__is_active=1, rfid_code__isnull=True).exists():
            # Student ID is active and doesn't have an associated RFID
            return JsonResponse({'exists': 2})
        elif EndUser.objects.filter(school_id=student_id, user__is_active=1).exists():
            # Student ID already has an RFID associated and is active
            return JsonResponse({'exists': 3})
        elif EndUser.objects.filter(school_id=student_id, user__is_active=0).exists():
            # Student ID is inactive
            return JsonResponse({'exists': 1})
    except EndUser.DoesNotExist:
        # Student ID does not exist in the database
        return JsonResponse({'exists': 0})



@require_POST
def register_rfid_code(request):
    school_id = request.POST.get('school_id')
    rfid = request.POST.get('rfid')

    try:
        end_user = EndUser.objects.get(school_id=school_id)
        end_user.rfid_code = rfid
        end_user.save()
        return JsonResponse({'success': True, 'message': 'Registration Successful'})
    except EndUser.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'EndUser not found; Call the Administrator Immediately'})