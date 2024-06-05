from django.urls import path
from .views import CompetitionListView, CompetitionDetailView, CompetitionApplyView, PartnerSearchView, CompetitionApplyResultView, MyCompetitionListView
# CompetitionApplyAPIView

urlpatterns = [
    path('competitions/', CompetitionListView.as_view(), name='competitions'),
    path('competitions/<int:pk>/details/', CompetitionDetailView.as_view(), name='competition'),
    path('competitions/<int:pk>/apply/', CompetitionApplyView.as_view(), name='competition-apply'),
    path('competitions/<int:pk>/partnersearch/', PartnerSearchView.as_view(), name='partner-search'),
    path('competitions/<int:pk>/application/', CompetitionApplyResultView.as_view(), name='competition-application'),
    path('competitions/mycompetitions/', MyCompetitionListView.as_view(), name='my-competitions')
]