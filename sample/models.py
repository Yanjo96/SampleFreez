from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.urls import reverse # Used to generate urls by reversing the URL pattern
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid
from datetime import date

"""
Model to add fields to the User Model
"""


"""
Model for upload files
"""
class Document(models.Model):
    box = models.CharField(max_length=50)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

"""
Model for the Freezer.
"""
class Freezer(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the freezer (e.g. Freezer 1)")
    temperature = models.IntegerField(help_text="Enter the temperature of the freezer (e.g. -80)")
    space = models.IntegerField(help_text="Enter how many compartments can store in the freezer")

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        # Returns the URL to access a particular freezer
        return reverse('freezer-detail',args=[str(self.id)])

    def __str__(self):
        return self.name

"""
Model for the compartment
"""
class Compartment(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the copartment (e.g. Compartment 1)")
    space = models.IntegerField(help_text="Enter how many racks/boxes can store in the compartment")
    freezer = models.ForeignKey('Freezer',on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        # Returns the URL to access a particular compartment
        return reverse('compartment-detail',args=[str(self.freezer.id),str(self.id)])

    def get_number_of_space(self):
        # Returns the taken place in the Compartment cause of you can store racks and boxes in it
        return int(Rack.objects.filter(compartment_id=self.id).count()) + int(Box.objects.filter(compartment_id=self.id).filter(rack_id__isnull='True').count())

    def __str__(self):
        return self.name

"""
Model for the Rack
"""
class Rack(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the rack (e.g. Rack 1)")
    space = models.IntegerField(help_text="Enter how many rackmodules can store in the rack")
    compartment = models.ForeignKey('Compartment',on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        # Returns the URL to access a particular rack
        return reverse('rack-detail',args=[str(self.compartment.freezer.id),str(self.compartment.id),str(self.id)])

    def __str__(self):
        return self.name

"""
Model for the Rackmodule
"""
class Rackmodule(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the rackmodule (e.g. Rackmodule 1)")
    space = models.IntegerField(help_text="Enter how many boxes can store in the rackmodule")
    rack = models.ForeignKey('Rack',on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse('rackmodule-detail',args=[str(self.rack.compartment.freezer.id),str(self.rack.compartment.id),str(self.rack.id),str(self.id)])

    def __str__(self):
        return self.name

"""
Model for the Box
"""
class Box(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the Box (e.g. Box 1)")
    space = models.IntegerField(help_text="Enter how many tubes can store in the box")
    freezer = models.ForeignKey('Freezer',on_delete=models.CASCADE)
    compartment = models.ForeignKey('Compartment',on_delete=models.CASCADE)
    #when the box is in the compartment you dont need a rack and a rackmodule cause of this there are 2 types of urls
    rack = models.ForeignKey('Rack',on_delete=models.CASCADE, blank=True,null=True)
    rackmodule = models.ForeignKey('Rackmodule', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(max_length=1000,help_text="Enter a comment if you want",blank=True)

    class Meta:
        ordering = ["name"]

    # If the Box is store in the rack you will nieed much more information in the url
    def get_absolute_rack_url(self):
        return reverse('box-r-detail',args=[str(self.freezer.id),str(self.compartment.id),str(self.rack.id),str(self.rackmodule.id),str(self.id)])

    #when the box is in the compartment you dont need a rack and a rackmodule
    def get_absolute_url(self):
        return reverse('box-c-detail',args=[str(self.freezer.id),str(self.compartment.id),str(self.id)])

    """
    To show the tubes in the right order like in the box you need a 2d array which you can display in the template
    """
    def sort_tubes(self):
        # if the box is empty self...[0] will return an error
        try:
            max_xvalue = self.tube_set.all().order_by('xvalue').reverse()[0].xvalue
            max_yvalue = self.tube_set.all().order_by('yvalue').reverse()[0].yvalue
        except:
            max_xvalue = 0
            max_yvalue = 0

        # create an empty arrow in the right size
        out = [ [ 'empty' for y in range( max_xvalue ) ] for x in range( max_yvalue ) ]

        for tube in self.tube_set.all():
            out[tube.yvalue-1][tube.xvalue-1] = tube

        return out

    def __str__(self):
        return self.name

"""
Model for the tube
"""
class Tube(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the rack (e.g. Tube 1)")
    box = models.ForeignKey('Box',on_delete=models.CASCADE,blank=True)
    xvalue = models.IntegerField(help_text="Enter the postion of the tube in the x coordinate", blank=True)
    yvalue = models.IntegerField(help_text="Enter the postion of the tube in the y coordinate", blank=True)
    biosample = models.ForeignKey('BioSample',on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(max_length=1000,help_text="Enter a comment if you want",blank=True)

    class Meta:
        ordering = ["xvalue","yvalue"]
        unique_together = (("xvalue", "yvalue","box"),)

    # Same as in the boxes, cause of the boexes where the tubes are can store directly in the compartment you will need a 2nd url
    def get_absolute_rack_url(self):
        # Returns the URL to access a particular tube
        return reverse('tube-r-detail',args=[str(self.box.freezer.id),str(self.box.compartment.id),str(self.box.rack.id),str(self.box.rackmodule.id),str(self.box.id),str(self.id)])

    #when the box is in the compartment you dont need a rack and a rackmodule
    def get_absolute_compartment_url(self):
        # Returns the URL to access a particular tube
        return reverse('tube-c-detail',args=[str(self.box.freezer.id),str(self.box.compartment.id),str(self.box.id),str(self.id)])

    def __str__(self):
        return self.name

"""
Model for the Biosample
"""
class BioSample(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the biosample (e.g. Biosample 1)")
    whoose = models.CharField(max_length=50, help_text="Enter the id whoose biosample is for (e.g. T1234)")
    contactPerson = models.CharField(max_length=100, help_text="Enter the contact person for this biosample")
    type = models.ForeignKey('Type',on_delete=models.CASCADE)

    #only when the type == Blood

    STATE_CHOICES = (
        ('lying','lying'),
        ('sitting','sitting'),
        ('standing','standing'),
    )
    state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True)

    SOBER_CHOICES = (
        ('sober','sober'),
        ('not sober','not sober'),
    )
    sober = models.CharField(max_length=50, choices=SOBER_CHOICES,blank=True)

    centrifugate = models.BooleanField(blank=True)
    pipet = models.BooleanField(blank=True)
    commentstep = models.TextField(max_length=1000,help_text="Enter a comment",blank=True)

    plasma = models.BooleanField(blank=True)
    plasmanumber = models.IntegerField(blank=True, default=0)
    seroes = models.BooleanField(blank=True)
    seroesnumber = models.IntegerField(blank=True, default=0)
    commentaliquot = models.TextField(max_length=1000,help_text="Enter a comment",blank=True)

    # koente man in der view mit überschrift freeze einruecken
    aliquot = models.BooleanField(blank=True)
    tubes = models.BooleanField(blank=True)

    transfer = models.TextField(max_length=1000,help_text="which samples when and where",blank=True)


    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        # Returns the URL to access a particular biosample
        return reverse('biosample-detail',args=[str(self.id)])

    def __str__(self):
        return self.name

"""
Modal for the type
"""
class Type(models.Model):

    def euColor(self):
        eu_color = {
            'serum':'rgba(255, 255, 255, 0.4)',          #white
            'serum-gel':'rgba(139, 69, 19, 0.4)',        #brown
            'lithium-heparin':'rgba(255, 128, 0, 0.4)',  #orange
            'flouride':'rgba(255, 255, 0, 0.4)',         #yellow
            'edta ke':'rgba(223, 1, 1, 0.4)',            #red
            'citrat bsg':'rgba(204, 46, 250, 0.4)',      #violet
            'citrat coagulation':'rgba(4, 180, 4, 0.4)', #green
        }
        return(eu_color[self.color])

    def usColor(self):
        us_color = {
            'serum':'rgba(223, 1, 1, 0.4)',                #red
            'serum-gel':'rgba(139, 69, 19, 0.4)',          #brown
            'lithium-heparin':'rgba(4, 180, 4, 0.4)',      #green
            'flouride':'rgba(132, 132, 132, 0.4)',         #gray
            'edta ke':'rgba(204, 46, 250, 0.4)',           #violet
            'citrat bsg':'rgba(0, 0, 0, 0.4)',             #black
            'citrat coagulation':'rgba(0, 191, 255, 0.4)', #blue
        }
        return(us_color[self.color])

    name = models.CharField(max_length=50, help_text="Enter the type of the biosample (e.g. Blood)")
    comment = models.TextField(blank=True,help_text="Enter a comment if you want")

    COLORCODE_CHOICES = (
        ('eu','EU'),
        ('us','US'),
    )
    code = models.CharField(max_length=50,choices=COLORCODE_CHOICES,blank=True)

    COLOR_CHOICES = (
        ('serum','Serum'),
        ('serum-gel','Serum-Gel'),
        ('lithium-heparin','Lithium-Heparin'),
        ('flouride','flouride'),
        ('edta ke','EDTA KA'),
        ('citrat bsg','Citrat BSG'),
        ('citrat coagulation','Citrat coagulation'),
    )

    color = models.CharField(max_length=50, choices=COLOR_CHOICES,blank=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        # Returns the URL to access a particular type
        return reverse('type-detail',args=[str(self.id)])

    def __str__(self):
        return self.name
