import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.forms.models import model_to_dict

from .controller import choose_team, assign_tasks
from .models import Developer, Task, Team

# TODO: There's no error handling on purpose. During development I wanted to see the entire stack trace. Before moving
#  to production, I will wrap the code so it fails without disclosing the entire error report.


@require_POST
def developer_create(request):
    # TODO: I should ask the Product Manager why the API client should supply the "globally unique keys" instead of the
    #  server. Usually, it is for the client to make multiple call if it wants to create multiple entries.
    #  It is obviously possible to create an endpoint to create multiple entries using a single call, but then the
    #  Product Manager should address what happens if one entry is added successfully and another one results in
    #  an error. In the meantime skipping that requirement.
    decoded = json.loads(request.body.decode())
    dev = Developer.objects.create(**decoded)
    choose_team(dev)
    assign_tasks()
    return HttpResponse(status=201)


@require_POST
def developer_delete(request):
    # TODO: I should ask the Product Manager why instructed to use POST instead of DELETE HTTP Method
    developer_id = request.GET.get('id')
    developer = Developer.objects.filter(id=developer_id)
    developer.delete()
    # TODO: Ask the Product Manager what should happen when a developer is deleted. Should it be removed from the team?
    #  What should happen to the tasks in the team then?
    return HttpResponse()


@require_GET
def developer_read(request):
    developer_id = request.GET.get('id')
    developer = list(Developer.objects.filter(id=developer_id).values())[0]
    return JsonResponse(developer)


@require_http_methods(['PUT', 'POST'])
def developer_update(request):
    # TODO: I should ask the Product Manager why data is passed in the query string in opposed to the body
    developer_id = request.GET.get('id')
    key = request.GET.get('key')
    data = request.GET.get('data')
    update = {key: data}
    developer = Developer.objects.filter(id=developer_id)
    developer.update(**update)
    return HttpResponse()


@require_POST
def task_create(request):
    # TODO: Same question for the Product Manager as in developer_create() above
    decoded = json.loads(request.body.decode())
    Task.objects.create(**decoded)
    assign_tasks()
    return HttpResponse(status=201)


@require_http_methods(['DELETE', 'POST'])
def task_delete(request):
    task_id = request.GET.get('id')
    task = Task.objects.filter(id=task_id)
    task.delete()
    return HttpResponse()


@require_GET
def tasks_view(request):
    status = request.GET.get('status')
    # Preferred this writing although this means that anything that is not 'assigned' will be considered as 'unassigned'
    # Can be changed if necessary
    assigned = status == 'assigned'
    limit = int(request.GET.get('limit', '3'))
    tasks = list(Task.objects.filter(assigned__isnull=(not assigned)).order_by('created').values())[:limit]
    return JsonResponse(tasks, safe=False)


@require_GET
def developer_get_teams(request):
    teams = Team.objects.all()
    ret_val = []
    for team in teams:
        temp = model_to_dict(team)
        temp['is_ready'] = team.is_ready()
        ret_val.append(temp)
    return JsonResponse(ret_val, safe=False)
