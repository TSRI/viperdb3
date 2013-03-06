from django import template

register = template.Library()

def image_path(virus, path_info ):

    path_info = path_info.split(',')

    image_type = path_info[0]
    image = path_info[1]
    filetype = "jpg"# path_info[2]

    virus_name = virus.entry_id

    path = "http://localhost:80/images/%s/%s-%s.%s" % (image_type, virus_name, image, filetype)

    return path

register.filter('image_path', image_path)
