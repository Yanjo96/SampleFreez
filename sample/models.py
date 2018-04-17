from django.db import models
from django.urls import reverse # Used to generate urls by reversing the URL pattern
from multiselectfield import MultiSelectField

import uuid
from datetime import date

class Document(models.Model):
    box = models.CharField(max_length=50)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

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

class Compartment(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the copartment (e.g. Compartment 1)")
    space = models.IntegerField(help_text="Enter how many racks can store in the compartment")
    freezer = models.ForeignKey('Freezer',on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        # Returns the URL to access a particular compartment
        return reverse('compartment-detail',args=[str(self.freezer.id),str(self.id)])

    def get_number_of_space(self):
        return int(Rack.objects.filter(compartment_id=self.id).count()) + int(Box.objects.filter(compartment_id=self.id).filter(rack_id__isnull='True').count())

    def __str__(self):
        return self.name

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

class Box(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the Box (e.g. Box 1)")
    space = models.IntegerField(help_text="Enter how many tubes can store in the box")
    freezer = models.ForeignKey('Freezer',on_delete=models.CASCADE)
    compartment = models.ForeignKey('Compartment',on_delete=models.CASCADE)
    #when the box is in the compartment you dont need a rack and a rackmodule
    rack = models.ForeignKey('Rack',on_delete=models.CASCADE, blank=True,null=True)
    rackmodule = models.ForeignKey('Rackmodule', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(max_length=1000,help_text="Enter a comment if you want",blank=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_rack_url(self):
        return reverse('box-r-detail',args=[str(self.freezer.id),str(self.compartment.id),str(self.rack.id),str(self.rackmodule.id),str(self.id)])

    #when the box is in the compartment you dont need a rack and a rackmodule
    def get_absolute_url(self):
            return reverse('box-c-detail',args=[str(self.freezer.id),str(self.compartment.id),str(self.id)])

    def __str__(self):
        return self.name

class Tube(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a name for the rack (e.g. Tube 1)")
    box = models.ForeignKey('Box',on_delete=models.CASCADE,blank=True)
    xvalue = models.IntegerField(help_text="Enter the postion of the tube in the x coordinate", blank=True)
    yvalue = models.IntegerField(help_text="Enter the postion of the tube in the y coordinate", blank=True)
    biosample = models.ForeignKey('BioSample',on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(max_length=1000,help_text="Enter a comment if you want",blank=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_rack_url(self):
        # Returns the URL to access a particular tube
        return reverse('tube-r-detail',args=[str(self.box.freezer.id),str(self.box.compartment.id),str(self.box.rack.id),str(self.box.rackmodule.id),str(self.box.id),str(self.id)])

    #when the box is in the compartment you dont need a rack and a rackmodule
    def get_absolute_compartment_url(self):
        # Returns the URL to access a particular tube
        return reverse('tube-c-detail',args=[str(self.box.freezer.id),str(self.box.compartment.id),str(self.box.id),str(self.id)])

    def __str__(self):
        return self.name

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

    # koennte man in der view mit überschrift Verarbeitungschritte einruecken
    centrifugate = models.BooleanField(blank=True)
    pipet = models.BooleanField(blank=True)
    commentstep = models.TextField(max_length=1000,help_text="Enter a comment",blank=True)

    # koennte man in der view mit überschrift aliquotierung einruecken
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

class Type(models.Model):
    name = models.CharField(max_length=50, help_text="Enter the type of the biosample (e.g. Blood)")
    comment = models.TextField(blank=True,help_text="Enter a comment if you want")

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        # Returns the URL to access a particular type
        return reverse('type-detail',args=[str(self.id)])

    def __str__(self):
        return self.name
