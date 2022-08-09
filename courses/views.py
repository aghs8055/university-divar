import markdown
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, ContactUsForm, ProfileSettingsForm
from django.views.generic import FormView, CreateView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Profile
from django import forms
from django.db.models import Q


def homepage(request):
    return HttpResponse(render(request, 'courses/homepage.html'))


def create_user(data):
    username, email = data['username'], data['email']
    first_name, last_name = data['first_name'], data['last_name']
    user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    user.set_password(data['password'])
    user.save()
    return user


def user_signup(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        return HttpResponse(render(request, 'courses/register.html', context={'form': form}))
    elif request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if not form.is_valid():
            return HttpResponse(
                render(request, 'courses/register.html', context={'form': form}))

        user = form.save()
        profile = Profile.objects.create(user=user)
        user.profile = profile
        user.save()
        return HttpResponseRedirect(reverse('courses:homepage'))


def user_login(request):
    if request.method == 'GET':
        return HttpResponse(render(request, 'courses/login.html'))
    if request.method == 'POST':
        username, password = request.POST.get('username'), request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('courses:homepage'))
        else:
            return HttpResponse(
                render(request, 'courses/login.html', context={'error_message': 'Invalid Username or password'}))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('courses:homepage'))


class ContactUs(FormView):
    template_name = 'courses/contact-us.html'
    form_class = ContactUsForm
    success_url = '/thanks'

    def form_valid(self, form):
        form.send_mail()
        return super(ContactUs, self).form_valid(form)


def thanks(request):
    return HttpResponse(render(request, 'courses/thanks.html'))


@login_required()
def profile_view(request):
    return HttpResponse(render(request, 'courses/profile_view.html'))


@login_required()
def panel(request):
    return HttpResponse(render(request, 'courses/panel.html'))


class ProfileSettings(LoginRequiredMixin, FormView):
    template_name = 'courses/profile_settings.html'
    form_class = ProfileSettingsForm
    success_url = '/profile'

    def form_valid(self, form):
        first_name, last_name = form.cleaned_data.get('first_name', ''), form.cleaned_data.get('last_name', '')
        if first_name != '':
            self.request.user.first_name = first_name
        if last_name != '':
            self.request.user.last_name = last_name
        self.request.user.profile.image = form.cleaned_data.get('image', None)
        self.request.user.profile.bio = markdown.markdown(form.cleaned_data.get('bio', None))
        self.request.user.profile.gender = form.cleaned_data.get('gender', None)
        self.request.user.profile.user_type = form.cleaned_data.get('user_type', None)
        self.request.user.save()
        self.request.user.profile.save()
        return super(ProfileSettings, self).form_valid(form)

    def get_form(self, form_class=None):
        form = super(ProfileSettings, self).get_form()
        form.initial['first_name'] = self.request.user.first_name
        form.initial['last_name'] = self.request.user.last_name
        form.initial['image'] = self.request.user.profile.image
        form.initial['bio'] = self.request.user.profile.bio
        form.initial['gender'] = self.request.user.profile.gender
        form.initial['user_type'] = self.request.user.profile.user_type
        return form


@method_decorator(staff_member_required, name='dispatch')
class AddCourse(CreateView):
    model = Course
    fields = '__all__'
    template_name = 'courses/add_course.html'
    success_url = '/panel'

    def get_form(self, form_class=None):
        form = super(AddCourse, self).get_form(form_class)
        form.fields['start_time'].widget = forms.TimeInput()
        form.fields['end_time'].widget = forms.TimeInput()
        return form


class CourseList(ListView):
    model = Course
    template_name = 'courses/courses.html'
    context_object_name = 'courses'
    paginate_by = 5


class TeacherSearch(ListView):
    model = User
    template_name = 'courses/teacher_search.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = User.objects.filter(profile__user_type='T')
        queryset = queryset.filter(
            Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        return queryset
