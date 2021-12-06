from os import name, popen
from sys import implementation
from django import forms
from django import template
from django.http import request, response
from django.http import FileResponse
from django.shortcuts import redirect, render
from .calculator import FoldingCalculator
from django.db.models import QuerySet
from django.db.models import Q
from database.models import *
from database.form import *
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages



def select(request):
    return render(request,'selectproject.html')

@login_required(login_url='login')
def folding_formular(request):
    return render(request,'foldingDoor/folding-formular.html')

# def fol_input_page(request):
#     return render(request, 'foldingDoor/fol_input_page.html')


User = get_user_model()

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_detail.html'

# ฟังก์ชั่นรับค่า Homepage คำนวณพื้นที่ ตรม. และ ความกว้าง ต่อ บานโดยประมาณ
def folding_input(requese):
    glassType2 = requese.POST.get('glass', None)
    glassThick = requese.POST.get('glassThickness', None)
    form = FoldingCalculator(requese.POST)        

    if form.is_valid():
        # รับข้อมูลจากฟอร์ม
        area_width = requese.POST.get('width', None)
        area_height = requese.POST.get('lenght', None)
        aluThick = requese.POST.get('aluThickness', None)
        aluColor = requese.POST.get('color', None)
        brandName = requese.POST.get('brand', None)
        youChoose_door = "คุณเลือกตามประตู"


        # คำนวณพื้นที่
        area_sqaure = float(area_width)*float(area_height)

        # คำนวณประตู
        door = requese.POST.get('door', None)
        door_single_width = float(area_width) / int(door)  # ความกว้างแต่ละบานพับ
        door_single_cbm = float(door_single_width) * float(area_height) # CBMของบานเดี่ยว

        #คำนวณค่าขนส่งCBM
        cbm_frame = float(area_width)*0.12*0.11
        h_package = 0.0675*float(door)
        l_package = area_height
        w_package = door_single_width
        all_cbm = float(h_package)*float(l_package)*float(w_package)
        all_cbm_cost = (float(all_cbm)*7300)+(float(cbm_frame)*7300)


        # คำนวณราคาตามขนาด
        alu_price_cbm12 = float(area_width)*float(area_height)*4500
        alu_price_door12 = float(door)*1.6*4500  # คำนวณราคาDOOR ขนาด 1.2mm
        alu_price_cbm16 = float(area_width)*float(area_height)*5300  # คำนวณราคาCBMขนาด 1.6mm
        alu_price_door16 = float(door)*1.6*5000  # คำนวณราคาDOOR ขนาด 1.6mm
        # คำนวณราคาCBMขนาด 2.0mm
        alu_price_cbm20 = float(area_width)*float(area_height)*5900
        alu_price_door20 = float(door)*1.6*5900  # คำนวณราคาDOOR ขนาด 2.0mm


        #ดึงข้อมูลกระจก
        all_glass = Glasscost.objects.all()
        glassSelect = Glasscost.objects.filter(glassType = glassType2) ##จับคู่ประเภทกระจกที่เลือกกับฟิลด์ในตาราง
        glassSelect_price = glassSelect[0].price #จับคู่ต้นทุนราคากระจก (ค่ากระจก/ตรฟ)
        sqf = float(area_sqaure)*10.76391 #แปลงเป็นตารางฟุต
        glass_cost_select = (sqf*float(glassSelect_price))+((sqf*float(glassSelect_price))*0.07) #ต้นทุนกระจกทั้งหมด

        #ดึงข้อมูลต้นทุนอลูมิเนียม
        cost_alu = DoorFoldingCost.objects.all()
        cost_alu_select = DoorFoldingCost.objects.filter(thick = aluThick) & \
                        DoorFoldingCost.objects.filter(color = aluColor)
        cost_alu_select_price = cost_alu_select[0].price

        #ต้นทุนอลูมิเนียมตามพื้นที่ CBM
        aluCost = float(cost_alu_select_price) * area_sqaure

        #ต้นทุนอลูมิเนียมตามจำนวนบาน
        aluCost_door = float(cost_alu_select_price) * float(door) * float(1.6)

        #ต้นทุนค่าใช้จ่ายอื่นๆ
        otherCost = OtherCost.objects.all()
        laborCost = otherCost[0].labor_cost
        all_labor_cost = int(laborCost) * int(door)  #รวมค่าแรง
        transport_cost = otherCost[0].transport_cost #ค่าขนส่ง
        tools_cost = otherCost[0].tools_cost #ค่าอุปกรณ์
        other_cost = otherCost[0].other_cost #ค่าใช้จ่ายอื่นๆ

        all_other_cost = all_labor_cost + int(transport_cost) + int(tools_cost) + int(other_cost) #รวมทุนค่าแรง + ค่าขนส่งและอื่นๆ



        #รวมทุนทั้งหมด
        allCost = float(all_other_cost) + glass_cost_select + float(aluCost) + all_cbm_cost
        allCost_door = float(all_other_cost) + glass_cost_select + float(aluCost_door) + all_cbm_cost

        #margin
        margin_CBM12 = alu_price_cbm12 - allCost 
        margin_CBM16 = alu_price_cbm16 - allCost
        margin_CBM20 = alu_price_cbm20 - allCost

        margin_door12 = alu_price_door12 -allCost
        margin_door16 = alu_price_door16-allCost
        margin_door20 = alu_price_door20 - allCost

        m_percent_12 = ((margin_CBM12 * 100)/alu_price_cbm12)
        m_percent_16 = ((margin_CBM16 * 100)/alu_price_cbm16)




        #ฟังก์ชั่นเลือกสูตรคำนวณจากบานประตู
        if door_single_cbm > 1.4:
            youChoose = "คำนวณตามพื้นที่ CBM"
            if aluThick == '1.2 mm':
                data = {
                    'width': area_width,
                    'lenght': area_height,
                    'sqaure': area_sqaure,
                    'aluThick': aluThick,
                    'glassType': glassType2,
                    'glassThick': glassThick,
                    'aluColor': aluColor,
                    'brand': brandName,
                    'door': door,
                    'alu_price_cbm12': alu_price_cbm12,
                    'all_cbm_cost':all_cbm_cost,
                    'all_glass': all_glass,
                    'glassSelect': glassSelect,
                    'glassSelect_price':glassSelect_price,
                    'glass_cost_select' : glass_cost_select,
                    'cost_alu_select_price':cost_alu_select_price,
                    'all_labor_cost': all_labor_cost,
                    'all_other_cost': all_other_cost,
                    'allCost': allCost,
                    'youChoose':youChoose,
                    'door_single_width':door_single_width,
                    'door_single_cbm':door_single_cbm,
                    'area_sqaure':area_sqaure,
                    'aluCost':aluCost,
                    'margin_CBM12':margin_CBM12,
                    'm_percent_12':m_percent_12,
                }
                print(glassThick)
                return render(requese, 'foldingDoor/result.html', data)

            elif aluThick == '1.6 mm':
                data = {
                    'width': area_width,
                    'lenght': area_height,
                    'sqaure': area_sqaure,
                    'aluThick': aluThick,
                    'glassType': glassType2,
                    'aluColor': aluColor,
                    'brand': brandName,
                    'door': door,
                    'alu_price_cbm16': alu_price_cbm16,
                    'all_glass': all_glass,
                    'glassSelect': glassSelect,
                    'glassSelect_price':glassSelect_price,
                    'glass_cost_select' : glass_cost_select,
                    'cost_alu_select_price':cost_alu_select_price,
                    'all_labor_cost': all_labor_cost,
                    'all_other_cost': all_other_cost,
                    'allCost': allCost,
                    'youChoose':youChoose,
                    'door_single_width':door_single_width,
                    'door_single_cbm':door_single_cbm,
                    'area_sqaure':area_sqaure,
                    'all_cbm_cost':all_cbm_cost,
                    'aluCost':aluCost,
                    'margin_CBM16':margin_CBM16,
                    'm_percent_16':m_percent_16,
                }

                return render(requese, 'foldingDoor/result.html', data)

            elif aluThick == '2.0 mm':
                data = {
                    'width': area_width,
                    'lenght': area_height,
                    'sqaure': area_sqaure,
                    'aluThick': aluThick,
                    'glassType': glassType2,
                    'glassThick': glassThick,
                    'aluColor': aluColor,
                    'brand': brandName,
                    'door': door,
                    'alu_price_cbm20': alu_price_cbm20,
                    'all_glass': all_glass,
                    'glassSelect': glassSelect,
                    'glassSelect_price':glassSelect_price,
                    'glass_cost_select' : glass_cost_select,
                    'cost_alu_select_price':cost_alu_select_price,
                    'all_labor_cost': all_labor_cost,
                    'all_other_cost': all_other_cost,
                    'allCost': allCost,
                    'youChoose':youChoose,
                    'door_single_width':door_single_width,
                    'door_single_cbm':door_single_cbm,
                    'area_sqaure':area_sqaure,
                    'all_cbm_cost':all_cbm_cost,
                    'aluCost':aluCost,
                    'margin_CBM20':margin_CBM20,
                }

                return render(requese, 'foldingDoor/result.html', data)

        elif door_single_cbm < 1.4:
        
            aluThick == '1.2 mm'
            data = {
                    'width': area_width,
                    'lenght': area_height,
                    'sqaure': area_sqaure,
                    'aluThick': aluThick,
                    'glassType': glassType2,
                    'glassThick': glassThick,
                    'aluColor': aluColor,
                    'brand': brandName,
                    'door': door,
                    'alu_price_door12': alu_price_door12,
                    'all_glass': all_glass,
                    'glassSelect': glassSelect,
                    'glassSelect_price':glassSelect_price,
                    'glass_cost_select' : glass_cost_select,
                    'cost_alu_select_price':cost_alu_select_price,
                    'all_labor_cost': all_labor_cost,
                    'all_other_cost': all_other_cost,
                    'allCost_door':  allCost_door,
                    'youChoose_door':youChoose_door,
                    'door_single_width':door_single_width,
                    'door_single_cbm':door_single_cbm,
                    'area_sqaure':area_sqaure,
                    'all_cbm_cost':all_cbm_cost,
                    'aluCost_door':aluCost_door,
                    'margin_door12':margin_door12,
                    
                }

            return render(requese, 'foldingDoor/result.html', data)
        elif aluThick == '1.6 mm':
            data = {
                    'width': area_width,
                    'lenght': area_height,
                    'sqaure': area_sqaure,
                    'aluThick': aluThick,
                    'glassType': glassType2,
                    'glassThick': glassThick,
                    'aluColor': aluColor,
                    'brand': brandName,
                    'door': door,
                    'alu_price_door16': alu_price_door16,
                    'all_glass': all_glass,
                    'glassSelect': glassSelect,
                    'glassSelect_price':glassSelect_price,
                    'glass_cost_select' : glass_cost_select,
                    'cost_alu_select_price':cost_alu_select_price,
                    'all_labor_cost': all_labor_cost,
                    'all_other_cost': all_other_cost,
                    'allCost_door':  allCost_door,
                    'youChoose_door':youChoose_door,
                    'door_single_width':door_single_width,
                    'door_single_cbm':door_single_cbm,
                    'area_sqaure':area_sqaure,
                    'all_cbm_cost':all_cbm_cost,
                    'aluCost_door':aluCost_door,
                    'margin_door16':margin_door16,
                    
                }

            return render(requese, 'foldingDoor/result.html', data)
        elif aluThick == '2.0':
            data = {
                    'width': area_width,
                    'lenght': area_height,
                    'sqaure': area_sqaure,
                    'aluThick': aluThick,
                    'glassType': glassType2,
                    'glassThick': glassThick,
                    'aluColor': aluColor,
                    'brand': brandName,
                    'door': door,
                    'alu_price_door20': alu_price_door20,
                    'all_glass': all_glass,
                    'glassSelect': glassSelect,
                    'glassSelect_price':glassSelect_price,
                    'glass_cost_select' : glass_cost_select,
                    'cost_alu_select_price':cost_alu_select_price,
                    'all_labor_cost': all_labor_cost,
                    'all_other_cost': all_other_cost,
                    ' allCost_door':  allCost_door,
                    'youChoose_door':youChoose_door,
                    'door_single_width':door_single_width,
                    'door_single_cbm':door_single_cbm,
                    'area_sqaure':area_sqaure,
                    'all_cbm_cost':all_cbm_cost,
                    'aluCost_door':aluCost_door,
                    'margin_door20':margin_door20,
                }
            return render(requese, 'foldingDoor/result.html', data)

    else:
        form = FoldingCalculator(requese.POST)
        w = requese.POST.get('width', 0)
        l = requese.POST.get('lenght', 0)
        x = {
            'form': form,
            'width': w,
            'lenght': l
        }
        
        return render(requese, 'foldingDoor/fol_input_page.html', x)

# โชว์ต้นทุนที่บันทึกทั้งหมด
@login_required(login_url='login')
def folding_allcost(request):
    return render(request, 'foldingDoor/folding-cost-allshow.html')

  # ระบบต้นทุนหลังบ้าน MODELS

# คำสั่งบันทึกต้นทุนอลูมิเนียม
@login_required(login_url='login')
def folding_cost(request):
    if request.method == 'POST':
        form = DoorFoldingCost_form(request.POST)
        if form.is_valid():
            brand = form.cleaned_data['brand']
            color = form.cleaned_data['color']
            thick = form.cleaned_data['thick']
            price = form.cleaned_data['price']
            ins = DoorFoldingCost.objects.create(user=request.user, brand=brand, color=color, thick=thick, price=price)
            ins.save()
            messages.success(request, 'Successfully created!')
            return redirect('fol_all_cost')
            # user = User.objects.create(id=)
        else:
            form = DoorFoldingCost_form()
    else:
        form = DoorFoldingCost_form()
    return render(request, 'foldingDoor/folding-cost-create.html', {'form': form})

# คำสั่งบันทึกต้นทุนกระจก
@login_required(login_url='login')
def glass_cost(request):
    form = Glasscost_form(request.POST)
    if form.is_valid():
        form.save()
    else:
        form = Glasscost_form()
    return render(request, 'glass-cost-create.html', {'form': form})

# คำสั่งบันทึกต้นทุนค่าใช้จ่ายอื่นๆ
@login_required(login_url='login')
def other_cost(request):
    form = OtherCost_form(request.POST)
    if form.is_valid():
        form.save()
    else:
        form = OtherCost_form()
    return render(request, 'other-cost-create.html', {'form': form})

# ฟังก์ชั่นส่งข้อมูลต้นทุน อลูมิเนียม กระจก และ ค่าใช้จ่ายอื่นๆ
@login_required(login_url='login')
def folding_cost_show(request):
    alu_cost_show = DoorFoldingCost.objects.filter(user=request.user)
    glass_cost_show = Glasscost.objects.filter(user=request.user)
    other_cost_show = OtherCost.objects.filter(user=request.user)
    data = {
        'alu': alu_cost_show,
        'glass': glass_cost_show,
        'other': other_cost_show
    }


    return render(request, 'foldingDoor/folding-cost-show.html', data)

# หน้าแก้ไขต้นทุนที่บันทึกไว้

@login_required(login_url='login')
def folding_cost_edit(request):
    data = DoorFoldingCost.objects.all()
    return render(request, 'folding-cost-edit.html', {'data': data})

@login_required(login_url='login')
def glass_cost_edit(request):
    data = Glasscost.objects.all()
    return render(request, 'glass-cost-edit.html', {'data': data})

@login_required(login_url='login')
def other_cost_edit(request):
    data = OtherCost.objects.all()
    return render(request, 'other_cost_edit.html', {'data': data})

# คำสั่งอัพเดทข้อมูลต้นทุน
@login_required(login_url='login')
def folding_cost_update(request, id):
    row = DoorFoldingCost.objects.get(id=id)

    form = DoorFoldingCost_form(instance=row, data=request.POST)
    if form.is_valid():
        form.save()
    else:
        row = DoorFoldingCost_form.objects.get(id=id)
        form = DoorFoldingCost_form(initial=row.__dict__)
    return render(request, 'foldingDoor/folding-cost-update.html', {'form': form})

@login_required(login_url='login')
def glass_cost_update(request, id):
    row = Glasscost.objects.get(id=id)

    form = Glasscost_form(instance=row, data=request.POST)
    if form.is_valid():
        form.save()
    else:
        row = Glasscost.objects.get(id=id)
        form = Glasscost_form(initial=row.__dict__)
    return render(request, 'glass-cost-update.html', {'form': form})

@login_required(login_url='login')
def other_cost_update(request, id):
    row = OtherCost.objects.get(id=id)

    form = OtherCost_form(instance=row, data=request.POST)
    if form.is_valid():
        form.save()
    else:
        row = OtherCost.objects.get(id=id)
        form = OtherCost_form(initial=row.__dict__)
    return render(request, 'other-cost-update.html', {'form': form})



def form_input(request):
    return render(request,'form_input.html')

def log_out(request):
    logout(request)
    return redirect ('select')


User = get_user_model()
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_detail.html'

def loginPage(request):

    
    
    return render(request, 'login_page/login.html')