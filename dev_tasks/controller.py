from datetime import datetime

import pydash

from .models import Developer, Task, Team


def assign_tasks():
    """
    Assigns all the queued tasks to teams.
    """
    tasks = Task.objects.filter(assigned__isnull=True).order_by('created')
    for task in tasks:
        teams = Team.objects.filter(task_capacity__gte=task.points)
        for team in teams:
            if team.is_ready() and team.is_eligible(task.type):
                task.assigned = datetime.now()
                task.team_id = team
                team.task_capacity -= task.points
                task.save()
                team.save()
                break


def developer_updated():
    # TODO: Implement logic for what happens when a developer properties are updated
    pass


def assign_developer(dev: Developer, dev_type: str, team: Team):
    """
    Assigned a developer of a specific type to a relevant team.
    :param Developer dev: The developer to assign
    :param str dev_type: The developer's classification (e.g. Full Stack)
    :param Team team: The team to assign the developer to
    """
    dev.team_id = team
    dev.save()
    seats = pydash.get(team, f"{dev_type}_seats")
    seats -= 1
    pydash.set_(team, f"{dev_type}_seats", seats)
    team.save()


def create_team(team_type: str) -> Team:
    """
    This creates a team of a specific type according to the team definition in the specification.
    :param str team_type: The type of the team to create
    :return: The created team object.
    :rtype: Team
    """
    team_types = {
        "1": {
            "team_type": "1",
            "full_stack_seats": 3,
            "backend_seats": 0,
            "frontend_seats": 0,
            "academic_seats": 0,
            "task_capacity": 15
        },
        "2": {
            "team_type": "2",
            "full_stack_seats": 0,
            "backend_seats": 3,
            "frontend_seats": 3,
            "academic_seats": 0,
            "task_capacity": 10
        },
        "3": {
            "team_type": "3",
            "full_stack_seats": 1,
            "backend_seats": 0,
            "frontend_seats": 0,
            "academic_seats": 3,
            "task_capacity": 5
        },
        "4": {
            "team_type": "4",
            "full_stack_seats": 0,
            "backend_seats": 2,
            "frontend_seats": 2,
            "academic_seats": 2,
            "task_capacity": 5
        }
    }
    team = Team(**team_types[team_type])
    team.save()
    return team


def choose_team(dev: Developer):
    """
    Select an appropriate team for the specified developer.
    :param Developer dev: The developer to choose the team for
    """
    if not dev.is_pro():
        return
    if dev.is_full():
        partial_teams = Team.objects.filter(full_stack_seats__gt=0).order_by('team_type')
        if len(partial_teams) == 0:
            partial_teams = [create_team('1')]
        assign_developer(dev, 'full_stack', partial_teams[0])
    elif dev.is_back():
        partial_teams = Team.objects.filter(backend_seats__gt=0).order_by('team_type')
        if len(partial_teams) == 0:
            partial_teams = [create_team('2')]
        assign_developer(dev, 'backend', partial_teams[0])
    elif dev.is_front():
        partial_teams = Team.objects.filter(frontend_seats__gt=0).order_by('team_type')
        if len(partial_teams) == 0:
            partial_teams = [create_team('4')]
        assign_developer(dev, 'frontend', partial_teams[0])
    elif dev.is_academic():
        partial_teams = Team.objects.filter(academic_seats__gt=0).order_by('team_type')
        if len(partial_teams) == 0:
            partial_teams = [create_team('3')]
        assign_developer(dev, 'academic', partial_teams[0])
