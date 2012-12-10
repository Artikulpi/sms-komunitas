from django import forms
from member.models import (TemaInformasi, HubunganKeluarga, Agama, Organisasi,
                           JenisUsaha, Keahlian, PendidikanTerakhir, Jurusan,
                           Pekerjaan, GolonganDarah, JadwalRonda, Usia,
                           StatusSosial, Person)
from message.models import Broadcast
from wilayah.models import (Desa, Dusun, Kampung, RT)

class DeleteMessagesForm(forms.Form):
    queue = forms.CharField(
        widget = forms.HiddenInput,
        required = False,
    )
    
    error_css_class = "alert alert-error"

class BroadcastForm(forms.Form):
    
    def _get_unique_domisili(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if x not in seen and not seen_add(x)]
    
    REL_CHOICES = (
        (0, "Dan"),
        (1, "Atau"),
    )
    
    persons = Person.objects.all()
    bulk_domisili = [x.domisili for x in persons]
    unique_domisili = _get_unique_domisili(bulk_domisili)
    
    DOMISILI_CHOICES = []
    for domisili in unique_domisili:
        DOMISILI_CHOICES.append(
            (domisili, domisili)
        )
    
    message = forms.CharField(
        max_length=160,
        widget=forms.widgets.Textarea(attrs={'cols':100, 'rows':3},),
    )
    
    external = forms.BooleanField(
        required = False,
        label = "Nomor Handphone",
    )
    
    member = forms.BooleanField(
        required = False,
        label = "Member",
    )
    
    extra_phones = forms.CharField(
        required = False,
        widget=forms.TextInput(attrs={'class':'input-xlarge'},),
    )
    
    tema_informasi = forms.ModelMultipleChoiceField(
        queryset = TemaInformasi.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    tema_informasi_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    hubungan_keluarga = forms.ModelMultipleChoiceField(
        queryset = HubunganKeluarga.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    hubungan_keluarga_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    jenis_kelamin = forms.MultipleChoiceField(
        choices = (
            (0, 'Laki-laki'),
            (1, 'Perempuan'),
        ),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    jenis_kelamin_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    domisili = forms.MultipleChoiceField(
        choices = DOMISILI_CHOICES,
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    domisili_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    agama = forms.ModelMultipleChoiceField(
        queryset = Agama.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    agama_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    organisasi = forms.ModelMultipleChoiceField(
        queryset = Organisasi.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    organisasi_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    jenis_usaha = forms.ModelMultipleChoiceField(
        queryset = JenisUsaha.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    jenis_usaha_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    keahlian = forms.ModelMultipleChoiceField(
        queryset = Keahlian.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    keahlian_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    pendidikan_terakhir = forms.ModelMultipleChoiceField(
        queryset = PendidikanTerakhir.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    pendidikan_terakhir_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    jurusan = forms.ModelMultipleChoiceField(
        queryset = Jurusan.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    jurusan_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    pekerjaan = forms.ModelMultipleChoiceField(
        queryset = Pekerjaan.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    pekerjaan_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    penerima_jaminan_sosial = forms.MultipleChoiceField(
        choices = (
            (0, "Tidak"),
            (1, "Ya"),
        ),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    penerima_jaminan_sosial_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    golongan_darah = forms.ModelMultipleChoiceField(
        queryset = GolonganDarah.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    golongan_darah_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    jadwal_ronda = forms.ModelMultipleChoiceField(
        queryset = JadwalRonda.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    jadwal_ronda_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    usia = forms.ModelMultipleChoiceField(
        queryset = Usia.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    usia_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    status_sosial = forms.ModelMultipleChoiceField(
        queryset = StatusSosial.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    status_sosial_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
    desa = forms.ModelMultipleChoiceField(
        queryset = Desa.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
    
    dusun = forms.ModelMultipleChoiceField(
        queryset = Dusun.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )
    
    kampung = forms.ModelMultipleChoiceField(
        queryset = Kampung.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )
    
    rt = forms.ModelMultipleChoiceField(
        queryset = RT.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )
    
    wilayah_rel = forms.ChoiceField(
        choices = REL_CHOICES,
        required = False,
    )
    
class SettingBroadcastForm(forms.ModelForm):
    error_css_class = 'alert alert-error'
    
    class Meta:
        model = Broadcast
        

class ReplyForm(forms.Form):
    message = forms.CharField(
        max_length=160,
        widget=forms.widgets.Textarea(attrs={'cols':100, 'rows':3},),
    )
    
    destination = forms.CharField(
        max_length=20,
        widget=forms.HiddenInput,
    )
    
class SearchForm(forms.Form):
    q = forms.CharField(required=False)
    