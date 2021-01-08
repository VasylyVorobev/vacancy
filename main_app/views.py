from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView, FormView
from django.views.generic.edit import FormMixin
from .models import Company, Vacancy, Specialty, Resume
from django.views.generic.base import View
from .forms import CreateCompanyForm, CreateVacancyForm, CreateResumeForm, ApplicationForm


class BaseView(View):

    def get(self, request):
        return render(request, 'main/base.html')


class IndexView(View):

    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            result = Vacancy.objects.filter(
                Q(title__icontains=search_query) |
                Q(specialty__code__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            return render(request, 'main/result_list.html', {'result': result})
        else:
            rubric = Specialty.objects.all()
            company = Company.objects.all()[:8]
            vacancy = Vacancy.objects.all()
            return render(request, 'main/index.html', {'rubric': rubric, 'company': company, 'vacancy': vacancy})


class VacancyList(View):

    def get(self, request, slug):
        vacancies = Vacancy.objects.filter(specialty__code=slug)
        specialty = Specialty.objects.get(code=slug)
        return render(request, 'main/vacancy_list.html', {'vacancies': vacancies,
                                                          'spec': specialty.get_title_display()})


class AllVacancy(ListView):
    model = Vacancy
    template_name = 'main/all_vacancy.html'


def success_sent(request):
    vacancy = Vacancy.objects.all()
    return render(request, 'resume/success_sent.html', {'vacancy': vacancy})


class VacancyDetail(FormMixin, DetailView):
    model = Vacancy
    template_name = 'main/vacancy_detail.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('success_sent_url')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.vacancy = self.get_object()
        self.object.save()
        return super(VacancyDetail, self).form_valid(form)


class CompanyDetail(DetailView):
    model = Company
    template_name = 'main/company_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetail, self).get_context_data(**kwargs)
        context['vacancy'] = Vacancy.objects.filter(company=self.object)
        return context


def empty_company(request):
    return render(request, 'company/empty_company.html')


class CreateCompany(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'company/company_create.html'
    form_class = CreateCompanyForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateCompany, self).form_valid(form)


class UpdateCompanyView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'company/company_update.html'
    fields = ['title', 'location', 'logo', 'description', 'employee_count']


class CreateVacancy(LoginRequiredMixin, CreateView):
    model = Vacancy
    template_name = 'vacancy/create_vacancy.html'
    form_class = CreateVacancyForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.company = self.request.user.company_set.first()
        self.object.save()
        return super().form_valid(form)


class UpdateVacancyView(LoginRequiredMixin, UpdateView):
    model = Vacancy
    template_name = 'vacancy/vacancy_update.html'
    fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']


class VacancyListView(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'vacancy/create_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyListView, self).get_context_data(**kwargs)
        context['vacancy'] = Vacancy.objects.filter(company__title=self.request.user.company_set.first())
        return context


def empty_resume(request):
    return render(request, 'resume/resume_empty.html')


class ResumeCreatedView(LoginRequiredMixin, CreateView):
    model = Resume
    template_name = 'resume/resume_created.html'
    form_class = CreateResumeForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(ResumeCreatedView, self).form_valid(form)


class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    model = Resume
    template_name = 'resume/resume_update.html'
    form_class = CreateResumeForm
