from .models import *


def category(request):
    cat_img = []
    for i in Category.objects.all().order_by('id'):
        for c in i.subcategories.all():
            for d in c.subcategory_products.all()[:1]:
                cat_img.append(d)
    return {'categories': Category.objects.all().order_by('id'), 'cat_img': cat_img}
