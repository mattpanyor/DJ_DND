from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.urls import reverse
from django.views import generic
from npc.models import Npc, Player
import json


class IndexView(generic.ListView):
    model = Npc
    template_name = 'npc/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['player_list'] = Player.objects.all()
        return context


class DamageHistoryView(generic.DetailView):
    model = Npc
    template_name = 'npc/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dmgh = json.loads(context['npc'].npc_damage_history)
        if 'dmg_history' in dmgh:
            context['dmg_history'] = dmgh['dmg_history']
        return context


def add_npc(request):
    name = request.POST['npc_name']
    health = request.POST['npc_health']

    new_npc = Npc(npc_name=name, npc_health=health)
    new_npc.save()

    return HttpResponseRedirect(reverse('npc:index'))


def edit_npc(request, pk):
    npc = get_object_or_404(Npc, pk=pk)
    hp_mod = request.POST['health_mod']
    if hp_mod is not '' and int(hp_mod) > 0:
        dmgh = json.loads(npc.npc_damage_history)
        if 'dmg_history' not in dmgh:
            dmgh.update({"dmg_history": []})

        if 'heal' in request.POST:
            npc.npc_health += int(hp_mod)
            dmgh['dmg_history'].append(str('+'+hp_mod))
        else:
            npc.npc_health -= int(hp_mod)
            dmgh['dmg_history'].append(str('-' + hp_mod))
        npc.npc_damage_history = json.dumps(dmgh)
        npc.save()

    return HttpResponseRedirect(reverse('npc:index'))


def del_npc(request, pk):
    npc = get_object_or_404(Npc, pk=pk)
    npc.delete()
    return HttpResponseRedirect(reverse('npc:index'))


def add_player(request):
    name = request.POST['player_name']

    np = Player(player_name=name)
    np.save()

    return HttpResponseRedirect(reverse('npc:index'))


def del_player(request, pk):
    dp = get_object_or_404(Player, pk=pk)
    dp.delete()

    return HttpResponseRedirect(reverse('npc:index'))