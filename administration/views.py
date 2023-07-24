from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from administration.forms import *
from administration.models import *
from administration.filters import *

# Create your views here.

######################################
def index(request):
    if Book.objects.all().count == 0:
        data = None
        data1 = None 
    elif Book.objects.count() > 4:
        data = Book.objects.all().order_by('rel_date')[0]
        data1 = Book.objects.all().order_by('rel_date')[1:4]
    elif Book.objects.count ==1:
        data = Book.objects.all().order_by('rel_date')[0]
    else:
        data = Book.objects.all().order_by('rel_date').last()
        data1 = Book.objects.all().order_by('rel_date')[1:]

    if Organization.objects.all().exists() == False:
        search = "India"
    else:
        data = Organization.objects.last()
        search = ("+".join([data.name, data.building, data.city, data.state, data.country])).replace(' ', '+')

    if request.method == 'POST':
        msg = Message.objects.create(receiver = Login.objects.first(), contact = int(request.POST.get('contact')) ,message = request.POST.get('message'), time = datetime.datetime.now())
        return redirect('/')
    return render(request, 'index.html', {'data':data, 'data1':data1, 'search':search})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dash')
            elif user.is_subadmin:
                return redirect('subadmin_dash')
            elif user.is_librarian:
                return redirect('librarian_dash')
            elif user.is_customer:
                return redirect('customer_dash')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request,'log.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')
    
################################################

###########################ADMIN SIDE###########################
def admin_check(user):
    return user.is_staff

@user_passes_test(admin_check, login_url="login_view")
def admin_dash(request):
    return render(request, 'admintemp/dashboard.html')

@user_passes_test(admin_check, login_url="login_view")
def admin_profile(request):
    data1 = request.user
    data2 = Organization.objects.last()
    return render(request, 'admintemp/profile.html', {'data1':data1, 'data2':data2})

@user_passes_test(admin_check, login_url="login_view")
def subadmin_register(request):
    login_form = LoginRegister()
    subadmin_form = SubAdminForm()
    if request.method == 'POST':
        login_form = LoginRegister(request.POST)
        subadmin_form = SubAdminForm(request.POST, request.FILES)
        if login_form.is_valid() and subadmin_form.is_valid():
            user = login_form.save(commit = False)
            user.is_subadmin = True
            user.save()
            sa = subadmin_form.save(commit = False)
            sa.user = user
            sa.save()
            messages.info(request, "Sub-Admin Registration Successfull")
            return redirect('admin_dash')   
    return render(request, 'admintemp/add_subadmin.html', {'login_form':login_form, 'subadmin_form': subadmin_form})

@user_passes_test(admin_check, login_url="login_view")
def view_subadmin(request):
    data = SubAdmin.objects.all()
    return render(request, 'admintemp/view_subadmin.html', {'data':data})

@user_passes_test(admin_check, login_url="login_view")
def edit_subadmin(request,id):
    data = SubAdmin.objects.get(id=id)
    form = SubAdminForm(instance=data)
    if request.method == 'POST':
        form = SubAdminForm(request.POST or None, request.FILES or None, instance=data)
        if  form.is_valid():
            form.save()
            messages.info(request, "Sub-Admin Successfully Edited")
            return redirect('view_subadmin')
    return render(request, 'admintemp/edit_subadmin.html', {'form':form})

@user_passes_test(admin_check, login_url="login_view")
def delete_subadmin(request,id):
    sa = SubAdmin.objects.get(id = id)
    data = Login.objects.get(subadmin = sa)
    if request.method == 'POST':
        data.delete()
        messages.info(request, "Sub-Admin Successfully Deleted")
    return redirect('view_subadmin')

@user_passes_test(admin_check, login_url="login_view")
def address(request):
    if Organization.objects.all().exists() == False:
        form = OrganizationForm()
        data = None
        search = "India"
    else:
        data = Organization.objects.last()
        form = OrganizationForm(instance = data)
        search = ("+".join([data.name, data.building, data.city, data.state, data.country])).replace(' ', '+')
    if request.method == 'POST':
        form = OrganizationForm(request.POST or None)
        if  form.is_valid():
            if data != None:
                data.delete()
            form.save()
            return redirect('address')
    return render(request, 'admintemp/address.html', {'form':form, 'search':search})

@user_passes_test(admin_check, login_url="login_view")
def admin_msg_sent(request):
    msg = Message.objects.filter(sender = request.user)
    return render(request, 'admintemp/admin_msg_sent.html', {'msg':msg})

@user_passes_test(admin_check, login_url="login_view")
def admin_msg_recv(request):
    msg = Message.objects.filter(receiver = request.user)
    return render(request, 'admintemp/admin_msg_recv.html', {'msg':msg})

@user_passes_test(admin_check, login_url="login_view")
def admin_msg(request):
        form = MessageForm()
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                msg = Message.objects.create(sender = request.user, receiver = Login.objects.get(id = form['receiver'].value()), contact = form['contact'].value(), message = form['message'].value(), time = datetime.datetime.now())
            return redirect('admin_msg_sent')
        return render(request, 'admintemp/admin_msg.html', {'form':form})

@user_passes_test(admin_check, login_url="login_view")
def del_admin_sent(request, id):
    msg = Message.objects.get(id = id)
    msg.delete()
    return redirect('admin_msg_sent')

################################################

###########################SUB-ADMIN SIDE###########################

def subadmin_check(user):
    return user.is_subadmin

@user_passes_test(subadmin_check, login_url="login_view")
def subadmin_dash(request):
    return render(request, 'subadmintemp/dashboard.html')

@user_passes_test(subadmin_check, login_url="login_view")
def subadmin_profile(request):
    data = SubAdmin.objects.get(user = request.user)
    return render(request, 'subadmintemp/profile.html', {'data':data})

@user_passes_test(subadmin_check, login_url="login_view")
def subadmin_settings(request):
    data = request.user
    return render(request, 'subadmintemp/settings.html', {'data':data})

@user_passes_test(subadmin_check, login_url="login_view")
def add_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "New Book Added Successfully")
            return redirect('add_book')
    return render(request, 'subadmintemp/add_book.html', {'form':form})

@user_passes_test(subadmin_check, login_url="login_view")
def view_book(request):
    book = Book.objects.all()
    itemFilter = BookFilter(request.GET, queryset = book)
    data = itemFilter.qs
    return render(request, 'subadmintemp/view_book.html', {'data':data, 'itemFilter':itemFilter})

@user_passes_test(subadmin_check, login_url="login_view")
def edit_book(request,id):
    data = Book.objects.get(id=id)
    form = BookForm(instance=data)
    if request.method == 'POST':
        form = BookForm(request.POST or None, request.FILES or None, instance=data)
        if  form.is_valid():
            form.save()
            messages.info(request, "Book Successfully Edited")
            return redirect('view_book')
    return render(request, 'subadmintemp/edit_book.html', {'form':form})

@user_passes_test(subadmin_check, login_url="login_view")
def delete_book(request,id):
    data = Book.objects.get(id=id)
    data.delete()
    messages.info(request, "Book Successfully Deleted")
    return redirect('view_book')

@user_passes_test(subadmin_check, login_url="login_view")
def view_customer(request):
    user = Customer.objects.all()
    itemFilter = CustomerFilter(request.GET, queryset = user)
    data = itemFilter.qs
    return render(request, 'subadmintemp/view_customer.html', {'data':data, 'itemFilter':itemFilter})

@user_passes_test(subadmin_check, login_url="login_view")
def edit_customer(request,id):
    data = Customer.objects.get(id=id)
    form = CustomerForm(instance=data)
    if request.method == 'POST':
        form = CustomerForm(request.POST or None, request.FILES or None, instance=data)
        if  form.is_valid():
            form.save()
            messages.info(request, "User Information Successfully Edited")
            return redirect('view_customer')
    return render(request, 'subadmintemp/edit_customer.html', {'form':form})

@user_passes_test(subadmin_check, login_url="login_view")
def delete_customer(request,id):
    st = Customer.objects.get(id = id)
    data = Login.objects.get(customer = st)
    if request.method == 'POST':
        data.delete()
        messages.info(request, "User Successfully Deleted")
    return redirect('view_customer')

@user_passes_test(subadmin_check, login_url="login_view")
def customer_register(request):
    login_form = LoginRegister()
    customer_form = CustomerForm()
    if request.method == 'POST':
        login_form = LoginRegister(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)
        if login_form.is_valid() and customer_form.is_valid():
            user = login_form.save(commit = False)
            user.is_customer = True
            user.save()
            st = customer_form.save(commit = False)
            st.user =  user
            st.save()
            messages.info(request, "User Registration Successfull")
            return redirect('customer_register')
    
    return render(request, 'subadmintemp/add_customer.html', {'login_form':login_form, 'customer_form': customer_form})

@user_passes_test(subadmin_check, login_url="login_view")
def librarian_register(request):
    login_form = LoginRegister()
    librarian_form = LibrarianForm()
    if request.method == 'POST':
        login_form = LoginRegister(request.POST)
        librarian_form = LibrarianForm(request.POST, request.FILES)
        if login_form.is_valid() and librarian_form.is_valid():
            user = login_form.save(commit = False)
            user.is_librarian = True
            user.save()
            sa = librarian_form.save(commit = False)
            sa.user =  user
            sa.save()
            messages.info(request, "Librarian Registration Successfull")
            return redirect('subadmin_dash')
    
    return render(request, 'subadmintemp/add_librarian.html', {'login_form':login_form, 'librarian_form': librarian_form})

@user_passes_test(subadmin_check, login_url="login_view")
def view_librarian(request):
    data = Librarian.objects.all()
    return render(request, 'subadmintemp/view_librarian.html', {'data':data})

@user_passes_test(subadmin_check, login_url="login_view")
def edit_librarian(request,id):
    data = Librarian.objects.get(id=id)
    form = LibrarianForm(instance=data)
    if request.method == 'POST':
        form = LibrarianForm(request.POST or None, request.FILES or None, instance=data)
        if  form.is_valid():
            form.save()
            messages.info(request, "Librarian Information Successfully Edited")
            return redirect('view_librarian')
    return render(request, 'subadmintemp/edit_librarian.html', {'form':form})

@user_passes_test(subadmin_check, login_url="login_view")
def delete_librarian(request,id):
    sa = Librarian.objects.get(id = id)
    data = Login.objects.get(librarian = sa)
    if request.method == 'POST':
        data.delete()
        messages.info(request, "Librarian Successfully Deleted")
    return redirect('view_librarian')

@user_passes_test(subadmin_check, login_url="login_view")
def genre(request):
    form = GenreForm()
    data = Genre.objects.all()     
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre')
    return render(request, 'subadmintemp/genre.html', {'data':data, 'form':form})

@user_passes_test(subadmin_check, login_url="login_view")
def delete_genre(request,id):
    data = Genre.objects.get(id=id)
    data.delete()
    return redirect('genre')

@user_passes_test(subadmin_check, login_url="login_view")
def language(request):
    form = LanguageForm()
    data = Language.objects.all()     
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('language')
    return render(request, 'subadmintemp/language.html', {'data':data, 'form':form})

@user_passes_test(subadmin_check, login_url="login_view")
def delete_lang(request,id):
    data = Language.objects.get(id=id)
    data.delete()
    return redirect('language')

@user_passes_test(subadmin_check, login_url="login_view")
def occupation(request):
    form = OccupationForm()
    data = Occupation.objects.all()     
    if request.method == 'POST':
        form = OccupationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('occupation')
    return render(request, 'subadmintemp/occupation.html', {'data':data, 'form':form})

@user_passes_test(subadmin_check, login_url="login_view")
def delete_occ(request,id):
    data = Occupation.objects.get(id=id)
    data.delete()
    return redirect('occupation')

@user_passes_test(subadmin_check, login_url="login_view")
def configure(request):
    if Configure.objects.all().exists() == False:
        form = ConfigureForm()
        data = None
    else:
        data = Configure.objects.last()
        form = ConfigureForm(instance = data)
    if request.method == 'POST':
        form = ConfigureForm(request.POST or None)
        if  form.is_valid():
            if data != None:
                data.delete()
            form.save()
            messages.info(request, "Configuration Successfull")
            return redirect('subadmin_dash')
    return render(request, 'subadmintemp/configure.html', {'form':form})   

@user_passes_test(subadmin_check, login_url="login_vie")
def subadmin_msg_sent(request):
    msg = Message.objects.filter(sender = request.user)
    return render(request, 'subadmintemp/subadmin_msg_sent.html', {'msg':msg})

@user_passes_test(subadmin_check, login_url="login_view")
def subadmin_msg_recv(request):
    msg = Message.objects.filter(receiver = request.user)
    return render(request, 'subadmintemp/subadmin_msg_recv.html', {'msg':msg})

@user_passes_test(subadmin_check, login_url="login_view")
def subadmin_msg(request):
        form = MessageForm()
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                msg = Message.objects.create(sender = request.user, receiver = Login.objects.get(id = form['receiver'].value()), contact = form['contact'].value(), message = form['message'].value(), time = datetime.datetime.now())
            return redirect('subadmin_msg_sent')
        return render(request, 'subadmintemp/subadmin_msg.html', {'form':form})

@user_passes_test(subadmin_check, login_url="login_view")
def del_subadmin_sent(request, id):
    msg = Message.objects.get(id = id)
    if request.method == 'POST':
        msg.delete()
    return redirect('subadmintemp/subadmin_msg_sent')

@user_passes_test(subadmin_check, login_url="login_view")
def del_subadmin_sent(request, id):
    msg = Message.objects.get(id = id)
    msg.delete()
    return redirect('subadmin_msg_sent')

################################################

###########################LIBRARIAN SIDE###########################

def lib_check(user):
    return user.is_librarian

@user_passes_test(lib_check, login_url="login_view")
def librarian_dash(request):
    return render(request, 'librariantemp/dashboard.html')

@user_passes_test(lib_check, login_url="login_view")
def customer_view(request):
    user = Customer.objects.all()
    itemFilter = CustomerFilter(request.GET, queryset = user)
    data = itemFilter.qs
    return render(request, 'librariantemp/view_customer.html', {'data':data, 'itemFilter':itemFilter})

@user_passes_test(lib_check, login_url="login_view")
def libra_profile(request):
    u = request.user
    data = Librarian.objects.get(user = u)
    return render(request, 'librariantemp/profile.html', {'data':data})

@user_passes_test(lib_check, login_url="login_view")
def view_books(request):
    genres = Genre.objects.all()
    langs = Language.objects.all() 
    genreID = request.GET.get('genre')
    langID = request.GET.get('lang')
    if genreID:
        book = Book.objects.filter(genre = genreID)
    elif langID:
        book = Book.objects.filter(lang = langID)
    elif genreID and langID:
        book = Book.objects.filter(genre = genreID, lang = langID)
    else:
        book = Book.objects.all()

    itemFilter = BookFilter(request.GET, queryset = book)
    data = itemFilter.qs
    return render(request, 'librariantemp/view_book.html', {'data':data, 'genres':genres, 'langs':langs, 'itemFilter':itemFilter})

@user_passes_test(lib_check, login_url="login_view")
def issue(request,id):
    bk = Book.objects.get(id = id)
    cop = bk.copies
    if cop == 0:
        avail = False
    else:
        avail = True
    roll = IntForm()
    if request.method == 'POST':
        try:
            conf = Configure.objects.last()
            st = Customer.objects.get(roll_no = request.POST['roll'])
        except:
            messages.info(request, "Record Error")
            return redirect('view_books')
        if Reserve.objects.filter(user = st.user, book = bk, status = "ISSUED").exists():
            messages.info(request, "Record Already Exists")
            return redirect('view_books')
        rs = Reserve.objects.create(user = st.user, book = bk, valid_till = datetime.date.today() + datetime.timedelta(days = conf.issue_till), status ="ISSUED")
        if Reserve.objects.filter(user = st.user, book = bk, status = "RESERVED").exists():
            Reserve.objects.get(user = st.user, book = bk, status = "RESERVED").delete()
        else:
            bk.copies = cop - 1
            bk.save()
        messages.info(request, "Book Issued")
        return redirect('view_books')
    return render(request, 'librariantemp/issue.html', {'roll':roll, 'book':bk, 'avail':avail})

@user_passes_test(lib_check, login_url="login_view")
def issue_book(request):
    roll = IntForm()
    isbn = IntForm()
    if request.method == 'POST':
        try:
            conf = Configure.objects.last()
            st = Customer.objects.get(roll_no = request.POST['roll'])
            bk = Book.objects.get(isbn = request.POST['isbn'])
        except:
            messages.info(request, "Record Error")
            return redirect('issue_book')
        if Reserve.objects.filter(user = st.user, book = bk, status = "ISSUED").exists():
            messages.info(request, "Record Already Exists")
            return redirect('view_books')
        rs = Reserve.objects.create(user = st.user, book = bk, valid_till = datetime.date.today() + datetime.timedelta(days = conf.issue_till), status ="ISSUED")
        if Reserve.objects.filter(user = st.user, book = bk, status = "RESERVED").exists():
            Reserve.objects.get(user = st.user, book = bk, status = "RESERVED").delete()
        else:
            bk.copies = bk.copies - 1
            bk.save()
        messages.info(request, "Book Issued")
        return redirect('issue_book')
    return render(request, 'librariantemp/issue_book.html', {'roll':roll, 'isbn':isbn})

@user_passes_test(lib_check, login_url="login_view")
def return_book(request):
    roll = IntForm()
    isbn = IntForm()
    if request.method == 'POST':
        try:
            st = Customer.objects.get(roll_no = request.POST['roll'])
            bk = Book.objects.get(isbn = request.POST['isbn'])
            rs = Reserve.objects.get(user = st.user, book = bk, status = "ISSUED")
            conf = Configure.objects.last()
        except:
            messages.info(request, "Record Error")
            return redirect('return_book')
        if rs.valid_till < datetime.date.today() and conf.interval > 0 and conf.fine != 0:
            n = (rs.valid_till - datetime.date.today()).days/conf.interval 
            if conf.hike < 0:
                n1 = conf.fine//conf.hike
                n = min(n,n1)
            rs.fine = conf.fine * (n+1) + conf.hike*(n*(n+1))/2
            st.fine = st.fine + rs.fine
        messages.info(request, f"There is a fine: {rs.fine}")
        messages.info(request, f"Total fine: {st.fine}")
        bk.copies = bk.copies + 1
        st.save()
        bk.save()
        rs.delete()
        messages.info(request, "Book Returned")
        return redirect('return_book')
    return render(request, 'librariantemp/return_book.html', {'roll':roll, 'isbn':isbn})

@user_passes_test(lib_check, login_url="login_view")
def cust_books(request, id):
    cust = Customer.objects.get(id = id)
    data1 = Reserve.objects.filter(user = cust.user, status = "ISSUED")
    data2 = Reserve.objects.filter(user = cust.user, status = "RESERVED")
    return render(request, 'librariantemp/cust_books.html', {'data1':data1, 'data2':data2})

@user_passes_test(lib_check, login_url="login_view")
def pay_fine(request, id):
    cust = Customer.objects.get(id = id)
    pay = IntForm()
    if request.method == 'POST':
        cust.fine = cust.fine - int(request.POST['pay'])
        cust.save()
        messages.info(request, "Amount Received")
        return redirect('customer_view')
    return render(request, 'librariantemp/pay_fine.html',{'fine':cust.fine})

@user_passes_test(lib_check, login_url="login_view")
def lib_msg_sent(request):
    msg = Message.objects.filter(sender = request.user)
    return render(request, 'librariantemp/lib_msg_sent.html', {'msg':msg})

@user_passes_test(lib_check, login_url="login_view")
def lib_msg_recv(request):
    msg = Message.objects.filter(receiver = request.user)
    return render(request, 'librariantemp/lib_msg_recv.html', {'msg':msg})

@user_passes_test(lib_check, login_url="login_view")
def lib_msg(request):
        form = MessageForm()
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                msg = Message.objects.createMessage.objects.create(sender = request.user, receiver = Login.objects.get(id = form['receiver'].value()), contact = form['contact'].value(), message = form['message'].value(), time = datetime.datetime.now())
            return redirect('lib_msg_sent')
        return render(request, 'librariantemp/lib_msg.html', {'form':form})

@user_passes_test(lib_check, login_url="login_view")
def del_lib_sent(request, id):
    msg = Message.objects.get(id = id)
    if request.method == 'POST':
        msg.delete()
    return redirect('librariantemp/lib_msg_sent')

@user_passes_test(lib_check, login_url="login_view")
def del_lib_sent(request, id):
    msg = Message.objects.get(id = id)
    msg.delete()
    return redirect('lib_msg_sent')

###########################CUSTOMER SIDE###########################

def cust_check(user):
    return user.is_customer

@user_passes_test(cust_check, login_url="login_view")
def customer_dash(request):
    return render(request, 'customertemp/dashboard.html')

@user_passes_test(cust_check, login_url="login_view")
def books_view(request):
    genres = Genre.objects.all()
    langs = Language.objects.all()
    genreID = request.GET.get('genre')
    langID = request.GET.get('lang')
    if genreID:
        book = Book.objects.filter(genre = genreID)
    elif langID:
        book = Book.objects.filter(lang = langID)
    elif genreID and langID:
        book = Book.objects.filter(genre = genreID, lang = langID)
    else:
        book = Book.objects.all()
    itemFilter = BookFilter(request.GET, queryset = book)
    data = itemFilter.qs
    return render(request, 'customertemp/view_book.html', {'data':data, 'genres':genres, 'langs':langs, 'itemFilter':itemFilter})

@user_passes_test(cust_check, login_url="login_view")
def cust_profile(request):
    u = request.user
    data = Customer.objects.get(user = u)
    return render(request, 'customertemp/profile.html', {'data':data})

@user_passes_test(cust_check, login_url="login_view")
def issued_books(request):
    data1 = Reserve.objects.filter(user = request.user, status = "ISSUED")
    data2 = Reserve.objects.filter(user = request.user, status = "RESERVED")
    return render(request, 'customertemp/issued_books.html', {'data1':data1, 'data2':data2})

@user_passes_test(cust_check, login_url="login_view")
def reserve_book(request,id):
    bk = Book.objects.get(id = id)
    cop = bk.copies
    if cop == 0:
        avail = False
    else:
        avail = True
    if request.method == 'POST':
        conf = Configure.objects.last()
        if Reserve.objects.filter(user = request.user, book = bk):
            messages.info(request, f"Book Already {Reserve.objects.filter(user = request.user, book = bk).status}")
            return redirect('return_book')
        rs = Reserve.objects.create(user = request.user, book = bk, valid_till = datetime.date.today() + datetime.timedelta(days = conf.reserve_till), status ="RESERVED")
        bk.copies = cop - 1
        bk.save()
        messages.info(request, "Book Reserved")
        return redirect('books_view')
    return render(request, 'customertemp/reserve.html', {'book':bk, 'avail':avail})

@user_passes_test(cust_check, login_url="login_view")
def genre_search(request, id):
    genre = Genre.objects.get(id = id)
    data = Book.objects.filter(genre = genre)
    return render(request, 'customertemp/view_book.html', {'data':data})
    
@user_passes_test(cust_check, login_url="login_view")
def cust_msg_sent(request):
    msg = Message.objects.filter(sender = request.user)
    return render(request, 'customertemp/cust_msg_sent.html', {'msg':msg})

@user_passes_test(cust_check, login_url="login_view")
def cust_msg_recv(request):
    msg = Message.objects.filter(receiver = request.user)
    return render(request, 'customertemp/cust_msg_recv.html', {'msg':msg})

@user_passes_test(cust_check, login_url="login_view")
def cust_msg(request):
        form = MessageForm()
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                msg = Message.objects.create(sender = request.user, receiver = Login.objects.get(id = form['receiver'].value()), contact = form['contact'].value(), message = form['message'].value(), time = datetime.datetime.now())
            return redirect('cust_msg_sent')
        return render(request, 'customertemp/cust_msg.html', {'form':form})

@user_passes_test(cust_check, login_url="login_view")
def del_cust_sent(request, id):
    msg = Message.objects.get(id = id)
    if request.method == 'POST':
        msg.delete()
    return redirect('customertemp/cust_msg_sent')

@user_passes_test(cust_check, login_url="login_view")
def del_cust_sent(request, id):
    msg = Message.objects.get(id = id)
    msg.delete()
    return redirect('cust_msg_sent')

################################################







