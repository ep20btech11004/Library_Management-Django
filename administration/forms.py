from django import forms
from administration.models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput
from django.core.validators import RegexValidator

gender_choices = [("Male", "Male"), ("Female", "Female"), ("Others", "Others")]

class DateInput(DateInput):
    input_type = 'date'

class LoginRegister(UserCreationForm):

    class Meta:
        model = Login
        fields = ('username', 'password1', 'password2')

class BookForm(forms.ModelForm):

    genre = forms.ModelChoiceField(queryset = Genre.objects.all())
    lang = forms.ModelChoiceField(queryset = Language.objects.all())
    rel_date = forms.DateField(widget = DateInput)

    class Meta:
        model = Book
        fields = ('name', 'author', 'isbn', 'copies', 'rel_date', 'genre', 'lang','description', 'image')

class CustomerForm(forms.ModelForm):

    occupation = forms.ModelChoiceField(queryset = Occupation.objects.all())
    gender = forms.ChoiceField(choices = gender_choices, widget = forms.RadioSelect)
    contact = forms.IntegerField(validators = [RegexValidator(regex = "^\\+?[1-9][0-9]{7,14}$", message = "Please Enter Valid Phone Number")])

    class Meta:
        model = Customer
        fields = ('name', 'occupation', 'age', 'roll_no', 'contact', 'email', 'gender', 'image')

class SubAdminForm(forms.ModelForm):
    gender = forms.ChoiceField(choices = gender_choices, widget = forms.RadioSelect)
    contact = forms.IntegerField(validators = [RegexValidator(regex = "^\\+?[1-9][0-9]{7,14}$", message = "Please Enter Valid Phone Number")])

    class Meta:
        model = SubAdmin
        fields = ('name', 'contact', 'age', 'gender', 'email', 'image') 

class LibrarianForm(forms.ModelForm):
    gender = forms.ChoiceField(choices = gender_choices, widget = forms.RadioSelect)
    designation = forms.ModelChoiceField(queryset = Occupation.objects.all())
    contact = forms.IntegerField(validators = [RegexValidator(regex = "^\\+?[1-9][0-9]{7,14}$", message = "Please Enter Valid Phone Number")])

    class Meta:
        model = Librarian
        fields = ('name', 'contact', 'age', 'gender', 'designation', 'email', 'image')

class ReserveForm(forms.ModelForm):

    class Meta:
        model = Reserve
        fields = ('user', 'book', 'valid_till')

class ConfigureForm(forms.ModelForm):
    fine = forms.IntegerField(initial = 0)
    hike = forms.IntegerField(initial = 0)
    interval = forms.IntegerField(initial = 0)
    issue_till = forms.IntegerField(initial = 10)
    reserve_till = forms.IntegerField(initial = 1)

    class Meta:
        model = Configure
        fields = ('fine', 'hike', 'interval', 'issue_till', 'reserve_till')

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset = Login.objects.all())
    
    class Meta:
        model = Message
        fields = ('receiver', 'contact', 'message')

class OrganizationForm(forms.ModelForm):
    contact = forms.IntegerField(validators = [RegexValidator(regex = "^\\+?[1-9][0-9]{7,14}$", message = "Please Enter Valid Phone Number")])
    estd = forms.DateField(widget = DateInput)

    class Meta:
        model = Organization
        fields = ('name', 'building', 'estd', 'contact', 'city', 'state', 'country')

class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = ('genre',)

class LanguageForm(forms.ModelForm):

    class Meta:
        model = Language
        fields = ('lang',)
    
class OccupationForm(forms.ModelForm):

    class Meta:
        model = Occupation
        fields = ('occupation',)

class IntForm(forms.ModelForm):

    class Meta:
        model = Int
        fields = ('num',)

