from django.contrib import admin
from .models import Freezer, Compartment, Rack, Rackmodule, Box, Tube, BioSample, Type

admin.site.register(Freezer)
admin.site.register(Compartment)
admin.site.register(Rack)
admin.site.register(Rackmodule)
admin.site.register(Box)
admin.site.register(Tube)
admin.site.register(Type)

@admin.register(BioSample)
class BioSampleAdmin(admin.ModelAdmin):
    list_display = (
                    'name',
                    'whoose',
                    'contactPerson',
                    'type',
                    'state',
                    'sober',
                    'centrifugate',
                    'pipet',
                    'commentstep',
                    'plasma',
                    'plasmanumber',
                    'seroes',
                    'seroesnumber',
                    'commentaliquot',
                    'aliquot',
                    'tubes',
                    'transfer',
                    )
    fields = (
                    'name',
                    'whoose',
                    'contactPerson',
                    'type',
                    'state',
                    'sober',
                    'centrifugate',
                    'pipet',
                    'commentstep',
                    ('plasma','plasmanumber'),
                    ('seroes','seroesnumber'),
                    'commentaliquot',
                    'aliquot',
                    'tubes',
                    'transfer',
                )
