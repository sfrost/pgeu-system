from django.contrib import admin

from postgresqleu.util.forms import ConcurrentProtectedModelForm

from postgresqleu.confreg.models import Conference, ConferenceRegistration, RegistrationType
from .models import Wikipage, WikipageHistory, WikipageSubscriber
from .models import AttendeeSignup


class WikipageAdminForm(ConcurrentProtectedModelForm):
    class Meta:
        model = Wikipage
        exclude = []

    def __init__(self, *args, **kwargs):
        super(WikipageAdminForm, self).__init__(*args, **kwargs)
        try:
            self.fields['author'].queryset = ConferenceRegistration.objects.filter(conference=self.instance.conference)
            self.fields['viewer_attendee'].queryset = ConferenceRegistration.objects.filter(conference=self.instance.conference)
            self.fields['editor_attendee'].queryset = ConferenceRegistration.objects.filter(conference=self.instance.conference)

            self.fields['viewer_regtype'].queryset = RegistrationType.objects.filter(conference=self.instance.conference)
            self.fields['editor_regtype'].queryset = RegistrationType.objects.filter(conference=self.instance.conference)
        except Conference.DoesNotExist:
            pass


class WikipageHistoryInline(admin.TabularInline):
    model = WikipageHistory
    readonly_fields = ['author', 'publishedat']
    exclude = ['contents', ]
    can_delete = False
    max_num = 0
    extra = 0


class WikipageSubscriberInline(admin.TabularInline):
    model = WikipageSubscriber
    readonly_fields = ['subscriber', ]
    can_delete = True
    max_num = 0
    extra = 0


class WikipageAdmin(admin.ModelAdmin):
    form = WikipageAdminForm
    inlines = [WikipageHistoryInline, WikipageSubscriberInline]
    autocomplete_fields = ('author', 'viewer_attendee', 'editor_attendee')


class AttendeeSignupAdminForm(ConcurrentProtectedModelForm):
    class Meta:
        model = AttendeeSignup
        exclude = []
        readonly_fields = ['signup', ]

    def __init__(self, *args, **kwargs):
        super(AttendeeSignupAdminForm, self).__init__(*args, **kwargs)
        try:
            self.fields['attendee'].queryset = ConferenceRegistration.objects.filter(conference=self.instance.signup.conference)
        except Exception as e:
            pass


class AttendeeSignupAdmin(admin.ModelAdmin):
    form = AttendeeSignupAdminForm
    list_display = ['signup', 'attendee', ]
    list_filter = ['signup__conference', ]


admin.site.register(Wikipage, WikipageAdmin)
admin.site.register(AttendeeSignup, AttendeeSignupAdmin)
