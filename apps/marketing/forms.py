from django.contrib.auth.models import Group
from django import forms
from .models import MarketingCode
# Register your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

class MarketingCodeForm(forms.ModelForm):
    code = forms.CharField(disabled=True,label="推广码",required=False)

    def __init__(self, *args, **kwargs):
        super(MarketingCodeForm, self).__init__(*args, **kwargs)
        g = Group.objects.get(name="marketer")
        users = g.user_set.all()
        self.fields['user'].queryset = users
    def generate_code(self):
        # 当前时间+userid+随机数
        from random import Random
        import time
        random_ins = Random()
        code = "{time_str}{ranstr}{userid}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.cleaned_data['user'].id,
                                                       ranstr=random_ins.randint(10, 99))

        return code

    def clean_code(self):
        code = self.generate_code()
        return code
    class Meta:
        model = MarketingCode
        fields = "__all__"
