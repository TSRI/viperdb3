from django.conf.urls.defaults import patterns, url

from viperdb.views.utilities import GalleryMakerView

urlpatterns = patterns("viperdb.views.utilities",
    url(r"^gallery-maker$", GalleryMakerView.as_view(), name="gallery_maker"),
)
