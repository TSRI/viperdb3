from django import template

register = template.Library()

def image_path(virus, image_type, image, filetype="jpg"):
 	virus_name = virus.name
	path = "images/%s/%s-%s.%s" % (image_type, virus_name, image, filetype)

	return path

register.filter('image_path', image_path)
