from .models import *


def category(request):
    return {'categories': Category.objects.all().order_by('id')}
