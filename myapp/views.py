import re
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect


# Create your views here.

# -------------------------------------------------login---------------------------------------------------------------------------------
from django.views.decorators.cache import never_cache

from myapp.models import *


def logins(request):
    return render(request,"logins.html")

def logins_post(request):
    username = request.POST['username']
    password = request.POST['password']
    data = authenticate(request,username=username,password=password)
    if data:
        login(request,data)
        if data.is_superuser:
            messages.success(request,"Welcome Admin")
            return redirect('/myapp/admin_dashboard')
        elif data.groups.filter(name="HOD").exists():
            request.session['hid'] = Hod.objects.get(USER=request.user.id).id
            request.session['depid'] = Hod.objects.get(id=request.session['hid']).STAFF.DEPARTMENT.id
            messages.success(request,"Welcome HOD")
            return redirect('/myapp/hod_dashboard')
        # elif data.groups.filter(name="staff").exists():
        #     messages.success(request,"Welcome Staff")
        #     return redirect('/myapp/staff_dashboard')
    else:
        messages.error(request, "Invalid Username or Password")
        return redirect('/myapp/')

def logouts(request):
    logout(request)
    return redirect('/myapp/')
# ----------------------------------------------------------admin------------------------------------------------------------------------
@login_required
@never_cache
def admin_dashboard(request):
    return render(request,"Admin/dashboard1.html")



#--------------------------- department----------------------------
@login_required
@never_cache
def add_department(request):
    return render(request,"Admin/add_department.html")
@login_required
@never_cache
def add_department_post(request):
    department_name = request.POST['department_name']
    department_details = request.POST['department_details']
    dep = department_details.capitalize()
    dep = re.sub(r'(?<=\.\s)([a-z])', lambda m: m.group(1).upper(), dep)

    if Department.objects.filter(department_name=department_name, department_details=department_details).exists():
        messages.error(request, "This Department is already existed")
        return redirect('/myapp/add_department')
    else:
        obj = Department()
        obj.department_name = department_name.title()
        obj.department_details = dep
        obj.save()
        messages.success(request, "Department is added")
        return redirect('/myapp/manage_department')

@login_required
@never_cache
def manage_department(request):
    data = Department.objects.all()
    for i in data:
        if Hod.objects.filter(STAFF__DEPARTMENT=i.id).exists():
            i.rstatus = "0"
    return render(request,"Admin/manage_department.html",{'data':data})

@login_required
@never_cache
def edit_department(request,id):
    data = Department.objects.get(id=id)
    print(data.department_name)
    return render(request,"Admin/edit_department.html",{'data':data})

@login_required
@never_cache
def edit_department_post(request):
    id = request.POST['id']
    department_name = request.POST['department_name']
    department_details = request.POST['department_details']
    dep = department_details.capitalize()
    dep = re.sub(r'(?<=\.\s)([a-z])', lambda m: m.group(1).upper(), dep)

    if Department.objects.filter(id=id,department_name=department_name, department_details=department_details,).exists():
        messages.error(request, "There is no changes")
        return redirect('/myapp/manage_department')
    else:
        obj = Department.objects.get(id=id)
        obj.department_name = department_name.title()
        obj.department_details = dep
        obj.save()
        messages.success(request, "Updated department")
        return redirect('/myapp/manage_department')

@login_required
@never_cache
def delete_department(request,id):
    Department.objects.get(id=id).delete()
    messages.error(request, "Deleted successfully")
    return redirect('/myapp/manage_department')

# ---------------------------------course--------------
@login_required
@never_cache
def add_course(request,id):
    return render(request,"Admin/add_course.html",{"id":id})

@login_required
@never_cache
def add_course_post(request):
    id= request.POST['id']
    course_name = request.POST['course_name']
    course_details = request.POST['course_details']
    cou = course_details.capitalize()
    cou = re.sub(r'(?<=\.\s)([a-z])', lambda m: m.group(1).upper(), cou)
    fee = request.POST['fee']
    total_semester = request.POST['total_semester']

    if Course.objects.filter(course_name=course_name, course_details=course_details,DEPARTMENT_id=id,fee=fee,total_semester=total_semester).exists():
        messages.error(request, "This Course is already existed")
        return redirect('/myapp/add_course/'+id)
    else:
        obj = Course()
        obj.course_name = course_name.title()
        obj.course_details = cou
        obj.fee = fee
        obj.DEPARTMENT_id = id
        obj.total_semester = total_semester
        obj.save()
        messages.success(request, "The Course is added successfully")
        return redirect('/myapp/manage_course/'+id)

@login_required
@never_cache
def manage_course(request,id):
    data = Course.objects.filter(DEPARTMENT_id=id)
    return render(request,"Admin/manage_course.html",{'data':data})

@login_required
@never_cache
def edit_course(request,id):
    data = Course.objects.get(id=id)
    return render(request,"Admin/edit_course.html",{'data':data})

@login_required
@never_cache
def edit_course_post(request):
    id = request.POST['id']
    course_name = request.POST['course_name']
    course_details = request.POST['course_details']
    cou = course_details.capitalize()
    cou = re.sub(r'(?<=\.\s)([a-z])', lambda m: m.group(1).upper(), cou)
    fee = request.POST['fee']
    total_semester = request.POST['total_semester']
    obj = Course.objects.get(id=id)

    if Course.objects.filter(id=id,course_name=course_name, course_details=course_details,fee=fee,total_semester=total_semester).exists():
        messages.error(request, "No Changes")
        return redirect('/myapp/manage_course/'+str(obj.DEPARTMENT_id))
    else:
        obj.course_name = course_name.title()
        obj.course_details = cou
        obj.fee = fee
        obj.total_semester = total_semester
        obj.save()
        messages.success(request, "Updated Successfully!!!!!!!!!!!")
        return redirect('/myapp/manage_course/'+str(obj.DEPARTMENT_id))

@login_required
@never_cache
def delete_course(request, id):
    dep_id= Course.objects.get(id=id).DEPARTMENT_id
    Course.objects.get(id=id).delete()
    messages.error(request, "Deleted successfully")
    return redirect('/myapp/manage_course/'+str(dep_id))

# --------------------------staff----------------------
@login_required
@never_cache
def add_staff(request,id):
    return render(request,"Admin/add_staff.html",{'id':id})

@login_required
@never_cache
def add_staff_post(request):
    id = request.POST['id']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    gender = request.POST['gender']
    house_name = request.POST['house_name']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pincode']
    file = request.FILES['image']
    fs = FileSystemStorage()
    file = fs.url(fs.save(file.name, file))
    qualification = request.POST['qualification']
    experience = request.POST['experience']
    pswd = str(random.randint(1010,9090))
    print("sataff password",pswd)
    if User.objects.filter(username=email).exists():
        messages.error(request,"Email is already existed")
        return redirect('/myapp/add_staff/'+id)
    else:
        obj = User()
        obj.username = email
        obj.password = make_password(pswd)
        obj.save()
        obj2 = Group.objects.filter(name="Staff")
        if obj2.exists():
            print("group already existed")
            obj.groups.add(Group.objects.get(name="Staff"))
        else:
            print("not existed")
            obj3 = Group()
            obj3.name = "staff"
            obj3.save()
            obj.groups.add(Group.objects.get(name="Staff"))
        data = Staff()
        data.name=name.title()
        data.email=email
        data.phone=phone
        data.gender=gender
        data.house_name=house_name.title()
        data.place=place.title()
        data.post=post.title()
        data.pin=pin
        data.qualification=qualification.capitalize()
        data.experience=experience
        data.image=file
        data.USER = obj
        data.DEPARTMENT_id = id
        data.save()
        messages.success(request,"The staff added successfully")
        return redirect('/myapp/manage_staff/'+id)

@login_required
@never_cache
def manage_staff(request,id):
    data = Staff.objects.filter(DEPARTMENT_id=id)
    return render(request,"Admin/manage_staff.html",{'data':data})

@login_required
@never_cache
def edit_staff(request,id):
    data = Staff.objects.get(id=id)
    return render(request,"Admin/edit_staff.html",{'data':data})

@login_required
@never_cache
def edit_staff_post(request):
    id = request.POST['id']
    data = Staff.objects.get(id=id)
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    gender = request.POST['gender']
    house_name = request.POST['house_name']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pincode']
    qualification = request.POST['qualification']
    experience = request.POST['experience']
    if Staff.objects.filter(id=id, name=name, email=email, phone=phone, gender=gender, house_name=house_name,place=place, post=post, pin=pin, qualification=qualification,experience=experience).exists():
        messages.error(request, "No changes!!!")
        return redirect('/myapp/manage_staff/'+str(data.DEPARTMENT_id))

    if 'image' in request.FILES:
        file = request.FILES['image']
        fs = FileSystemStorage()
        file = fs.url(fs.save(file.name, file))
        data.image = file
        data.save()
    data.name = name.title()
    data.email = email
    data.phone = phone
    data.gender = gender
    data.house_name = house_name.title()
    data.place = place.title()
    data.post = post.title()
    data.pin = pin
    data.qualification = qualification.capitalize()
    data.experience = experience
    data.save()
    messages.success(request, "Updated successfully")
    return redirect('/myapp/manage_staff/' + str(data.DEPARTMENT_id))

@login_required
@never_cache
def delete_staff(request,id):
    dep_id = Staff.objects.get(id=id).DEPARTMENT_id
    Staff.objects.get(id=id).delete()
    messages.error(request, "Deleted successfully")
    return redirect('/myapp/manage_staff/'+str(dep_id))

# ------------------------------------admin HOD--------------------------------------
@login_required
@never_cache
def add_hod(request,id):
    data = Staff.objects.filter(DEPARTMENT_id=id)
    return render(request,"Admin/add_hod.html",{'data':data})

@login_required
@never_cache
def setting_hod(request,id):
    return render(request,"Admin/hod_email.html",{'id':id})

@login_required
@never_cache
def setting_hod_post(request):
    id = request.POST['id']
    email = request.POST['email']
    pswd = random.randint(1010,9990)
    print("HOD password..............",pswd)
    if User.objects.filter(username=email).exists():
        messages.error(request,"Email is already existed")
        return redirect('/myapp/setting_hod/'+id)
    else:
        obj = User()
        obj.username = email
        obj.password = make_password(pswd)
        obj.save()
        obj2 = Group.objects.filter(name="HOD")
        if obj2.exists():
            print("group already existed")
            obj.groups.add(Group.objects.get(name="HOD"))
        else:
            print("not existed")
            obj3 = Group()
            obj3.name = "HOD"
            obj3.save()
            obj.groups.add(Group.objects.get(name="HOD"))
    data = Hod()
    data.STAFF_id = id
    data.USER = obj
    data.save()
    dep_id = data.STAFF.DEPARTMENT_id
    messages.success(request,"Allocated HOD successfully")
    return redirect('/myapp/view_hod/'+str(dep_id))
def view_hod(request,id):
    data = Hod.objects.filter(STAFF__DEPARTMENT=id)
    if data.exists():
        return render(request,"Admin/view_hod.html",{'data':data[0]})
    else:
        messages.error(request,"Please allocate Hod")
        return redirect('/myapp/manage_department')

@login_required
@never_cache
def remove_hod(request,id):
    dep_id = Hod.objects.get(id=id).STAFF.DEPARTMENT_id
    uid = Hod.objects.get(id=id).USER.id
    Hod.objects.get(id=id).delete()
    User.objects.get(id=uid).delete()
    # Hod.objects.get(id=id).delete()
    messages.error(request,"Deleted HOD successfully")
    return redirect('/myapp/add_hod/'+str(dep_id))

@login_required
@never_cache
def view_feedback(request):
    data = Feedback.objects.all()
    return render(request,"Admin/view_feedback.html",{'data':data})

@login_required
@never_cache
def send_reply(request,id):
    return render(request,"Admin/send_reply.html",{'id':id})

@login_required
@never_cache
def send_reply_post(request):
    id = request.POST['id']
    reply = request.POST['reply']
    rep = reply.capitalize()
    rep = re.sub(r'(?<=\.\s)([a-z])', lambda m: m.group(1).upper(), rep)

    data = Feedback.objects.get(id=id)
    data.reply = rep
    data.status = "viewed and replied"
    data.save()
    messages.success(request,"Replied successfully")
    return redirect('/myapp/view_feedback')

# ---------------------------------------------notification-----------------------

@login_required
@never_cache
def add_notification(request):
    data = Course.objects.all()
    start_date = datetime.now().date()
    new_date = start_date+timedelta()
    current_year = datetime.now().year
    years = range(current_year, current_year + 11)
    return render(request,"Admin/add_notification.html",{'new_date':str(new_date),'data':data,"years":years})

@login_required
@never_cache
def add_notification_post(request):
    course = request.POST['course']
    semester = request.POST['semester']
    start_date = request.POST['start_date']
    end_date = request.POST['last_date']
    amount = request.POST['amount']
    academic_year = request.POST['academic_year']

    if Notification.objects.filter(COURSE=course,semester=semester,start_date=start_date,end_date=end_date,amount=amount,academic_year=academic_year).exists():
        messages.error(request,"Notification is already given")
        return redirect('/myapp/add_notification')
    else:
        data = Notification()
        data.COURSE_id = course
        data.semester = semester
        data.start_date = start_date
        data.end_date = end_date
        data.amount = amount
        data.academic_year = academic_year
        data.save()
        messages.success(request,"Notification is added successfully")
    return redirect('/myapp/manage_notification')

@login_required
@never_cache
def manage_notification(request):
    data = Notification.objects.all()
    return render(request,"Admin/manage_notification.html",{'data':data})

@login_required
@never_cache
def edit_notification(request, id):
    start_date = datetime.now().date()
    new_date = start_date + timedelta()
    data = Notification.objects.get(id=id)
    course = Course.objects.all()
    current_year = datetime.now().year
    years = []
    for year in range(current_year, current_year + 11):
        years.append(f"{year}-{year + 1}")
    return render(request, "Admin/edit_notification.html", {"data": data,"course": course,"years": years,"new_date":new_date})
@login_required
@never_cache
def edit_notification_post(request):
    id = request.POST['id']
    course = request.POST['course']
    semester = request.POST['semester']
    start_date = request.POST['start_date']
    end_date = request.POST['last_date']
    amount = request.POST['amount']
    academic_year = request.POST['academic_year']

    if Notification.objects.filter(COURSE_id=course,semester=semester,start_date=start_date,end_date=end_date,amount=amount,academic_year=academic_year).exists():
        messages.error(request,"No changes!!!")
        return redirect('/myapp/manage_notification')
    else:
        data = Notification.objects.get(id=id)
        data.COURSE_id = course
        data.semester = semester
        data.start_date = start_date
        data.end_date = end_date
        data.amount = amount
        data.academic_year = academic_year
        data.save()
        messages.success(request,"Notification is edited successfully")
        return redirect('/myapp/manage_notification')

@login_required
@never_cache
def delete_notification(request,id):
    Notification.objects.get(id=id).delete()
    messages.error(request, "Deleted Notification Successfully")
    return redirect('/myapp/manage_notification')

@login_required
@never_cache
def view_payment(request,id):
    data = Payment.objects.filter(NOTIFICATION_id=id)
    return render(request,"Admin/view_payment.html",{'data':data})

# ------------------------------------change password----------------------------------
@login_required
@never_cache
def admin_change_password(request):
    return render(request,"Admin/change_password.html")

@login_required
@never_cache
def admin_change_password_post(request):
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    if check_password(current_password,request.user.password):
        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password Changed Successfully")
            return redirect('/myapp/')
        else:
            messages.error(request, "Please enter same Password")
            return redirect('/myapp/admin_change_password')


# -------------------------------------------------------HOD module-------------------------------------------------------------

@login_required
@never_cache
def hod_dashboard(request):
    return render(request,"Hod/dashboard.html")

@login_required
@never_cache
def view_course(request):
    data = Course.objects.filter(DEPARTMENT_id=request.session['depid'])
    return render(request,"Hod/view_course.html",{'data':data})

# ---------------------------student------------------
@login_required
@never_cache
def add_student(request):
    current_year = datetime.now().year
    years = range(current_year, current_year + 11)
    data = Course.objects.filter(DEPARTMENT_id=request.session['depid'])
    return render(request,"Hod/add_student.html",{'data':data,"years":years})

@login_required
@never_cache
def add_student_post(request):
    name = request.POST['name'].title()
    email = request.POST['email']
    phone = request.POST['phone']
    house_name = request.POST['house_name'].title()
    place = request.POST['place'].title()
    post = request.POST['post'].title()
    pin = request.POST['pin']
    register_no = request.POST['register_no']
    addmission_no = request.POST['addmission_no']
    course_name = request.POST['course']
    gender = request.POST['gender']
    parent_name = request.POST['parent_name'].title()
    parent_phone = request.POST['parent_phone']
    semester = request.POST['semester']
    addmission_date = request.POST['addmission_date']
    academic_year = request.POST['academic_year']
    file = request.FILES['image']
    fs = FileSystemStorage()
    file = fs.url(fs.save(file.name,file))

    pswd = random.randint(1010, 9990)
    print("Student password..............", pswd)
    if User.objects.filter(username=email).exists():
        messages.error(request, "Email is already existed")
        return redirect('/myapp/add_student')
    else:
        obj = User()
        obj.username = email
        obj.password = make_password(pswd)
        obj.save()
        obj2 = Group.objects.filter(name="Student")
        print(course_name,".................................................................")
        if obj2.exists():
            print("group already existed")
            obj.groups.add(Group.objects.get(name="Student"))
        else:
            print("not existed")
            obj3 = Group()
            obj3.name = "Student"
            obj3.save()
            obj.groups.add(Group.objects.get(name="Student"))
        data = Student()
        data.name = name
        data.email = email
        data.phone = phone
        data.house_name = house_name
        data.place = place
        data.post = post
        data.pin = pin
        data.register_no = register_no
        data.addmission_no = addmission_no
        data.COURSE_id = course_name
        data.gender = gender
        data.parent_name = parent_name
        data.parent_phone = parent_phone
        data.semester = semester
        data.academic_year = academic_year
        data.addmission_date = addmission_date
        data.image = file
        data.USER = obj
        data.save()
        messages.success(request, "Student added successfully")
    return redirect('/myapp/manage_student')

@login_required
@never_cache
def manage_student(request):
    data = Student.objects.filter(COURSE__DEPARTMENT=request.session['depid'])
    return render(request,"Hod/manage_student.html",{'data':data})

@login_required
@never_cache
def edit_student(request,id):
    course = Course.objects.filter(DEPARTMENT_id=request.session['depid'])
    data =Student.objects.get(id=id)
    current_year = datetime.now().year
    years = []
    for year in range(current_year, current_year + 11):
        years.append(f"{year}-{year + 1}")
    return render(request,"Hod/edit_student.html",{'data':data,'course':course,'id':id,"years":years})

@login_required
@never_cache
def edit_student_post(request):
    id = request.POST['id']
    data = Student.objects.get(id=id)
    name = request.POST['name'].title()
    email = request.POST['email']
    phone = request.POST['phone']
    house_name = request.POST['house_name'].title()
    place = request.POST['place'].title()
    post = request.POST['post'].title()
    pin = request.POST['pin']
    register_no = request.POST['register_no']
    addmission_no = request.POST['addmission_no']
    course_name = request.POST['course']
    gender = request.POST['gender']
    parent_name = request.POST['parent_name'].title()
    parent_phone = request.POST['parent_phone']
    semester = request.POST['semester']
    addmission_date = request.POST['addmission_date']
    academic_year = request.POST['academic_year']

    if 'file' in request.FILES:
        file = request.FILES['file']
        fs = FileSystemStorage()
        file = fs.url(fs.save(file.name, file))
        data.image = file
        data.name = name
        data.email = email
        data.phone = phone
        data.house_name = house_name
        data.place = place
        data.post = post
        data.pin = pin
        data.register_no = register_no
        data.addmission_no = addmission_no
        data.COURSE.id = course_name
        data.gender = gender
        data.parent_name = parent_name
        data.parent_phone = parent_phone
        data.semester = semester
        data.academic_year = academic_year
        data.addmission_date = addmission_date
        data.save()
        messages.success(request, "Updated successfully")
        return redirect('/myapp/manage_student')
    else:
        if Student.objects.filter(id=id, name=name, email=email, phone=phone, gender=gender, house_name=house_name,
                                  place=place, post=post, pin=pin, register_no=register_no, addmission_no=addmission_no,
                                  COURSE_id=course_name, parent_name=parent_name, parent_phone=parent_phone,
                                  semester=semester, addmission_date=addmission_date,
                                  academic_year=academic_year).exists():
            messages.error(request, "No changes!!!")
            return redirect('/myapp/manage_student')
        else:
            data.name = name
            data.email = email
            data.phone = phone
            data.house_name = house_name
            data.place = place
            data.post = post
            data.pin = pin
            data.register_no = register_no
            data.addmission_no = addmission_no
            data.COURSE.id = course_name
            data.gender = gender
            data.parent_name = parent_name
            data.parent_phone = parent_phone
            data.semester = semester
            data.academic_year = academic_year
            data.addmission_date = addmission_date
            data.save()
            messages.success(request, "Updated successfully")
            return redirect('/myapp/manage_student')


@login_required
@never_cache
def delete_student(request,id):
    Student.objects.get(id=id).delete()
    messages.error(request, "Deleted Successfully")
    return redirect('/myapp/manage_student')

# ----------------------------------------subject-----------------------------
@login_required
@never_cache
def add_subject(request):
    course = Course.objects.filter(DEPARTMENT_id=request.session['depid'])
    return render(request,"Hod/add_subject.html",{'data':course})

@login_required
@never_cache
def add_subject_post(request):
    sub_name = request.POST['sub_name'].title()
    sub_details = request.POST['sub_details']
    subject = sub_details.capitalize()
    subject = re.sub(r'(?<=\.\s)([a-z])', lambda m: m.group(1).upper(), subject)

    semester = request.POST['semester']
    course = request.POST['course']
    if Subject.objects.filter(sub_name=sub_name,sub_details=sub_details,semester=semester,COURSE_id=course).exists():
        messages.error(request, "Subject is already existed")
        return redirect('/myapp/add_subject')
    else:
        data = Subject()
        data.sub_name = sub_name
        data.sub_details = subject
        data.semester = semester
        data.COURSE_id = course
        data.save()
        messages.success(request, "Subject Added Successfully")
        return redirect('/myapp/manage_subject')

@login_required
@never_cache
def manage_subject(request):
    data = Subject.objects.filter(COURSE__DEPARTMENT=request.session['depid'])
    return render(request,"Hod/manage_subject.html",{'data':data})

@login_required
@never_cache
def edit_subject(request,id):
    course = Course.objects.filter(DEPARTMENT_id=request.session['depid'])
    data = Subject.objects.get(id=id)
    return render(request,"Hod/edit_subject.html",{'data':data,'course':course})

@login_required
@never_cache
def edit_subject_post(request):
    id = request.POST['id']
    sub_name = request.POST['sub_name']
    sub_details = request.POST['sub_details']
    subject = sub_details.capitalize()
    subject = re.sub(r'(?<=\.\s)([a-z])', lambda m: m.group(1).upper(), subject)
    semester = request.POST['semester']
    course = request.POST['course']
    if Subject.objects.filter(id=id,sub_name=sub_name,sub_details=sub_details,semester=semester,COURSE_id=course).exists():
        messages.error(request, "No Changes!!!")
        return redirect('/myapp/manage_subject')
    else:
        data = Subject.objects.get(id=id)
        data.sub_name = sub_name
        data.sub_details = subject
        data.semester = semester
        data.COURSE_id = course
        data.save()
        messages.success(request,"Updated Subject Successfully")
        return redirect('/myapp/manage_subject')

@login_required
@never_cache
def delete_subject(request,id):
    Subject.objects.get(id=id).delete()
    messages.error(request, "Deleted Successfully")
    return redirect('/myapp/manage_subject')

# ------------------------------------------chat------------------
@login_required
@never_cache
def allocate_staff(request,id):
    staff = Staff.objects.filter(DEPARTMENT_id=request.session['depid'])
    current_year = datetime.now().year
    years = range(current_year, current_year + 11)
    # context = {
    #     'years': years,
    # }
    return render(request,"Hod/allocate_staff.html",{'years':years,'id':id,'staff':staff})

@login_required
@never_cache
def allocate_staff_post(request):
    id = request.POST['id']
    staff_id = request.POST['staff']
    academic_year = request.POST['academic_year']
    if Subject_staff.objects.filter(SUBJECT_id=id,academic_year=academic_year,STAFF_id=staff_id).exists():
        messages.error(request,"Subject's staff is already allocated")
        return redirect('/myapp/allocated_staff_subject')
    else:
        data = Subject_staff()
        data.academic_year=academic_year
        data.STAFF_id = staff_id
        data.SUBJECT_id = id
        data.save()
        messages.success(request,"Staff is allocated successfully")
        return redirect('/myapp/allocated_staff_subject')

@login_required
@never_cache
def allocated_staff_subject(request):
    data = Subject_staff.objects.all()
    return render(request,"Hod/subject_staff_view.html",{'data':data})
# ------------------------------------------chat------------------

@login_required
@never_cache
def chatt(request, u):
    request.session['head'] = "CHAT"
    request.session['uid'] = u
    return render(request, 'Hod/chat.html', {'u': u})


@login_required
@never_cache
def chatsnd(request):
    m = request.POST.get('m', '').strip()
    # Create and save chat message
    obj = Chat(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Added time
        type='hod',
        STUDENT_id=request.session['uid'],
        HOD_id=request.session['hid'],
        message=m
    )
    obj.save()

    return JsonResponse({"status": "ok", "message_id": obj.id})


@login_required
@never_cache
def chatrply(request):
    last_id = request.POST.get('last_id', 0)
    try:
        last_id = int(last_id)
    except ValueError:
        last_id = 0

    # Get messages with proper ordering and filtering
    messages = Chat.objects.filter(
        STUDENT=request.session['uid'],
        id__gt=last_id  # Only get messages newer than last_id
    ).order_by('id')  # Ensure chronological order

    v = []
    for i in messages:
        v.append({
            'id': i.id,  # Include message ID for tracking
            'type': i.type,
            'chat': i.message,
            'selimage': i.HOD.STAFF.image,  # You can add actual image paths here
            'uimage': i.STUDENT.image,  # You can add actual image paths here
            'date': i.date,
        })

    return JsonResponse({
        "status": "ok",
        "data": v,
        "count": len(v),
        "last_id": messages.last().id if messages else last_id
    })


# -------------------------------change password-------------------
@login_required
@never_cache
def hod_change_password(request):
    return render(request,"Hod/change_password.html")

@login_required
@never_cache
def hod_change_password_post(request):
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    if check_password(current_password,request.user.password):
        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password Changed Successfully")
            return redirect('/myapp/')
        else:
            messages.success(request, "Password Changed Successfully")
            return redirect('/myapp/hod_change_password')
# ============================================view hod profile================
@login_required
@never_cache
def my_profile(request):
    data = Hod.objects.get(id=request.session['hid'])
    return render(request,"Hod/my_profile.html",{'data':data})

# -----------------------------------------------forgot password-----------------------------------------------------------------------

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, Group
import random
from django.conf import settings
import os

def forgotpassword(request):
    return render(request, "forgotpassword.html")


def forgotpasswordbuttonclick(request):
    email = request.POST['textfield']
    if User.objects.filter(username=email).exists():

        pwd = str(random.randint(1100, 9999))

        request.session['otp'] = pwd
        request.session['email'] = email

        subject = f"Your OTP - {os.path.basename(settings.BASE_DIR)}"

        html_content = f"""
        <html>
        <body style="font-family:Arial,sans-serif;">
            <h2 style="color:#2c7be5;">{os.path.basename(settings.BASE_DIR)}</h2>

            <p>Hello,</p>

            <p>Your OTP is:</p>

            <div style="
                padding:10px;
                border:1px solid #ddd;
                display:inline-block;
                font-size:20px;
                font-weight:bold;
                color:#2c7be5;
                background:#f5f5f5;
            ">
                {pwd}
            </div>

            <p>Please do not share this OTP with anyone.</p>

            <hr>
            <small>This is an automated email from {os.path.basename(settings.BASE_DIR)}.</small>

        </body>
        </html>
        """

        email_message = EmailMultiAlternatives(
            subject=subject,
            body="Your OTP: " + pwd,
            from_email=None,
            to=[email]
        )

        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return HttpResponse(
            "<script>window.location='/myapp/otp'</script>"
        )

    else:
        return HttpResponse(
            "<script>alert('Email not found');window.location='/myapp/forgotpassword'</script>"
        )


def otp(request):
    return render(request,"otp.html")


def otpbuttonclick(request):
    otp = request.POST["textfield"]

    if otp == str(request.session['otp']):
        return HttpResponse("<script>window.location='/myapp/forgotpswdpswed'</script>")
    else:
        return HttpResponse("<script>alert('Incorrect OTP');window.location='/myapp/otp'</script>")


def forgotpswdpswed(request):
    return render(request,"forgotpswdpswed.html")


def forgotpswdpswedbuttonclick(request):
    np = request.POST["password"]

    User.objects.filter(
        username=request.session['email']
    ).update(password=make_password(np))

    return HttpResponse(
        "<script>alert('Password changed successfully');window.location='/myapp/'</script>"
    )

# ---------------------------------------------Student app----------------------------------------------------------------------

def logins_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    data = authenticate(request,username=username,password=password)
    if data:
        login(request,data)
        if data.groups.filter(name="Student").exists():
            user_id = Student.objects.get(USER=request.user.id).id
            return JsonResponse({'status':"Welcome Student","user_id":user_id})
        else:
            print("not existed....................")
            return JsonResponse({'status': "Invalid Username and Password"})
    else:
        print("......................................not existed")
        return JsonResponse({'status':"Invalid Username and Password"})

# --------------------------change password------------
def change_password_flutter(request):
    data = Student.objects.get(id=request.POST['user_id'])
    newpassword = request.POST['password']
    User.objects.filter(id=data.USER.id).update(password=make_password(newpassword))
    return JsonResponse({"status":"Updated Password Successfully"})

# --------------------------view profile-----------------------
def student_profile_flutter(request):
    user_id = request.POST['user_id']
    data = Student.objects.get(id=user_id)
    return JsonResponse({"name":data.name,"email":data.email,"phone":data.phone,"house_name":data.house_name,"place":data.place,"post":data.post,"pin":data.pin,"register_no":data.register_no,"addmission_no":data.addmission_no,"course_name":data.COURSE.course_name,"parent_name":data.parent_name,"parent_phone":data.parent_phone,"semester":data.semester,"addmission_date":data.addmission_date,"academic_year":data.academic_year,"image":data.image,"gender":data.gender})

# ------------------------view course-----------------------------------

def view_course_info_flutter(request):
    user_id = request.POST['user_id']
    data = Student.objects.get(id=user_id)
    return JsonResponse({"course_name":data.COURSE.course_name,"course_details":data.COURSE.course_details,"department_name":data.COURSE.DEPARTMENT.department_name,"department_details":data.COURSE.DEPARTMENT.department_details,"fee":data.COURSE.fee,"total_semester":data.COURSE.total_semester,})

# ------------------------view subject and staff-----------------------------------

def view_subject_flutter(request):
    # user_id = request.POST['user_id']
    id = Student.objects.get(id=request.POST['user_id']).COURSE.id
    academic = Student.objects.get(id=request.POST['user_id']).academic_year
    data = Subject_staff.objects.filter(SUBJECT__COURSE=id,academic_year=academic)
    ab = []
    for i in data:
        ab.append({
            "id":i.id,
            "staff_name":i.STAFF.name,
            "staff_qualification":i.STAFF.qualification,
            "staff_email":i.STAFF.email,
            "subject_name":i.SUBJECT.sub_name,
            "subject_details":i.SUBJECT.sub_details,
            "semester":i.SUBJECT.semester,
            "academic_year":i.academic_year
        })
    return JsonResponse({"status":"viewed successfully","data":ab})

def view_hod_flutter(request):
    id = Student.objects.get(id=request.POST['user_id']).COURSE.DEPARTMENT.id
    data = Hod.objects.get(STAFF__DEPARTMENT=id)
    print(data.STAFF.experience,data.STAFF.qualification)
    return JsonResponse({"id":data.id,"name":data.STAFF.name,"email":data.USER.username,"phone":data.STAFF.phone,"qualification":data.STAFF.qualification,"experience":data.STAFF.experience,"gender":data.STAFF.gender,"image":data.STAFF.image})

def chat_flutter(request):
    id = request.POST['user_id']
    return JsonResponse({"status":"Welcome Student"})

def view_notification_flutter(request):
    id = request.POST['user_id']
    sem = Student.objects.get(id=id).semester
    course_id = Student.objects.get(id=id).COURSE.id
    data = Notification.objects.filter(semester=sem,COURSE=course_id)
    ab = []
    for i in data:
        if Payment.objects.filter(NOTIFICATION_id=i.id,STUDENT_id=id).exists():
            print("its paid")
            current_date = datetime.now().date()
            if i.start_date <= current_date and i.end_date >= current_date:
                rstatus = "1"
                # make payment
            else:
                rstatus = "0"
                # no make payment
            # if i.end_date>= current_date:
            #     mstatus = "1"
            # else:
            #     mstatus = "0"
            ab.append({
                "id": i.id,
                "semester": i.semester,
                "course_name": i.COURSE.course_name,
                "amount": i.amount,
                "start_date": i.start_date,
                "end_date": i.end_date,
                "academic_year": i.academic_year,
                "rstatus": rstatus,
                "payment": "paid",
                # "mstatus":mstatus,
            })
        else:
            current_date = datetime.now().date()
            if i.start_date <= current_date and i.end_date>= current_date:
                rstatus = "1"
                # make payment
            else:
                rstatus = "0"
                # no make payment
            # if i.end_date>= current_date:
            #     mstatus = "1"
            # else:
            #     mstatus = "0"
            ab.append({
                "id": i.id,
                "semester": i.semester,
                "course_name": i.COURSE.course_name,
                "amount": i.amount,
                "start_date": i.start_date,
                "end_date": i.end_date,
                "academic_year": i.academic_year,
                "rstatus":rstatus,
                "payment":"1"
                # "mstatus":mstatus,
            })
    return JsonResponse({"status":"Here is your fee notification","data":ab})

def payment_histoy_flutter(request):
    uid = request.POST['user_id']
    data = Payment.objects.filter(STUDENT_id=uid,status="paid")
    ab = []
    for i in data:
        ab.append({
            "id": i.id,
            "Course_name": i.NOTIFICATION.COURSE.course_name,
            "amount": i.NOTIFICATION.amount,
            "payment_method": i.payment_method,
            "date": i.date,
        })
    return JsonResponse({"status": "Here is your payment history", "data": ab})

def send_feedback_flutter(request):
    feedback = request.POST['feedback']
    id = request.POST['user_id']
    data = Feedback()
    data.feedback = feedback
    data.date = datetime.now().date()
    data.status = "Not viewed"
    data.reply = "no reply yet"
    data.STUDENT_id = id
    data.save()
    return JsonResponse({'status':"Thank you for your feedback"})

def view_feedback_flutter(request):
    id = request.POST['user_id']
    data = Feedback.objects.filter(STUDENT=id)
    ab = []
    for i in data:
        ab.append({
            "id": i.id,
            "feedback": i.feedback,
            "date": i.date,
            "status": i.status,
            "reply": i.reply,
        })
    return JsonResponse({"data": ab})

def forgotemail(request):
    from django.core.mail import EmailMultiAlternatives
    from django.http import JsonResponse
    from django.contrib.auth.models import User
    from django.conf import settings
    from datetime import datetime
    import random
    import os
    email = request.POST['email']

    data = User.objects.filter(username=email)

    if data.exists():

        otp = str(random.randint(100000, 999999))

        # store in session instead of returning to client
        request.session['otp'] = otp
        request.session['email'] = email

        try:

            project_name = os.path.basename(settings.BASE_DIR)

            subject = "🔑 Forgot Password"

            html = f"""
                            <!DOCTYPE html>
                            <html>
                            <body style="font-family:Arial,sans-serif">

                                <div style="
                                background:#2c7be5;
                                padding:20px;
                                text-align:center;
                                color:white">

                                    <h1>{project_name}</h1>

                                </div>

                                <div style="padding:25px">

                                    <h2>Password Reset Request</h2>

                                    <p>Hello,</p>

                                    <p>Use the OTP below:</p>

                                    <div style="
                                    text-align:center;
                                    font-size:30px;
                                    font-weight:bold;
                                    letter-spacing:8px;
                                    color:#2c7be5;
                                    border:1px dashed #ccc;
                                    padding:15px">

                                        {otp}

                                    </div>

                                    <p>Valid for 10 minutes</p>

                                    <p>
                                    Never share this OTP with anyone.
                                    </p>

                                    <hr>

                                    <small>
                                    © {datetime.now().year}
                                    {project_name}
                                    </small>

                                </div>

                            </body>
                            </html>
                            """

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=f"Your OTP: {otp}",
                to=[email]
            )

            email_message.attach_alternative(
                html,
                "text/html"
            )

            email_message.send()

            return JsonResponse({
                'status': 'ok',"otpp":otp
            })

        except Exception as e:

            print(e)

            return JsonResponse({
                'status': 'mail failed'
            })

    return JsonResponse({
        'status': 'not found'
    })

def forgotpass(request):
    email = request.POST['email']
    npass = request.POST['password']
    cpass = request.POST['confirmpassword']
    print(email, npass, cpass)
    if npass == cpass:
        User.objects.filter(username=email).update(password=make_password(npass))
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'})


# ------------------------------------------chat flutter-------------------------

def user_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']



    # print(FROM_id, TOID_id,"Lk")



    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.STUDENT_id=FROM_id
    c.HOD_id=TOID_id
    c.message=msg
    c.type='student'
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})

def user_viewchat(request):
    from_id=request.POST['from_id']
    to_id=request.POST['to_id']
    # print(to_id)

    l=[]
    data=Chat.objects.filter(STUDENT=from_id,HOD=to_id).order_by('id')

    # data= Chat.objects.all()

    for res in data:
        l.append({'id':res.id,'from':res.STUDENT.id,'to':res.HOD.id,'msg':res.message,'date':res.date,'type':res.type})

    return JsonResponse({'status':"ok",'data':l})
# ---------------------------payment flutter--------------------------------

def make_payment_flutter(request):
    noti_id = request.POST['notification_id']
    user_id = request.POST['user_id']
    if Payment.objects.filter(STUDENT_id=user_id,NOTIFICATION_id=noti_id).exists():
        return JsonResponse({'status':"payment already done"})
    else:
        return JsonResponse({'status':"payment not done"})

def payment_flutter(request):
    mode = request.POST['mode']
    user_id = request.POST['user_id']
    noti_id = request.POST['notification_id']
    print(mode,"......................................................................")
    data = Payment()
    data.payment_method = mode
    data.STUDENT_id = user_id
    data.NOTIFICATION_id = noti_id
    data.status = "paid"
    data.date = datetime.now().date()
    data.save()
    return JsonResponse({'status':"ok"})