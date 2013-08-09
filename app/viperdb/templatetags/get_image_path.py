from django import template

register = template.Library()

def image_path(entry_id, image_type, image_subtype):

    path = "http://localhost:80/images/%s/%s-%s" % \
           (image_type, entry_id, image_subtype)
    return path

register.simple_tag(image_path)
