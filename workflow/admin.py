# -*- coding: utf-8 -*-
#from django.contrib import admin
from django.contrib.admin import site, ModelAdmin, TabularInline, StackedInline
#from django.contrib.auth.models import User

from workflow.models import *
from workflow.forms import StepAdminForm


class StepInline(StackedInline):
    model = Step
    form = StepAdminForm
    extra = 1
    ordering = ['sequence']
    classes = ('collapse-open',)
    allow_add = True


class DynamicFieldProcessInline(TabularInline):
    model = DynamicFieldProcess
    extra = 1
    #exclude = ['name','initial','max_length']
    fields = ['label', 'fieldtype', 'required', 'sequence']
    allow_add = True


class ProcessAdmin(ModelAdmin):
    list_display = ('name','id','desc')
    ModelAdmin.actions_on_top = True
    inlines = [ DynamicFieldProcessInline, StepInline, ]
site.register(Process, ProcessAdmin)


class DynamicFieldStepInline(TabularInline):
    model = DynamicFieldStep
    extra = 1
    #exclude = ['name','initial','max_length']
    fields = ['label', 'fieldtype', 'required', 'sequence']
    allow_add = True


class StepAdmin(ModelAdmin):
    ModelAdmin.actions_on_top = True
    list_display = ('id','name','process','sequence')
    list_filter = ('process','managers')
    list_display_links = ('name','process')
    ordering = ['sequence']
    inlines = [ DynamicFieldStepInline, ]
site.register(Step, StepAdmin)


class WorkAdmin(ModelAdmin):
    list_display = ('id','current_step','name','owner')
    list_display_links = ('name',)
    search_fields = ['name','desc']
    ModelAdmin.actions_on_top = True
    list_filter = ('current_step','owner')
site.register(Work, WorkAdmin)


site.register(Attachment)


# User profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
site.unregister(User)
class UserProfileInline(TabularInline):
    model = UserProfile
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
site.register(User, UserProfileAdmin)
