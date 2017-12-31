# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from django.conf import settings
from mixer.backend.django import mixer


pytestmark = pytest.mark.django_db

class TestPost:

    def test_post_unicode(self):
        post_title = 'Sample title'
        post = mixer.blend('blog.Post', title=post_title)
        assert str(post) == post_title, 'Should return only the Title'

    def test_post_instance(self):
        post = mixer.blend('blog.Post',)
        user = mixer.blend(settings.AUTH_USER_MODEL)
        post.make_read_only(user.id)
        read_only = post

        assert not read_only.editable, 'Should return False'
        assert read_only.editable_by == user.id, 'Should be User pk'

        read_only.make_editable()
        editable_post = read_only

        assert editable_post.editable, 'Should return True'
        assert not editable_post.editable_by, 'Should return 0'



