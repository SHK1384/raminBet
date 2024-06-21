from django.contrib import admin
from django.contrib.admin import SimpleListFilter, ModelAdmin
from .models import *
import datetime

# Register your models here.
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Prediction)
admin.site.register(FinalistPrediction)
admin.site.register(ChampionPrediction)

class MatchListFilter(admin.SimpleListFilter):
    title = "Today"

    parameter_name = "date"

    def lookups(self, request, model_admin):
        return [
            ("today", "today")
        ]

    def queryset(self, request, queryset):
        if self.value() == "today":
            return queryset.filter(
                date__gte=datetime.date.today()
            )

class MatchAdmin(admin.ModelAdmin):
    list_filter = (MatchListFilter,)

admin.site.register(Match, MatchAdmin)