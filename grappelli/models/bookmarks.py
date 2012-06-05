# coding: utf-8

from django.db import models, transaction
from django.utils.translation import ugettext as _

from grappelli.fields import PositionField

class Bookmark(models.Model):
    """
    Bookmark.
    """
    
    user = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name=_('User'), related_name="admin_bookmark_set")
    
    class Meta:
        app_label = "grappelli"
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')
        ordering = ['user',]
    
    def __unicode__(self):
        return u"%s" % (self.user)
    
    save = transaction.commit_on_success(models.Model.save)
    

class BookmarkItem(models.Model):
    """
    Bookmark Item.
    """
    
    bookmark = models.ForeignKey(Bookmark)
    title = models.CharField(_('Title'), max_length=80)
    link = models.CharField(_('Link'), max_length=200, help_text=_('The Link should be relative, e.g. /admin/blog/.'))
    
    # order
    order = PositionField(unique_for_field='bookmark')
    
    class Meta:
        app_label = "grappelli"
        verbose_name = _('Bookmark Item')
        verbose_name_plural = _('Bookmark Items')
        ordering = ['order']
    
    def __unicode__(self):
        return u"%s" % (self.title)
    
    save = transaction.commit_on_success(models.Model.save)
    

