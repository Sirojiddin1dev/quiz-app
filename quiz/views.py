from django.shortcuts import render,redirect
from .models import Task , Category ,Taskusers
from customusers.models import CustomUser
from django.contrib.auth import authenticate, login, logout 
import datetime
from django.views.generic.edit import UpdateView
from .forms import CustomUserCreationForm,CustomAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from datetime import date
from transliterate import translit

now = datetime.datetime.now()
import os
from django.shortcuts import redirect, render
from .models import Taskusers, CustomUser, Task, Category
import datetime
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

font_path = "static/fonts/DejaVuSans.ttf"
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Shrift fayli topilmadi: {font_path}")

pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

def homepage(request, id):
    now = datetime.datetime.now()
    print(now, "++++++++++++++++++++++++")

    if request.user.test_access == 1:
        alc = '1-2-Modul'
        tasks = Task.objects.filter(category=id)
    elif request.user.test_access == 4:
        tasks = Task.objects.all()
        alc = 'ALL'
    elif request.user.test_access == 2:
        tasks = Task.objects.filter(category=id)
        alc = '3-Modul'
    else:
        alc = 0

    category = Category.objects.get(id=id, is_active=True)
    tasks_count = tasks.count()

    if request.user.is_active:
        if request.method == 'POST':
            natija1 = request.POST.get('natija1', 0)
            natija2 = request.POST.get('natija2', 0)

            # Always create a new Taskusers instance
            Taskusers.objects.create(
                username=request.user,
                natija1=natija1,
                natija2=natija2,
                checking=request.POST.get('checking1'),
                checking2=request.POST.get('checking2'),
                category=category,
                all=alc,
                attempts=1
            )

            user = CustomUser.objects.get(id=request.user.id)
            user.test_access = 0
            user.save()

            return redirect('/')

        user = request.user
        if user.language == "uzbek":
            if category.title == "1-2-Modul":
                user_timer = 50
            else:
                user_timer = 151
        elif user.language == "russian":
            if category.title == "1-2-Modul":
                user_timer = 35
            else:
                user_timer = 116
        else:
            user_timer = category.timer

        if request.user.test_access == 4:
            user_timer = 201 if user.language == "uzbek" else 151

        context = {
            'task': tasks,
            'task_c': tasks_count,
            'yourtest': request.user.taskusers_set.all(),
            'category': category,
            'user_timer': user_timer,
        }
    else:
        context = {}

    return render(request, 'test.html', context)



def apply(request):
    usertask = Taskusers.objects.all().order_by('-date')
    
    context ={
    'topshirganlar':usertask,
    'true':Taskusers.objects.filter(checking='True').all().count(),
    'false':Taskusers.objects.filter(checking='False').all().count(),
    }
    return render(request,'apply.html',context)


def admindetail(request,id):
    categ = Category.objects.get(id=id)
    if request.method =="POST":
        Task.objects.create(
            category=categ,
            title=request.POST.get('title'),
            a=request.POST.get('a'),
            b=request.POST.get('b'),
            c=request.POST.get('c'),
            d=request.POST.get('d'),
            togri_javob=request.POST.get('togri_javob')
        )
        return redirect('admindetail',categ.id)


    context={
        'categ':categ,
        'tasks':categ.task_set.all().order_by('-id')
    }
    return render(request,'categorydetail.html',context)

def taskdelete(request,id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('admindetail',task.category.id)


class Updatetask(UpdateView):
    model= Task
    template_name='updatetask.html'
    fields='__all__'

def index(request):

    if request.user.is_active == True:
        context={
            'yourtest':request.user.taskusers_set.all(),
        }
    else:
        context={}
    categories = Taskusers.objects.filter(checking=True, username=request.user.id).values_list('category', flat=True)
    
    task_category = Category.objects.exclude(id__in=categories)

    user = request.user
    try: 

        if user.test_access == 4:
            
            user_category = task_category
        
        elif user.test_access == 2:
            
            user_category = Category.objects.exclude(id__in=categories).filter(title="3-Modul")

        elif user.test_access == 1:
            
            user_category = Category.objects.exclude(id__in=categories).filter(title="1-2-Modul")

        else:

            user_category = []
    except:
        user_category = []
    context['categories']= user_category

    # print(context)
    return render(request,'index.html',context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to your home page or any other desired page
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the URL name of your home page
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


def get_certificate(request):
    user = request.user

    if user.certificate and user.passed:
        certificate_template = "certificatefull.pdf"
        position_y = 330
    elif user.certificate:
        certificate_template = "certificatepart.pdf"
        position_y = 330
    else:
        # Sertifikat olish shartlari bajarilmagan holatlar uchun
        return HttpResponse("No certificate available for this user.")

    # FIO ni Cyrillicga o'zgartirish
    full_name = translit(user.get_full_name(), 'ru', reversed=False)
    issued_date = date.today().strftime("%d.%m.%Y")  # Bugungi sanani formatlash

    packet = io.BytesIO()

    # Sertifikatni yaratish
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("DejaVuSans", 35)  # DejaVu Sans shriftini ishlatish

    # Matnning kengligini hisoblash va markazga joylash
    text_width = can.stringWidth(full_name, "DejaVuSans", 35)
    page_width, page_height = letter
    position_x = (page_width - text_width) / 2

    can.drawString(position_x, position_y, full_name)

    # Sana uchun shriftni kichraytirish va joylashuvni sozlash
    can.setFont("DejaVuSans", 20)
    date_position_x = 420  # Sanani o'ngroqqa surish
    date_position_y = 120  # Sanani pastroqqa tushirish
    can.drawString(date_position_x, date_position_y, issued_date)
    can.save()

    # Sertifikat shabloni bilan birlashtirish
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open(certificate_template, "rb"))
    output = PdfFileWriter()
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    # Faylni saqlash
    filename = f"{full_name}_certificate.pdf"
    with open(filename, "wb") as output_stream:
        output.write(output_stream)

    # HTTP javobni tayyorlash
    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response




def start_test(request):
    if request.user.is_active == True:
        context = {
            'yourtest': request.user.taskusers_set.all(),
        }
    else:
        context = {}
    categories = Taskusers.objects.filter(checking=True, username=request.user.id).values_list('category', flat=True)

    task_category = Category.objects.exclude(id__in=categories)

    user = request.user
    try:

        if user.test_access == 4:

            user_category = task_category

        elif user.test_access == 2:

            user_category = Category.objects.exclude(id__in=categories).filter(title="3-Modul")

        elif user.test_access == 1:

            user_category = Category.objects.exclude(id__in=categories).filter(title="1-2-Modul")

        else:

            user_category = []
    except:
        user_category = []
    category_ids = list(user_category.values_list('id', flat=True))
    category = Category.objects.filter(id__in=category_ids)
    tasks = Task.objects.filter(category__in=category).count()
    user = request.user
    if user.language == "uzbek":
        if "1-2-Modul" in user_category.values_list('title', flat=True):
            user_timer = category.filter(title="1-2-Modul").first().timer = 50
        else:
            user_timer = category.first().timer = 151
    elif user.language == "russian":
        if "1-2-Modul" in user_category.values_list('title', flat=True):
            user_timer = category.filter(title="1-2-Modul").first().timer = 35
        else:
            user_timer = category.first().timer = 116
    else:
        user_timer = category.first().timer
    if request.user.test_access == 4:
        category_ids = 1
        if user.language == "uzbek":
            user_timer = 201
        else:
            user_timer = 151
    context['categories'] = category_ids
    context['tasks'] = tasks
    context['task'] = user_timer

    # print(context)
    return render(request, 'start_test.html', context)
