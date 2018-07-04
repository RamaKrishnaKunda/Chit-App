from django.views.generic import ListView, CreateView, DeleteView
from django.views import View
from chit_app.models import *
from django import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from chit_app.forms import *
from django.shortcuts import redirect, render

class ChitList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Chit
    template_name = 'chitlist.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChitList, self).get_context_data(**kwargs)
        if self.request.user.get_all_permissions():
            context['has_perm'] = True
            context['chit_list'] = Chit.objects.values('id', 'name', 'month', 'year', 'amount', 'number_of_months', 'people_present')
        else:
            context['has_perm'] = False
            user = self.request.user
            context['chit_list'] = Lifted.objects.values('chit__id', 'chit__month', 'chit__year', 'chit__amount').filter(user__id = user.id).distinct()
            # all_chits = Lifted.objects.values('chit__id').filter(user__id = user.id).distinct()
        return context

class AddChit(LoginRequiredMixin, CreateView):
    login_url = '/login'
    template_name = 'addchit_form.html'
    form_class = AddChitForm
    model = Chit
    success_url = urls.reverse_lazy('chit_app:chitlist')

    def get_context_data(self, **kwargs):
        context = super(AddChit, self).get_context_data(**kwargs)
        form = AddChitForm()
        context.update({'form': form})
        return context

    def post(self, request, *args, **kwargs):
        form = AddChitForm(request.POST)
        if form.is_valid():
            chit = form.save(commit = False)
            chit.people_present = 0
            chit.save()
            return redirect('chit_app:chitlist')
        else:
            context = {'form': AddChitForm(), **form.errors}
            return render(request=request, template_name='addchit_form.html', context=context)

class AddPeople(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        form = AddPersonForm()
        return render(request=request, template_name='addpeopletemplate.html', context={'form':form, 'UserPresent': True, 'ChitsAvaiable' : True})

    def post(self, request, **kwargs):
        form = AddPersonForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            number_of_chits = form.cleaned_data['num_of_chits']
            chit_obj = Chit.objects.get(id=kwargs['chit_id'])
            if chit_obj.people_present + number_of_chits > chit_obj.number_of_months:
                return render(request=request, template_name='addpeopletemplate.html', context={'form':form, 'UserPresent': True, 'ChitsAvaiable' : False})
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                return render(request=request, template_name='addpeopletemplate.html', context={'form':form, 'UserPresent': False, 'ChitsAvaiable' : True})
            for iter in range(number_of_chits):
                lifted_obj = Lifted(user = user, chit = chit_obj)
                lifted_obj.amount = chit_obj.amount // chit_obj.number_of_months
                # import ipdb
                # ipdb.set_trace()
                lifted_obj.save()
                chit_obj.people_present += 1
            chit_obj.save()
            if chit_obj.people_present < chit_obj.number_of_months:
                return redirect('chit_app:addpeople', **kwargs)
            else:
                return redirect('chit_app:chitlist')

class ViewPeople(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = User
    template_name = 'viewpeople.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewPeople, self).get_context_data(**kwargs)
        context['users'] = Lifted.objects.values('user__first_name','user__last_name', 'lifted', 'lift_request', 'id').filter(chit__id = self.kwargs['chit_id'])
        return context

class DeleteChit(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Chit
    template_name = 'chit_delete.html'
    success_url = urls.reverse_lazy('chit_app:chitlist')

class ViewUserChits(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Chit
    template_name = 'viewuserchits.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewUserChits, self).get_context_data(**kwargs)
        user = self.request.user
        if not Lifted.objects.all().filter(user__id = user.id, chit__id = self.kwargs['chit_id']):
            return None
        context['chitlist'] = Lifted.objects.values('id', 'lifted', 'lift_request', 'chit__amount', 'chit__number_of_months', 'amount').filter(user__id = user.id).filter(chit__id = self.kwargs['chit_id'])
        context['chitid'] = self.kwargs['chit_id']
        return context

class RequestLift(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, **kwargs):
        user = request.user
        lift_obj = Lifted.objects.get(id = kwargs['lifted_id'])
        lift_obj.lift_request = 1
        lift_obj.save()
        return redirect('chit_app:userchitview', **{'chit_id': self.kwargs['chit_id']})

class ConfirmLift(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request, **kwargs):
        user = request.user
        lift_obj = Lifted.objects.get(id=kwargs['lifted_id'])
        lift_obj.lifted = True
        lift_obj.lift_request = 2
        lift_obj.amount += 1000
        lift_obj.save()
        lift_objs = Lifted.objects.all().filter(chit__id = kwargs['chit_id'])
        for lift_obj in lift_objs:
            if lift_obj.lift_request == 1:
                lift_obj.lift_request = 0
                lift_obj.save()
        return redirect('chit_app:viewpeople', **{'chit_id': self.kwargs['chit_id']})

def RemoveRequests(request, **kwargs):
    lift_objs = Lifted.objects.all().filter(chit__id=kwargs['chit_id'])
    for lift_obj in lift_objs:
        if lift_obj.lift_request == 1:
            lift_obj.lift_request = 0
            lift_obj.save()
    return redirect('chit_app:viewpeople', **{'chit_id': kwargs['chit_id']})

def First_page_view(request):
    return render(request = request, template_name='_base.html', context = {'firstpage': True})