# -*- coding: utf-8 -*-
import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.core.urlresolvers import reverse
from django.test import Client

pytestmark = pytest.mark.django_db


class TestPostAdmin:

    def test_admin_submit_actions(self):
        passw = '123'
        user1 = User.objects.create_superuser('admin1', 'admin1@example.com', passw)
        user2 = User.objects.create_superuser('admin2', 'admin2@example.com', passw)
        post1 = mixer.blend('blog.Post')
        post2 = mixer.blend('blog.Post')

        # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#reversing-admin-urls
        list_url = reverse('admin:{app}_{model}_changelist'.format(
            app=post1._meta.app_label,
            model=post1._meta.model_name,
        ))

        # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#reversing-admin-urls
        detail_url1 = reverse('admin:{app}_{model}_change'.format(
            app=post1._meta.app_label,
            model=post1._meta.model_name,
        ), args=(post1.id,))

        # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#reversing-admin-urls
        detail_url2 = reverse('admin:{app}_{model}_change'.format(
            app=post1._meta.app_label,
            model=post1._meta.model_name,
        ), args=(post2.id,))

        # Create two different sessions
        c1 = Client()
        c2 = Client()

        # Authenticate the users
        c1.login(username=user1.username, password=passw)
        c2.login(username=user2.username, password=passw)

        # User_1 access Post model instance
        user1_edit_post1 = c1.get(detail_url1)

        # All the Buttons are available
        assert user1_edit_post1.status_code == 200, 'Should return 200'
        assert user1_edit_post1.context['show_save_and_add_another'], 'Should return True'
        assert user1_edit_post1.context['show_save_and_continue'], 'Should return True'
        assert user1_edit_post1.context['show_save'], 'Should return True'
        assert user1_edit_post1.context['show_delete_link'], 'Should return True'

        # User_2 access the same Post model instance
        user2_edit_post1 = c2.get(detail_url1)

        # All the Buttons are not available anymore
        assert user2_edit_post1.status_code == 200, 'Should return 200'
        assert not user2_edit_post1.context['show_save_and_add_another'], 'Should return False'
        assert not user2_edit_post1.context['show_save_and_continue'], 'Should return False'
        assert not user2_edit_post1.context['show_save'], 'Should return False'
        assert not user2_edit_post1.context['show_delete_link'], 'Should return False'

        # User_2 access another Post model instance
        user2_edit_post2 = c2.get(detail_url2)

        # All the Buttons are not available anymore
        assert user2_edit_post2.status_code == 200, 'Should return 200'
        assert user2_edit_post2.context['show_save_and_add_another'], 'Should return True'
        assert user2_edit_post2.context['show_save_and_continue'], 'Should return True'
        assert user2_edit_post2.context['show_save'], 'Should return True'
        assert user2_edit_post2.context['show_delete_link'], 'Should return True'

        # User_1 Releases the Post model instance
        user1_list_view = c1.get(list_url)
        assert user1_list_view.status_code == 200, 'Should return 200'

        # User_2 access Again First Post model instance
        user2_edit_post1 = c2.get(detail_url1)

        # All the Buttons available Now
        assert user2_edit_post1.status_code == 200, 'Should return 200'
        assert user2_edit_post1.context['show_save_and_add_another'], 'Should return True'
        assert user2_edit_post1.context['show_save_and_continue'], 'Should return True'
        assert user2_edit_post1.context['show_save'], 'Should return True'
        assert user2_edit_post1.context['show_delete_link'], 'Should return True'




