from django.contrib import admin
from blog.models import Post, BlogComment
# Register your models here.
admin.site.register(BlogComment)

# inject tiny js code to post admin panel
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tiny.js',)