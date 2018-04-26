from django import forms
from .models import Tube, Freezer, Compartment, Rack, Rackmodule, Box, Tube, BioSample, Type, Document
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms.forms import NON_FIELD_ERRORS


# The freezer form
class FreezerForm(forms.ModelForm):
    class Meta:
        model = Freezer
        fields = '__all__'

# The Compartment Form
class CompartmentForm(forms.ModelForm):

    error_messages = {
        'freezer_full': 'The freezer is full'
    }

    class Meta:
        model = Compartment
        fields = '__all__'

    def clean_freezer(self):
        data = self.cleaned_data['freezer']
        freezer_id = self.data.get('freezer')
        full = int(Compartment.objects.filter(freezer_id=freezer_id).count())
        #Check freezzer isnt full.
        if int(data.space) <= full:
            print(self.get_form_kwargs)
            msg = self.error_messages['freezer_full']
            self.add_error(NON_FIELD_ERRORS, msg)

        # Remember to always return the cleaned data.
        return data

class CompartmentUpdateForm(forms.ModelForm):

    class Meta:
        model = Compartment
        fields = '__all__'


# The rack form
class RackForm(forms.ModelForm):

    error_messages = {
        'compartment_full': 'The compartment is full'
    }

    class Meta:
        model = Rack
        fields = '__all__'

    # Im Moment nimmt eine lose Box genauso viel Platz weg wie ein Rack, dass passt noch nicht so genau. Man koennte die Boxen 0,1 groß sein lassen koennen
    # aber das ist erstmal weniger wichtig sollte aber fuer spaeter richtig angepasst werden
    def clean_compartment(self):
        data = self.cleaned_data['compartment']
        compartment_id = self.data.get('compartment')
        full = int(Rack.objects.filter(compartment_id=compartment_id).count()) + int(Box.objects.filter(compartment_id=compartment_id).filter(rack_id__isnull='True').count())
        #Check compartment isnt full.
        if int(data.space) < full+1:
            msg = self.error_messages['compartment_full']
            self.add_error(NON_FIELD_ERRORS, msg)

        # Remember to always return the cleaned data.
        return data

# The rackmodule form
class RackmoduleForm(forms.ModelForm):

    error_messages = {
        'rack_full': 'The rack is full'
    }

    class Meta:
        model = Rackmodule
        fields = '__all__'

    def clean_rack(self):
        data = self.cleaned_data['rack']
        rack_id = self.data.get('rack')
        full = int(Rackmodule.objects.filter(rack_id=rack_id).count())
        #Check rack isnt full.
        if int(data.space) < full+1:
            msg = self.error_messages['rack_full']
            self.add_error(NON_FIELD_ERRORS, msg)

        # Remember to always return the cleaned data.
        return data

# The tube form
class BoxRackForm(forms.ModelForm):

    error_messages = {
        'rackmodule_full': 'The rackmodule is full'
    }

    class Meta:
        model = Box
        fields = '__all__'

    def clean_rackmodule(self):
        data = self.cleaned_data['rackmodule']
        rackmodule_id = self.data.get('rackmodule')
        full = int(Box.objects.filter(rackmodule_id=rackmodule_id).count())
        #Check compartment isnt full.
        if int(data.space) < full+1:
            msg = self.error_messages['rackmodule_full']
            self.add_error(NON_FIELD_ERRORS, msg)
        # Remember to always return the cleaned data.
        return data

    def __init__(self, *args, **kwargs):
        super(BoxRackForm, self).__init__(*args, **kwargs)

        #Create a new queryset for compartment so you can only choose the compartments which are part of the choosen freezer
        if 'freezer' in self.data:
            try:
                freezer_id = int(self.data.get('freezer'))
                self.fields['compartment'].queryset = Compartment.objects.filter(freezer_id=freezer_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['compartment'].queryset = self.instance.freezer.compartment_set.order_by('name')

        #Create a new queryset for rack so you can only choose the racks which are part of the choosen compartment
        if 'compartment' in self.data:
            try:
                compartment_id = int(self.data.get('compartment'))
                self.fields['rack'].queryset = Rack.objects.filter(compartment_id=compartment_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['rack'].queryset = self.instance.compartment.rack_set.order_by('name')

        #Create a new queryset for rackmodule so you can only choose the rackmodules which are part of the choosen rack
        if 'rack' in self.data:
            try:
                rack_id = int(self.data.get('rack'))
                self.fields['rackmodule'].queryset = Rackmodule.objects.filter(rack_id=rack_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['rackmodule'].queryset = self.instance.rack.rackmodule_set.order_by('name')

class BoxCompartmentForm(forms.ModelForm):

    error_messages = {
        'compartment_full': 'The compartment is full'
    }

    class Meta:
        model = Box
        fields = ['name','space','freezer','compartment']

    def clean_compartment(self):
        data = self.cleaned_data['compartment']
        compartment_id = self.data.get('compartment')
        full = int(Rack.objects.filter(compartment_id=compartment_id).count()) + int(Box.objects.filter(compartment_id=compartment_id).filter(rack_id__isnull='True').count())
        #Check compartment isnt full.
        if int(data.space) < full+1:
            msg = self.error_messages['compartment_full']
            self.add_error(NON_FIELD_ERRORS, msg)

        # Remember to always return the cleaned data.
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'freezer' in self.data:
            try:
                freezer_id = int(self.data.get('freezer'))
                self.fields['compartment'].queryset = Compartment.objects.filter(freezer_id=freezer_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['compartment'].queryset = self.instance.freezer.compartment_set.order_by('name')

# The tube form
class TubeForm(forms.ModelForm):

    error_messages = {
        'box_full': 'The box is full',
        # Error when if an other tube has already the place of the new tube
        'is_occupied': 'The Place is occupied',
    }

    class Meta:
        model = Tube
        fields = '__all__'

    def clean_box(self):
        data = self.cleaned_data['box']
        box_id = self.data.get('box')
        full = int(Tube.objects.filter(box_id=box_id).count())
        #Check box isnt full.
        if int(data.space) < full+1:
            msg = self.error_messages['box_full']
            self.add_error(NON_FIELD_ERRORS, msg)
        # Remember to always return the cleaned data.
        return data

# The biosample form
class BioSampleForm(forms.ModelForm):
    class Meta:
        model = BioSample
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contactPerson'].label = "Contact person"
        self.fields['commentstep'].label = "Comment to the steps"
        self.fields['commentaliquot'].label = "Comment to the aliquot"

# The type form
class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'

# To upload files
class DocumentForm(forms.ModelForm):
    error_messages = {
        'wrong_input': 'The input format is wrong. Please use csv files.',
    }

    class Meta:
        model = Document
        fields = ['box', 'document']

    def clean_document(self):
        data = self.cleaned_data['document']
        #Check file format.
        if str(data)[-3:] != 'csv':
            msg = self.error_messages['wrong_input']
            self.add_error(NON_FIELD_ERRORS, msg)
        # Remember to always return the cleaned data.
        return data
