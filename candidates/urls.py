

from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    ### this is for receiving the newcands, no output for browser
    path('newcand/', views.AddCandidate, name='newcand'),
    path('veto/', views.GetVeto, name='veto'),
    path('mma/', views.MMAUpdates, name='Multimessenger Update'),
    path('slack/',views.Slack,name='Slack response handler'),
    ####
    path('<int:question_id>/', views.Detail, name='detail')
]



"""
urlpatterns = [
    # ex: /candidates/
    path('', views.index, name='index'),
    path('newcand/', views.add_candidate, name='newcand'), ### this is for receiving the newcands, no output for browser
    path('veto/', views.veto, name='veto'), ### this is for receiving the newcands, no output for browser
    # ex: /candidates/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /candidates/5/info/
    # path('<int:question_id>/info/', views.info, name='info'), ## extensive info page?

]
"""
