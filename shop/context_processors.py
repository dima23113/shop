from .models import *


def category(request):
    tst = {}
    for d in Product.objects.all().select_related('subcategory').select_related('category'):
        if d.subcategory in tst.keys():
            pass
        else:
            tst[d.subcategory] = d
    category_img = [v for v in tst.values()]

    return {'categories': Category.objects.all().order_by('id'), 'category_img': category_img}
