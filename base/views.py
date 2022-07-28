from typing import List
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import TeamMember
from django.urls import reverse_lazy


class TeamMemberList(ListView):
    model = TeamMember


class TeamMemberCreate(CreateView):
    model = TeamMember
    fields = '__all__'
    success_url = reverse_lazy('members')


class TeamMemberUpdate(UpdateView):
    model = TeamMember
    fields = '__all__'
    success_url = reverse_lazy('members')


class TeamMemberDelete(DeleteView):
    model = TeamMember
    success_url = reverse_lazy('members')
