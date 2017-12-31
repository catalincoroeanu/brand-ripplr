# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    content = models.TextField(max_length=600)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    editable = models.BooleanField(default=True)
    editable_by = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        unique_together = ('title', 'slug')

    def make_read_only(self, user):
        self.editable = False
        self.editable_by = int(user)
        self.save()

    def make_editable(self):
        self.editable = True
        self.editable_by = 0
        self.save()
