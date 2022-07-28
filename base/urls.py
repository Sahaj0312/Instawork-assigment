from django.urls import path
from .views import TeamMemberList, TeamMemberCreate, TeamMemberUpdate, TeamMemberDelete

urlpatterns = [
    path('', TeamMemberList.as_view(), name="members"),
    path('member-add/', TeamMemberCreate.as_view(), name='member-add'),
    path('member-update/<int:pk>/',
         TeamMemberUpdate.as_view(), name='member-update'),
    path('member-delete/<int:pk>/',
         TeamMemberDelete.as_view(), name='member-delete'),
]
