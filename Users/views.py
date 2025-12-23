from django.shortcuts import render,redirect
from .forms import RegisterUserForm,TicketForm,ReportForm
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Ticket,Report,CustomUser
from datetime import datetime as dt
import datetime 
import calendar
# Create your views here.
def Hello(request):
    return render(request,"Users/Welcome.html")


# Boss
def is_boss(user):
    return user.is_boss


@login_required
@user_passes_test(is_boss)
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid() == True:
            ticket = form.save(commit= False)
            ticket.boss = request.user
            ticket.save()
            return redirect("dashboard")
    else:
        form = TicketForm()
    
    return render(request,"Users/Create_ticket.html",{"form":form})
            


@login_required
@user_passes_test(is_boss)
def view_reports(request):
    reports = Report.objects.filter(ticket__boss=request.user).order_by("-creation_date")
    return render(request,"Users/View_reports.html",{"reports":reports})


@login_required
@user_passes_test(is_boss)
def register_new_worker(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid() == True:
            form.save()
            return redirect("login")
        else:
            print("It's not valid.")
            print(form.errors)
    else:
        form = RegisterUserForm()
    return render(request,"Users/Register.html",{"form":form})

@login_required
@user_passes_test(is_boss)
def Workers(request):
    workers = CustomUser.objects.filter(is_worker = True)
    return render(request,"Users/Workers.html",{"workers":workers})


# Workers
@login_required
def my_tickets(request):
    tickets = request.user.assigned_tickets.all().order_by('-id')
    
    tickets = Ticket.objects.filter(worker=request.user)
    ticket_reports = {}
    for ticket in tickets:
        ticket_reports[ticket.id] = ticket.reports.filter(worker = request.user).first()
    return render(request,"Users/My_tickets.html",{"tickets":tickets,"ticket_reports":ticket_reports})


@login_required
def send_report(request,ticket_id):
    ticket = Ticket.objects.get(id = ticket_id)
    if request.method == "POST":
        form = ReportForm(request.POST,request.FILES)
        if form.is_valid()== True:
            report = form.save(commit=False)
            report.worker = request.user
            report.ticket = ticket
            ticket.work_completed = True
            report.save()
            ticket.save()
            return redirect("dashboard")
    else:
        form = ReportForm()
    return render(request,"Users/Send_report.html",{"form":form,"ticket":ticket})
    

@login_required
def dashboard(request):
    context = {}
    if request.user.is_worker == True:
        tickets = Ticket.objects.filter(worker=request.user)
        ticket_reports = {}
        for ticket in tickets:
            ticket_reports[ticket.id] = ticket.reports.filter(worker = request.user).first()
        
        context.update({
            "tickets":tickets,
            "ticket_reports": ticket_reports,
            "tickets_review": tickets.filter(status='to_review').count(),
            "tickets_pending": tickets.filter(status='pending').count(),
            "tickets_week": tickets.filter(due_date__week=datetime.date.today().isocalendar()[1]).count(),
            "tickets_month": tickets.filter(due_date__month=datetime.date.today().month).count(),
        })
        
    elif request.user.is_boss == True:
        workers = CustomUser.objects.filter(is_worker = True)
        tickets = Ticket.objects.filter(work_completed = False)
        context.update({
            "total_tickets": Ticket.objects.all().count(),
            "tickets_por_estado": {
                "to_review": Ticket.objects.filter(status='to_review').count(),
                "pending": Ticket.objects.filter(status='pending').count(),
                },
            "workers": workers.count(),
            "tickets": tickets.count(),
        })
    return render(request,"Users/Dashboard.html",context)


# More

@login_required
def calendar_dashboard(request):
    now = dt.now()
    year = now.year
    month = now.month
    
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdatescalendar(year,month)
    
    week = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
    
    context ={
        "year":year,
        "month": month,
        "month_days" : month_days,
        "week": week,
    }
    return render(request,"Users/Calendar.html",context)

