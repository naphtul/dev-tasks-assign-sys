from django.urls import path

from . import views

app_name = 'dev_tasks'
urlpatterns = [
    # POST /developer/data/create
    path('developer/data/create', views.developer_create, name='developer_create'),
    # POST /developer/data/delete?id=#
    path('developer/data/delete', views.developer_delete, name='developer_delete'),
    # GET /developer/data/retrieve?id=#
    path('developer/data/retrieve', views.developer_read, name='developer_read'),
    # PUT or POST /developer/data/update?id=#&key=#&data=#
    path('developer/data/update', views.developer_update, name='developer_update'),
    # POST /tasks/create
    path('tasks/create', views.task_create, name='task_create'),
    # DELETE/POST /task/delete?id=#
    path('task/delete', views.task_delete, name='task_delete'),
    # GET /tasks/view?status=<assigned / unassigned>&limit=#
    path('tasks/view', views.tasks_view, name='tasks_view'),
    # GET /developer/data/get_teams
    path('developer/data/get_teams', views.developer_get_teams, name='developer_get_teams'),
]
