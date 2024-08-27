# Blog/templatetags/custom_filters.py

from django import template
import re

register = template.Library()

@register.filter
def add_lazy_load(value):
    pattern = re.compile(r'<img\s+src="([^"]+)"([^>]*)>', re.IGNORECASE)
    replacement = r'<img src="\1" \2 loading="lazy">'
    return pattern.sub(replacement, value)
