import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Astronaut, Spacecraft, Mission
from django.db.models import Q, Count, Avg


def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    ).order_by('name')

    result = []
    for a in astronauts:
        status = 'Active' if a.is_active else 'Inactive'
        result.append(f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {status}")
    return "\n".join(result)


def get_top_astronaut():
    top_astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if top_astronaut:
        return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.mission_count} missions."
    return "No data."


def get_top_commander():
    top_commander = Astronaut.objects.annotate(
        commanded_missions_count=Count('commanded_missions')
    ).filter(commanded_missions_count__gt=0).order_by('-commanded_missions_count', 'phone_number').first()

    if top_commander:
        return f"Top Commander: {top_commander.name} with {top_commander.commanded_missions_count} commanded missions."
    return "No data."


def get_last_completed_mission():
    last_mission = Mission.objects.filter(status='Completed').order_by('-launch_date').first()

    if not last_mission:
        return "No data."

    commander_name = last_mission.commander.name if last_mission.commander else "TBA"
    astronaut_names = ", ".join([astronaut.name for astronaut in last_mission.astronauts.order_by('name')])
    total_spacewalks = sum(astronaut.spacewalks for astronaut in last_mission.astronauts.all())

    return (f"The last completed mission is: {last_mission.name}. Commander: {commander_name}. "
            f"Astronauts: {astronaut_names}. Spacecraft: {last_mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    most_used_spacecraft = Spacecraft.objects.annotate(num_missions=Count('mission')).order_by('-num_missions', 'name').first()

    if not most_used_spacecraft:
        return "No data."

    num_astronauts = Astronaut.objects.filter(missions__spacecraft=most_used_spacecraft).distinct().count()

    return (
        f"The most used spacecraft is: {most_used_spacecraft.name}, manufactured by {most_used_spacecraft.manufacturer}, "
        f"used in {most_used_spacecraft.num_missions} missions, astronauts on missions: {num_astronauts}.")


def decrease_spacecrafts_weight():
    spacecrafts_to_update = Spacecraft.objects.filter(
        mission__status='Planned', weight__gte=200.0
    ).distinct()

    num_of_spacecrafts_affected = spacecrafts_to_update.count()

    if num_of_spacecrafts_affected == 0:
        return "No changes in weight."

    for spacecraft in spacecrafts_to_update:
        spacecraft.weight -= 200.0
        spacecraft.save()

    avg_weight = Spacecraft.objects.all().aggregate(avg_weight=Avg('weight'))['avg_weight']

    return f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg"




