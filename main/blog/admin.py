# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Post
from django.contrib.admin.templatetags.admin_modify import register, submit_row
from django.contrib import messages
from django.core.cache import cache


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ['title', 'slug', 'content', 'updated', 'created']
    exclude = ['editable', 'editable_by']
    prepopulated_fields = {"slug": ("title",)}

    @register.inclusion_tag('admin/submit_line.html', takes_context=True)
    def submit_row(context):
        submit = submit_row(context)
        submit.update(
            {
                'show_save_and_add_another': context.get(
                    'show_save_and_add_another',
                    submit['show_save_and_add_another']
                ),
                'show_save_and_continue': context.get(
                    'show_save_and_continue',
                    submit['show_save_and_continue']
                ),
                'show_save': context.get(
                    'show_save',
                    submit['show_save']
                ),
                'show_delete_link': context.get(
                    'show_delete_link',
                    submit['show_delete_link']
                )
        })
        return submit

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        user_id = request.user.id
        editor = cache.get(user_id)
        if editor is not None:
            obj = Post.objects.get(pk=int(editor))
            obj.make_editable()
            cache.delete(user_id)
        return super(PostAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, extra_context=None):
        obj = Post.objects.get(pk=object_id)
        user_id = request.user.id
        if obj.editable or obj.editable_by == user_id:
            obj.make_read_only(user_id)
            cache.set(user_id, object_id)
            return super(PostAdmin, self).change_view(request, object_id, extra_context=extra_context)
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['show_delete'] = False
        messages.warning(request, 'This Instance is currently under Edit.')
        return super(PostAdmin, self).change_view(request, object_id, extra_context=extra_context)


admin.site.register(Post, PostAdmin)
