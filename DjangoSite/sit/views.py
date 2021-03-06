from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from .models import Job, Child, Babysitter, Client
import datetime
from .forms import ClientForm, JobForm, ChildForm, GetJob

# Create your views here.

def index(request):
    # return HttpResponse("Hello, world. You're at the sit index.")
    # template = loader.get_template("sit/login.html")
    # return HttpResponse(template.render())
    return render(request, 'sit/login.html')

def addsitters(request):
    return render(request, 'sit/addsitters.html')

# def addjob(request):
#     return render(request, 'sit/addjob.html')

def profiles(request, sitter_id):
    sitter = get_object_or_404(Babysitter, pk=sitter_id)
    jobs = Job.objects.all()
    langs = sitter.babysitter_languages.all()
    now = datetime.datetime.now()
    # jobs = Job.objects.get(sitter=sitter)
    return render(request, 'sit/profiles.html', {'sitter':sitter, 'langs':langs, 'jobs':jobs, 'now':now})


def showJobTest(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    children = job.child.all()
    return render(request, 'sit/oneJobTest.html', {'job':job, 'children':children})

def showJobSitter(request, job_id, sitter_id):
    job = get_object_or_404(Job, pk=job_id)
    sitter = get_object_or_404(Babysitter, pk=sitter_id)
    children = job.child.all()
    return render(request, 'sit/oneJobSitter.html', {'job':job, 'children':children, 'sitter':sitter})

def pickupJob(request, job_id, sitter_id):
        job = get_object_or_404(Job, pk=job_id)
        sitter = get_object_or_404(Babysitter, pk=sitter_id)
        children = job.child.all()

        if request.method == 'POST':
                form = GetJob(request.POST)
                j = get_object_or_404(Job, pk=job_id)
                if not j.sitter:
                        if form.is_valid:
                                
                                j.sitter = sitter
                                j.save()
                                return HttpResponseRedirect('/pcs/sitterHome/' + sitter.id.__str__())

                else:
                        form = GetJob(initial={'job': job, 'sitter': sitter})
                        return render(request, 'sit/pickupJob.html', {'job':job, 'children':children, 'sitter':sitter, 'form':form})
        else:
                form = GetJob(initial={'job': job, 'sitter': sitter})
                return render(request, 'sit/pickupJob.html', {'job':job, 'children':children, 'sitter':sitter, 'form':form})




def availableJobs(request, sitter_id):
    job_list= Job.objects.order_by('id')
    sitter = Babysitter.objects.get(pk=sitter_id)

    eligible_jobs = []
    for job in job_list:
            if not job.is_old_job and not job.sitter:
                    eligible_jobs.append(job)
#     print(eligible_jobs)                

    context= {'job_list':eligible_jobs, 'sitter':sitter}
    return render(request, 'sit/availableJobs.html', context)



def seeJobsTest(request):
    job_list= Job.objects.order_by('id')
    # output = ', '.join([j.location for j in job_list])
    # template = loader.get_template('sit/showJobTest.html')
    context= {'job_list':job_list}
    # return HttpResponse(template.render(context, request))
    return render(request, 'sit/showJobTest.html', context)

def addClient(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['client_name']
            phone = form.cleaned_data['client_phone']
            c = Client(client_name=name, client_phone=phone)
            c.save()
            return HttpResponseRedirect('/pcs/childform')

    else:
        form = ClientForm()
        
        return render(request, 'sit/clientForm.html', {'form':form})

def addChild(request):
        if request.method == 'POST':
                form = ChildForm(request.POST)
                if form.is_valid():
                        name = form.cleaned_data['child_firstname']
                        yrs = form.cleaned_data['child_age_years']
                        mons = form.cleaned_data['child_age_months']
                        allergies = form.cleaned_data['child_allergies']
                        parent = form.cleaned_data['child_parent']

                        child = Child(child_firstname=name, child_age_years=yrs, child_age_months=mons, child_allergies=allergies, child_parent=parent)
                        child.save()
                        return HttpResponseRedirect('/pcs/client/' + parent.id.__str__())
        else:
                form = ChildForm()
                return render(request, 'sit/childForm.html', {'form':form})

def addjob(request):
        children = Child.objects.all()
        child = []
        if request.method == 'POST':
                form = JobForm(request.POST)
                if form.is_valid():
                        client = form.cleaned_data['client']
                        for c in children:
                                if c.child_parent == client:
                                        child.append(c)
                        location = form.cleaned_data['location']
                        num_child = len(child)
                        datetime_start = form.cleaned_data['datetime_start']
                        datetime_end = form.cleaned_data['datetime_end']


                        
                        j = Job(client=client, location=location, num_child=num_child,
                        datetime_start=datetime_start, datetime_end=datetime_end)
                        # j.child.add(child)

                        j.save()
                        j = Job.objects.get(location=location, num_child=num_child, client=client, datetime_start=datetime_start)
                        for ch in child:
                                j.child.add(ch)
                        # j.save()
                        return HttpResponseRedirect('/pcs/adminHome')

        else:
                form = JobForm()
                
                return render(request, 'sit/addjob.html', {'form':form})

def seeSitters(request):
    sit_list= Babysitter.objects.order_by('id')
    context= {'sit_list':sit_list}
    return render(request, 'sit/sitters.html', context)

def sitterLog(request):
        sit_list= Babysitter.objects.order_by('id')
        slist=[]
        for s in sit_list:
                if not s.is_superuser:
                        slist.append(s)
        context= {'sitters':slist}
        return render(request, 'sit/sitter.html', context)

def pastJobs(request):
    job_list= Job.objects.order_by('id')
    context= {'job_list':job_list}
    return render(request, 'sit/pastJobs.html', context)

def acceptedJobs(request):
    job_list= Job.objects.order_by('id')
    context= {'job_list':job_list}
    return render(request, 'sit/acceptedJobs.html', context)

def pendingJobs(request):
    job_list= Job.objects.order_by('id')
    context= {'job_list':job_list}
    return render(request, 'sit/pendingJobs.html', context)


def adminHome(request):
        job_list= Job.objects.order_by('id')
        
        pending = []
        accepted = []
        past = []
        sitters = []
        clients = Client.objects.order_by('id')
        
        for job in job_list:
                if not job.is_old_job:
                        if not job.sitter:
                                pending.append(job)

                        if job.sitter:
                                accepted.append(job)

                if job.is_old_job:
                        past.append(job)

        for s in Babysitter.objects.order_by('id'):
                if not s.is_superuser:
                        sitters.append(s)
                        
        context= {'job_list':job_list, 'pending':pending, 'accepted':accepted, 'past':past, 'sitters':sitters, 'clients':clients  }
        # print(sitters)
        return render(request, 'sit/adminHome.html', context)


def sitterHome(request, sitter_id):
        sitter = get_object_or_404(Babysitter, pk=sitter_id)
        job_list = Job.objects.order_by('id')
        pending = []
        accepted = []
        past = []


        for job in job_list:
                if not job.is_old_job:
                        if not job.sitter:
                                pending.append(job)

                        if job.sitter == sitter:
                                accepted.append(job)

                if job.is_old_job and job.sitter == sitter:
                        past.append(job)

        context= {'job_list':job_list, 'pending':pending, 'accepted':accepted, 'past':past, 'sitter':sitter}
        return render(request, 'sit/sitterHome.html', context)


def showClient(request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        childset = Child.objects.all()
        children = []
        for child in childset:
                if child.child_parent == client:
                        children.append(child)
        return render(request, 'sit/client.html', {'client':client, 'children':children})