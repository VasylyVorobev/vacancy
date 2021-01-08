from django.urls import path
from django.views.decorators.http import require_POST

from . import views

urlpatterns = [
    path('resume/create/', views.ResumeCreatedView.as_view(), name='create_resume_url'),
    path('resume/<str:slug>/update/', views.ResumeUpdateView.as_view(), name='update_resume_url'),
    path('resume/empty/', views.empty_resume, name='empty_resume_url'),
    # path('resume/sent_letter/', require_POST(views.ApplicationView.as_view()), name='sent_letter_url'),
    path('resume/success_sent/', views.success_sent, name='success_sent_url'),
    path('company/create/', views.CreateCompany.as_view(), name='create_company_url'),
    path('vacancy/create', views.CreateVacancy.as_view(), name='create_vacancy_url'),
    path('vacancy/list', views.VacancyListView.as_view(), name='list_of_my_vacancy_url'),
    path('vacancy/<str:slug>/update/', views.UpdateVacancyView.as_view(), name='update_vacancy_url'),
    path('company/empty/', views.empty_company, name='empty_company_url'),
    path('company/<str:slug>/update/', views.UpdateCompanyView.as_view(), name='update_company_url'),
    path('', views.IndexView.as_view(), name='main'),
    # path('search/', views.IndexView.as_view(), name='search'),
    path('vacancy/all', views.AllVacancy.as_view(), name='all_vacancy'),
    path('vacancy/<str:slug>/', views.VacancyList.as_view(), name='list_vacancy_url'),
    path('vacancy_detail/<str:slug>/', views.VacancyDetail.as_view(), name='detail_vacancy_url'),
    path('company/<str:slug>/', views.CompanyDetail.as_view(), name='detail_company_url'),
]
