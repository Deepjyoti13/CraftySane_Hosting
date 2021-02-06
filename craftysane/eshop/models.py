from django import forms
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, TextInput, Textarea

# Create your models here.
class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    office_address = models.CharField(blank=True,max_length=100)
    mail_address = models.CharField(blank=True,max_length=100)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=50)
    smtpserver = models.CharField(blank=True,max_length=50)
    smtpemail = models.CharField(blank=True,max_length=50)
    smtppassword = models.CharField(blank=True,max_length=10)
    smtpport = models.CharField(blank=True,max_length=5)
    icon = models.ImageField(blank=True,upload_to='images/')
    assured_logo = models.ImageField(blank=True,upload_to='images/')
    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    
    name= models.CharField(blank=True,max_length=20)
    email= models.CharField(blank=True,max_length=50)
    phone= models.CharField(blank=True,max_length=50)
    subject= models.CharField(blank=True,max_length=50)
    message= models.TextField(blank=True,max_length=255)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name'   : TextInput(attrs={'class': 'w-100 px-2 mx-0 my-1', 'required': 'True', "style": "background-color: rgba(0, 128, 0, 0.13);border: none;height: 40px;border-radius: 10px;", 'placeholder':'Full Name'}),
            'subject' : TextInput(attrs={'class': 'w-100 px-2 mx-0 my-1', 'required': 'True', "style": "background-color: rgba(0, 128, 0, 0.13);border: none;height: 40px;border-radius: 10px;", 'placeholder':'Subject'}),
            'email'   : TextInput(attrs={'class': 'w-100 px-2 mx-0 my-1', 'required': 'True', "style": "background-color: rgba(0, 128, 0, 0.13);border: none;height: 40px;border-radius: 10px;", 'placeholder':'Email Address'}),
            'phone'   : TextInput(attrs={'class': 'w-100 px-2 mx-0 my-1', 'required': 'True', "style": "background-color: rgba(0, 128, 0, 0.13);border: none;height: 40px;border-radius: 10px;", 'placeholder':'Phone Number'}),
            'message' : Textarea(attrs={'class': 'w-100 px-2 mx-0 my-1', 'required': 'True', "style": "background-color: rgba(0, 128, 0, 0.13);border: none;height: 80px;border-radius: 10px;", 'placeholder':'Your Message','rows':'5'}),
        }
