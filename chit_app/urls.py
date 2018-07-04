from django.urls import path
from chit_app.views import *

app_name = 'chit_app'

urlpatterns = [
    path('', First_page_view, name = 'firstpage'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('signup/', SignUp.as_view(), name = 'signup'),
    path('logout/', Logout, name = 'logout'),
    path('addchit/', AddChit.as_view(), name = 'addchit'),
    path('chitlist/', ChitList.as_view(), name = 'chitlist'),
    path('chitlist/<int:chit_id>', ViewUserChits.as_view(), name = 'userchitview'),
    path('chitlist/<int:chit_id>/<int:lifted_id>/request', RequestLift.as_view(), name = 'request'),
    path('chitlist/<int:chit_id>/addpeople/', AddPeople.as_view(), name = 'addpeople'),
    path('chitlist/<int:pk>/deletechit/', DeleteChit.as_view(), name = 'addpeople'),
    path('chitlist/<int:chit_id>/viewpeople/', ViewPeople.as_view(), name = 'viewpeople'),
    path('chitlist/<int:chit_id>/viewpeople/<int:lifted_id>', ConfirmLift.as_view(), name = 'confirmlift'),
    path('chitlist/<int:chit_id>/viewpeople/remove_requests', RemoveRequests, name = 'remove_requests'),
]