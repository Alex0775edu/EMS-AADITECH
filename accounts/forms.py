from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'institute_id',
            'date_of_birth',
            'role',
            'institution',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user
        self.fields['role'].choices = self._allowed_role_choices(current_user)
        self.fields['institution'].required = False

    def _allowed_role_choices(self, user):
        if user and user.is_superuser:
            return [('ADMIN', 'Admin'), ('INSTITUTE', 'Institute')]
        if user and user.role == 'ADMIN':
            return [('TEACHER', 'Teacher'), ('STUDENT', 'Student')]
        return []

    def clean_role(self):
        role = self.cleaned_data['role']
        allowed = {choice[0] for choice in self._allowed_role_choices(self.current_user)}
        if role not in allowed:
            raise forms.ValidationError('You are not allowed to create this role.')
        return role

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = User.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def clean_institute_id(self):
        institute_id = (self.cleaned_data.get('institute_id') or '').strip()
        if not institute_id:
            raise forms.ValidationError('Institute ID is required.')
        qs = User.objects.filter(institute_id__iexact=institute_id)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('This institute ID is already in use.')
        return institute_id

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        institution = cleaned_data.get('institution')

        if self.current_user and self.current_user.is_superuser and role == 'ADMIN' and not institution:
            self.add_error('institution', 'Institution is required when creating an Admin user.')

        if self.current_user and not self.current_user.is_superuser and self.current_user.role == 'ADMIN':
            if not self.current_user.institution:
                raise forms.ValidationError('Your admin account has no institution mapped. Contact superuser.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.email.lower()
        user.institute_id = (user.institute_id or '').strip()
        user.username = self._build_unique_username(user)

        if self.current_user and not self.current_user.is_superuser and self.current_user.role == 'ADMIN':
            user.institution = self.current_user.institution

        if user.role in {'ADMIN', 'INSTITUTE'}:
            user.is_staff = True

        default_password = user.default_password_from_dob()
        if default_password:
            user.set_password(default_password)

        if commit:
            user.save()
        return user

    def _build_unique_username(self, user):
        base = (user.institute_id or user.email.split('@')[0] or 'user').lower().replace(' ', '')
        candidate = base
        i = 1
        while User.objects.filter(username=candidate).exists():
            i += 1
            candidate = f'{base}{i}'
        return candidate
