from collections import defaultdict
from database.models import*

class DoorFoldingCost_form(forms.ModelForm):
    class Meta:
        model = DoorFoldingCost
        exclude = ('user',)
        labels ={
            'brand': 'ยี่ห้ออลูมิเนียม',
            'thick': 'ความหนาอลูมิเนียม',
            'color': 'สีอลูมิเนียม',
            'price': 'ราคา',
        }
        widgets = {
            'brand': forms.TextInput(attrs= {'placeholder':'ใส่ชื่อแบรนด์ของคุณ เช่น เมืองทอง'}),
            'thick': forms.Select(),
            'color': forms.Select(),
            'price': forms.NumberInput(attrs={'placeholder':'ราคา/ตรม. '}),

            
        }
        def __str__(self):
       
            return f'{self.brand}|{self.thick}|{self.color}|{self.price}|{self.email}'


class SlindingDoor_form(forms.ModelForm):
    class Meta:
        model = SlidingDoor
        fields = "__all__"
        labels ={
            'brand': 'ยี่ห้ออลูมิเนียม',
            'thick': 'ความหนาอลูมิเนียม',
            'color': 'สีอลูมิเนียม',
            'price': 'ราคา',
        }
        widgets = {
            'brand': forms.TextInput(attrs= {'placeholder':'ใส่ชื่อแบรนด์ของคุณ เช่น เมืองทอง'}),
            'thick': forms.Select(),
            'color': forms.Select(),
            'price': forms.NumberInput(attrs={'placeholder':'ราคา/ตรม. '}),

            
        }
        def __str__(self):
       
            return f'{self.brand}|{self.thick}|{self.color}|{self.price}'

class Glasscost_form(forms.ModelForm):

    class Meta:
        model = Glasscost
        fields = "__all__"
        labels = {
            'glassType': 'ประเภทกระจก',
            'glassThick': 'ความหนากระจก',
            'price' : 'ราคา'
        }
        widgets = {
            'glassType' : forms.Select(),
            'glassThick': forms.Select(),
            'price' : forms.NumberInput(attrs={'placeholder':'ราคา ต่อ ตารางฟุต. '}),
        }

class OtherCost_form(forms.ModelForm):
    class Meta:
        model = OtherCost
        fields = "__all__"
        labels = {
            'cbm_cost' : 'ค่าขนส่ง CBM',
            'kg_cost' : 'ค่าขนส่ง KG',
            'labor_cost' : 'ค่าแรงช่าง',
            'transport_cost' : 'ค่าน้ำมันรับของ-วัดหน้างาน',
            'tools_cost' : 'อุปกรณ์เสริม',
            'other_cost' : 'ค่าใช้จ่ายอื่นๆ'
        }
        widgets = {
            'cbm_cost' : forms.NumberInput(attrs={'placeholder':'ค่าขนส่ง ต่อ CBM '}),
            'kg_cost' : forms.NumberInput(attrs={'placeholder':'ค่าขนส่ง ต่อ กิโลกรัม '}),
            'labor_cost' : forms.NumberInput(attrs={'placeholder':'ค่าแรงติดตั้ง ต่อหน่วย'}),
            'tools_cost' : forms.NumberInput(attrs={'placeholder':'อุปกรณ์เสริม เช่น ซิลิโคน กาว '}),
            'other_cost' : forms.NumberInput(attrs={'placeholder':'ค่าใช้จ่ายอื่นๆ '}),
        }
    