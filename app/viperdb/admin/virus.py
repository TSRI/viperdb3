from django.contrib import admin

class VirusAdmin(admin.ModelAdmin):
    actions = ['start_analysis', 'generate_images']
    readonly_fields = ('entry_key', 'layer_count',)

    def has_add_permission(self, request):
        return False

    def start_analysis(self, request, queryset):
        [virus.analyze() for virus in queryset.all()]
    start_analysis.short_description = "Start analysis with selected viruses"

    def generate_images(self, request, queryset):
        [virus.generate_images() for virus in queryset.all()]
    generate_images.short_description = "Generate images for selected viruses"
