from django.urls import path,include
from .views import taskdelete,Updatetask ,apply ,homepage,index,user_login,user_logout,signup,admindetail, get_certificate, start_test
urlpatterns = [
    path('test/<int:id>/', homepage, name='test'),
    path('', index, name='home'),    
    path('start-test/', start_test, name='start_test'),
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('certificate/', get_certificate, name='get_certificate'),
    
    # path('adminpage/', adminpage, name='adminpage'),
    # path('adminpage/apply/', apply, name='apply'),    
    # path('adminpage/modul/<int:id>/', admindetail, name='admindetail'),
    # path('taskdelete/<int:id>/', taskdelete, name='taskdelete'),
    # path('updatetask/<int:pk>/', Updatetask.as_view(), name='updatetask'),
]
