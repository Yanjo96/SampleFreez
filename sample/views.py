from django.shortcuts import render
from .models import Freezer, Compartment, Rack, Rackmodule, Box, Tube, BioSample, Type
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .forms import FreezerForm, CompartmentForm, RackForm, RackmoduleForm, BoxCompartmentForm, BoxRackForm, TubeForm, BioSampleForm, TypeForm
import operator

from django.db.models import Q
from functools import reduce

def index(request):
    # View function for home page of site.
    # Generate counts of some of the main objects
    num_freezer=Freezer.objects.all().count()
    num_biosample=BioSample.objects.all().count()

    #Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_freezer':num_freezer,'num_biosample':num_biosample,}
    )

# Um nur ein Compartment auzuwählen das auch im dazugehörigen Freezer liegt und nicht
# eins random genommen werden kann
def load_compartments(request):
    freezer_id = request.GET.get('freezer')
    compartments = Compartment.objects.filter(freezer_id=freezer_id).order_by('name')
    return render(request, 'sample/compartment/compartment_dropdown_list_options.html', {'compartments': compartments})

def popup(request):
    return render(request, 'sample/type/type_form.html')

# Um nur ein Rack auzuwählen das auch im dazugehörigen Compartment liegt und nicht
# eins random genommen werden kann
def load_racks(request):
    compartment_id = request.GET.get('compartment')
    racks = Rack.objects.filter(compartment_id=compartment_id).order_by('name')
    return render(request, 'sample/rack/rack_dropdown_list_options.html', {'racks': racks})

def load_rackmodules(request):
    rack_id = request.GET.get('rack')
    rackmodules = Rackmodule.objects.filter(rack_id=rack_id).order_by('name')
    return render(request, 'sample/rackmodule/rackmodule_dropdown_list_options.html', {'rackmodules': rackmodules})


"""
Freezer view
"""
class FreezerListView(LoginRequiredMixin, generic.ListView):
    template_name = 'sample/freezer/freezer_list.html'
    model = Freezer
    paginate_by = 10

class FreezerDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sample/freezer/freezer_detail.html'
    model = Freezer

class FreezerCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_freezer'
    model = Freezer
    template_name = 'sample/freezer/freezer_form.html'
    form_class = FreezerForm

class FreezerUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_freezer'
    template_name = 'sample/freezer/freezer_form.html'
    model = Freezer
    form_class = FreezerForm

class FreezerDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_freezer'
    template_name = 'sample/freezer/freezer_confirm_delete.html'
    model = Freezer
    success_url = reverse_lazy('freezer')

"""
Compartment view
"""
class CompartmentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sample/compartment/compartment_detail.html'
    model = Compartment


class CompartmentCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_compartment'
    model = Compartment
    template_name = 'sample/compartment/compartment_form.html'
    form_class = CompartmentForm

    def get_initial(self):
        return {
            'freezer':Freezer.objects.get(pk=self.kwargs['freezer']),
        }

class CompartmentUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_compartment'
    template_name = 'sample/compartment/compartment_form.html'
    model = Compartment
    form_class = CompartmentForm

class CompartmentDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_compartment'
    template_name = 'sample/compartment/compartment_confirm_delete.html'
    model = Compartment
    success_url = reverse_lazy('freezer')

"""
Rack view
"""
class RackDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sample/rack/rack_detail.html'
    model = Rack

class RackCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_rack'
    model = Rack
    template_name = 'sample/rack/rack_form.html'
    form_class = RackForm

    def get_initial(self):
        return {
            'freezer':Freezer.objects.get(pk=self.kwargs['freezer']),
            'compartment':Compartment.objects.get(pk=self.kwargs['compartment']),
        }

class RackUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_rack'
    template_name = 'sample/rack/rack_form.html'
    model = Rack
    form_class = RackForm

class RackDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_rack'
    template_name = 'sample/rack/rack_confirm_delete.html'
    model = Rack
    success_url = reverse_lazy('freezer')

"""
Rackmodule view
"""
class RackmoduleDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sample/rackmodule/rackmodule_detail.html'
    model = Rackmodule

class RackmoduleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_rackmodule'
    model = Rackmodule
    template_name = 'sample/rackmodule/rackmodule_form.html'
    form_class = RackmoduleForm

    def get_initial(self):
        return {
            'freezer':Freezer.objects.get(pk=self.kwargs['freezer']),
            'compartment':Compartment.objects.get(pk=self.kwargs['compartment']),
            'rack':Rack.objects.get(pk=self.kwargs['rack']),
        }

class RackmoduleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_rackmodule'
    template_name = 'sample/rackmodule/rackmodule_form.html'
    model = Rackmodule
    form_class = RackmoduleForm

class RackmoduleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_rackmodule'
    template_name = 'sample/rackmodule/rackmodule_confirm_delete.html'
    model = Rackmodule
    success_url = reverse_lazy('freezer')

"""
Box view
"""
class BoxRackDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sample/box/box_detail.html'
    model = Box

class BoxRackCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_box'
    model = Box
    template_name = 'sample/box/box_form.html'
    form_class = BoxRackForm

    def get_initial(self):
        return {
            'freezer':Freezer.objects.get(pk=self.kwargs['freezer']),
            'compartment':Compartment.objects.get(pk=self.kwargs['compartment']),
            'rack':Rack.objects.get(pk=self.kwargs['rack']),
            'rackmodule':Rackmodule.objects.get(pk=self.kwargs['rackmodule'])
        }

    def get_success_url(self):
        return reverse('rackmodule-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['rack'],self.kwargs['rackmodule']])

class BoxRackUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_box'
    template_name = 'sample/box/box_form.html'
    model = Box
    form_class = BoxRackForm

    def get_success_url(self):
        return reverse('box-r-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['rack'],self.kwargs['rackmodule'],self.kwargs['pk']])

class BoxRackDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_box'
    template_name = 'sample/box/box_confirm_delete.html'
    model = Box

    def get_success_url(self):
        return reverse('rackmodule-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['rack'],self.kwargs['rackmodule']])

class BoxCompartmentDetailView(generic.DetailView):
    template_name = 'sample/box/box_detail.html'
    model = Box

class BoxCompartmentCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_box'
    model = Box
    template_name = 'sample/box/box_form.html'
    form_class = BoxCompartmentForm

    def get_initial(self):
        return {
            'freezer':Freezer.objects.get(pk=self.kwargs['freezer']),
            'compartment':Compartment.objects.get(pk=self.kwargs['compartment']),
        }

    def get_success_url(self):
        return reverse('compartment-detail', args=[self.kwargs['freezer'],self.kwargs['compartment']])

class BoxCompartmentUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_box'
    template_name = 'sample/box/box_form.html'
    model = Box
    form_class = BoxCompartmentForm

    def get_success_url(self):
        return reverse('box-c-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['pk']])

class BoxCompartmentDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_box'
    template_name = 'sample/box/box_confirm_delete.html'
    model = Box

    def get_success_url(self):
        return reverse('compartment-detail', args=[self.kwargs['freezer'],self.kwargs['compartment']])

"""
Tube view
"""
class TubeRackDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sample/tube/tube_detail.html'
    model = Tube

class TubeRackCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_tube'
    model = Tube
    template_name = 'sample/tube/tube_form.html'
    form_class = TubeForm

    def get_initial(self):
        return {
            'freezer':Freezer.objects.get(pk=self.kwargs['freezer']),
            'compartment':Compartment.objects.get(pk=self.kwargs['compartment']),
            'rack':Rack.objects.get(pk=self.kwargs['rack']),
            'rackmodule':Rackmodule.objects.get(pk=self.kwargs['rackmodule']),
            'box':Box.objects.get(pk=self.kwargs['box'])
        }

    def get_success_url(self):
        return reverse('box-r-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['rack'],self.kwargs['rackmodule'],self.kwargs['box']])

class TubeRackUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_tube'
    template_name = 'sample/tube/tube_form.html'
    model = Tube
    form_class = TubeForm

    def get_success_url(self):
        return reverse('tube-r-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['rack'],self.kwargs['rackmodule'],self.kwargs['box'],self.kwargs['pk']])

class TubeRackDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_tube'
    template_name = 'sample/tube/tube_confirm_delete.html'
    model = Tube

    def get_success_url(self):
        return reverse('box-r-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['rack'],self.kwargs['rackmodule'],self.kwargs['box']])

class TubeCompartmentDetailView(generic.DetailView):
    template_name = 'sample/tube/tube_detail.html'
    model = Tube

class TubeCompartmentCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_tube'
    model = Tube
    template_name = 'sample/tube/tube_form.html'
    form_class = TubeForm

    def get_initial(self):
        return {
            'freezer':Freezer.objects.get(pk=self.kwargs['freezer']),
            'compartment':Compartment.objects.get(pk=self.kwargs['compartment']),
            'box':Box.objects.get(pk=self.kwargs['box'])
        }

    def get_success_url(self):
        return reverse('box-c-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['box']])

class TubeCompartmentUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_tube'
    template_name = 'sample/tube/tube_form.html'
    model = Tube
    form_class = TubeForm

    def get_success_url(self):
        return reverse('tube-c-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['box'],self.kwargs['pk']])

class TubeCompartmentDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_tube'
    template_name = 'sample/tube/tube_confirm_delete.html'
    model = Tube
    success_url = reverse_lazy('freezer')

    def get_success_url(self):
        return reverse('box-c-detail', args=[self.kwargs['freezer'],self.kwargs['compartment'],self.kwargs['box']])

class TubeBiosampleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_tube'
    model = Tube
    template_name = 'sample/tube/tube_form.html'
    form_class = TubeForm

    def get_success_url(self):
        return reverse('biosample-detail', args=[self.kwargs['biosample']])

"""
BioSample view
"""
class BioSampleListView(LoginRequiredMixin, generic.ListView):
    template_name = 'sample/biosample/biosample_list.html'
    model = BioSample
    paginate_by = 10

class BioSampleDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sample/biosample/biosample_detail.html'
    model = BioSample

class BioSampleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_biosample'
    model = BioSample
    template_name = 'sample/biosample/biosample_form.html'
    form_class = BioSampleForm

class BioSampleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_biosample'
    template_name = 'sample/biosample/biosample_form.html'
    model = BioSample
    fields = '__all__'

class BioSampleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_biosample'
    template_name = 'sample/biosample/biosample_confirm_delete.html'
    model = BioSample
    success_url = reverse_lazy('biosample')

"""
Type view
"""
class TypeListView(LoginRequiredMixin, generic.ListView):
    template_name = 'sample/type/type_list.html'
    model = Type

class TypeDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sample/type/type_detail.html'
    model = Type

class TypeCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'sample.add_type'
    model = Type
    template_name = 'sample/type/type_form.html'
    form_class = TypeForm

class TypeUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'sample.change_type'
    template_name = 'sample/type/type_form.html'
    model = Type
    form_class = TypeForm

    def dispatch(self, *args, **kwargs):
        self.type_id = kwargs['pk']
        return super(TypeUpdate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        type = Type.objects.get(id=self.type_id)
        return HttpResponse(render_to_string('sample/type/type_edit_form_success.html', {'type': type}))

class TypeDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'sample.delete_type'
    template_name = 'sample/type/type_confirm_delete.html'
    model = Type
    success_url = reverse_lazy('type')

"""
Searchbar
"""
class AllListView(generic.ListView):
    template_name = "sample/all_list.html"
    model = Freezer

class SearchListView(LoginRequiredMixin, AllListView):
    """
    Display a Freezer List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(SearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )

        return result

    def get_context_data(self,**kwargs):
        query = self.request.GET.get('q')
        print(query)
        context = super(AllListView, self).get_context_data(**kwargs)
        if query:
            query_list = query.split()
            context['compartment_list'] = Compartment.objects.filter(reduce(operator.and_,(Q(name__icontains=q) for q in query_list)))
            context['rack_list'] = Rack.objects.filter(reduce(operator.and_,(Q(name__icontains=q) for q in query_list)))
            context['rackmodule_list'] = Rackmodule.objects.filter(reduce(operator.and_,(Q(name__icontains=q) for q in query_list)))
            context['box_list'] = Box.objects.filter(reduce(operator.and_,(Q(name__icontains=q) for q in query_list)))
            context['tube_list'] = Tube.objects.filter(reduce(operator.and_,(Q(name__icontains=q) for q in query_list)))
            context['biosample_list'] = BioSample.objects.filter(reduce(operator.and_,(Q(name__icontains=q) for q in query_list)))
            context['type_list'] = Type.objects.filter(reduce(operator.and_,(Q(name__icontains=q) for q in query_list)))
            context['user_list'] = User.objects.filter(reduce(operator.and_,(Q(username__icontains=q) for q in query_list)))
        return context
