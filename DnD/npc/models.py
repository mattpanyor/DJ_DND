from django.db import models

# Create your models here.

class Npc(models.Model):
    npc_name = models.CharField(max_length=50)
    npc_health = models.IntegerField()
    npc_damage_history = models.TextField(default="{}", blank=True)

    def __str__(self):
        return self.npc_name
