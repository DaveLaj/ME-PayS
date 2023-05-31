from django.contrib.auth import get_user_model
from me_pays_app.models.users import *
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def validate_SID(request):
    student_id = request.GET.get('school_id')
    
    try:
        if EndUser.objects.get(school_id=student_id, user__is_active=1, rfid_code__isnull=True):
        # Student ID is active and doesnt have an associated rfid
            return JsonResponse({'exists' : 2})
        elif EndUser.objects.get(school_id=student_id, user__is_active=1):
        # Student ID is already has an rfid associated and is active
            return JsonResponse({'exists': 3})
        elif EndUser.objects.get(school_id=student_id):
        # Student ID is inactive
            return JsonResponse({'exists': 1})
    except EndUser.DoesNotExist:
        # Student ID does not exist in the database
        return JsonResponse({'exists': 0})


