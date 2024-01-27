from django import template
import math
from App_CourseTransaction.models import UserCourse
from App_Course.models import Course

register = template.Library()

@register.simple_tag
def calc_selling_price(price, discount):
    if discount is None or discount == 0:
        return price
    else:
        selling_price = price-(price*(discount*0.01))
        return math.ceil(selling_price)
 

def card_content_range_filter(value):
    return value[0:250] + '...'

register.filter('card_content_range_filter', card_content_range_filter) 

@register.simple_tag
def is_enrolled(request, slug):
    print("From CustomTags: ", slug)
    if not request.user.is_authenticated:
        return False
    
    try:
        user_course = UserCourse.objects.get(user=request.user, course = Course.objects.get(slug=slug))
        return True
    except:
        return False