from crispy_forms.layout import Column
from django import forms
from django.forms import widgets
from django.forms.fields import ChoiceField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, ButtonHolder



class FoldingCalculator (forms.Form):
    width = forms.FloatField(
        label='ความกว้าง',
        required=True,
        widget=forms.NumberInput(attrs={'placeholder':'ความกว้าง เมตร', 'style': 'border-color: lightgray; font-size:18px; width:auto;padding: 12px 20px; ',})

    )
    lenght = forms.FloatField(
        label='ความสูง',
        required=True,
        widget=forms.NumberInput(attrs={'placeholder':'ความสูง เมตร','style': 'border-color: lightgray; font-size:18px; width:auto;padding: 12px 20px; '})

    )
    door = forms.IntegerField(
        
        label = 'จำนวนบานประตู',
        required=True,
        widget=forms.NumberInput(attrs={'placeholder':'จำนวนบานประตู ' ,'style': 'border-color: lightgray; font-size:16px; width:auto ;padding: 12px 20px;',}),
    )


    ch = [('สีดำ','สีดำ'),('สีขาว','สีขาว'), ('สีเทา','สีเทา'), ('สีลายไม้อ่อน','สีลายไม้อ่อน'), ('สีลายไม้เข้ม','สีลายไม้เข้ม')]
    color = ChoiceField(
        label='สีอลูมิเนียม',
        choices=ch,
        widget=forms.Select(attrs={'style': 'border-color: lightgray; font-size:18px; height:100%; width:auto; padding: 12px 20px;'}),
        required=True

    )
    ch = [('1.2 mm','1.2 mm'), ('1.6 mm', '1.6 mm'), ('2.0 mm','2.0 mm')]
    aluThickness = ChoiceField(
        label='ความหนาอลูมิเนียม',
        choices=ch,
        widget=forms.Select(attrs={'style': 'border-color: lightgray; font-size:18px; height:100%; width:100%; padding: 12px 20px;'}),
        required=True,
        
    )

    ch = [('กระจกเขียวตัดแสง','กระจกเขียวตัดแสง'),('กระจกใส','กระจกใส'), ('กระจกสีชา','กระจกสีชา'), ('กระจกเทมเปอร์','กระจกเทมเปอร์'), ('กระจกลามิเนท','กระจกลามิเนท')]
    glass = ChoiceField(
        label='ประเภทกระจก',
        choices=ch,
        widget=forms.Select(attrs={'style': 'border-color: lightgray; font-size:18px; height:100%; width:auto; padding: 12px 20px;'}),
        required=True
    )

    ch = [('6','6 mm'),('7','7 mm'),('8','8 mm'),('9','9 mm'),('10','10 mm')]
    glassThickness = ChoiceField(
        label='ความหนากระจก',
        choices=ch,
        widget=forms.Select(attrs={'style': 'border-color: lightgray; font-size:18px; height:100%; width:auto; padding: 12px 20px;'}),
        required=True
        
    )
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             'first arg is the legend of the fieldset',
    #             'like_website',
    #             'favorite_number',
    #             'favorite_color',
    #             'favorite_food',
    #             'notes'
    #         ),
    #         ButtonHolder(
    #             Submit('submit', 'Submit', css_class='button white'),
    #         ))