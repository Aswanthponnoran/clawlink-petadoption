from django.shortcuts import render,redirect
from shop.models import Category,Product


# Create your views here.
def index(request):
    return render(request,'index.html')

def base(request):
    return render(request,'base.html')

def category(request):
    c=Category.objects.all()
    context={'cat':c}
    print(context)
    return render(request,'category.html',context)


def product(request,prodtid):
    print(prodtid)
    c=Category.objects.get(id=prodtid)
    p=Product.objects.filter(category=c)
    context={'cat':c,'pro':p}
    return render(request,'product.html',context)

def productdetail(request,prodetilid):
    p=Product.objects.get(id=prodetilid)
    print(prodetilid)
    context={'pro':p}
    return render(request,'details.html',context)


from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']
        if (p == cp):
            u = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
            u.save()
        else:
                return HttpResponse("Password should be same")
        return redirect('shop:category')
    return render(request, 'register.html')

# Request
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
def user_login(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']

        User = authenticate(username=u,password=p)  # checks weather the details entered by the user is correct or not
        if User:  # if user already exist
                login(request, User)
                return redirect('shop:category')
        else:  # If user does not exist
                return HttpResponse('Invalid')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('shop:login')



def addcategories(request):
    if(request.method=="POST"):
        n=request.POST['n']
        i=request.FILES['i']
        d=request.POST['d']
        c=Category.objects.create(name=n,image=i,desc=d)
        c.save()
        return redirect('shop:category')
    return render(request,'addcategories.html')

def addproducts(request):
    if(request.method == "POST"):
        n=request.POST['n']
        i=request.FILES['f']
        d=request.POST['d']
        s=request.POST['s']
        p=request.POST['p']
        c=request.POST['c']
        print(c)
        cat=Category.objects.get(name=c)#Retrives category record matching with the name
        p=Product.objects.create( name=n,desc=d,image=i,price=p,stock=s,category=cat)
        p.save()
        return redirect('shop:category')
    return render(request,'addproducts.html')



def addstock(request,adstkid):
    p=Product.objects.get(id=adstkid)
    if request.method=="POST":
      p.stock=request.POST['s']
      p.save()

      return redirect('shop:detail',adstkid)
    context = {'pro': p}

    return render(request,'addstock.html',context)