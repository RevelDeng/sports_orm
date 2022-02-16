from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q, Count

from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"atlantic_conference_teams": League.objects.get(id=5).teams,
		"curr_bos_penguins": Team.objects.get(id=28).curr_players,
		"curr_base_conf": Player.objects.filter(curr_team__in=Team.objects.filter(league=League.objects.get(id=2))),
		"curr_foot_lopez": Player.objects.filter(curr_team__in=Team.objects.filter(league=League.objects.get(id=7))).filter(last_name__iexact="lopez"),
		"football_players": Player.objects.filter(
			Q(all_teams__in=Team.objects.filter(league=League.objects.get(id=9))) | Q(all_teams__in=Team.objects.filter(league=League.objects.get(id=7)))
		).distinct(),
		"sophia_teams": Team.objects.filter(curr_players__in=Player.objects.filter(first_name__iexact="sophia")),
		"sophia_leagues": League.objects.filter(teams__in=Team.objects.filter(curr_players__in=Player.objects.filter(first_name__iexact="sophia"))),
		"most_flores": Player.objects.filter(last_name__iexact="flores").exclude(curr_team=Team.objects.get(id=10)),
		"sams_teams": Team.objects.filter(all_players__in=Player.objects.filter(id=115)),
		"tigercats": Player.objects.filter(all_teams__in=Team.objects.filter(id=37)),
		"old_vikings": Player.objects.filter(all_teams__in=Team.objects.filter(id=40)).exclude(curr_team=Team.objects.get(id=40)),
		"pre_colts_jacob_gray": Team.objects.filter(all_players__in=Player.objects.filter(id=151)),
		"amateur_baseball_josh": Player.objects.filter(
			first_name__iexact="joshua").filter(all_teams__in=Team.objects.filter(league=League.objects.get(id=3))
		),
		"12_player_teams": Team.objects.annotate(total_players=Count("all_players")),
		"players_by_teamcount": Player.objects.annotate(num_teams=Count("all_teams")).order_by('num_teams')
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")