from django.shortcuts import render,redirect
from razorpay import Order

from cart.models import Cart
from shop.models import Product
from cart.models import Cart
from cart.models import Payment,Order_details

import razorpay

# Create your views here.
def addtocarts(request,addcarts):
    print(addcarts)
    p=Product.objects.get(id=addcarts)
    u=request.user
    try:
       c=Cart.objects.get(user=u,product=p)
       c.quantity+=1
       p.stock-=1
       p.save()
       c.save()
    except:
       c=Cart.objects.create(product=p,user=u,quantity=1)
       p.stock-=1
       p.save()
       c.save()
    return redirect('cart:cartview')

def cart_view(request):
    u=request.user
    c=Cart.objects.filter(user=u) #To filter cart records for a particular user
    total=0
    for i in c:
        total+=i.quantity*i.product.price
    context={'cart':c,'total':total}
    return render(request,'addtocarts.html',context)


def cart_remove(request,m):
    u=request.user
    p=Product.objects.get(id=m)
    try:
      c=Cart.objects.get(user=u,product=p)
      if c.quantity>1:
         c.quantity-=1
         c.save()
         p.stock+=1
         p.save()
      else:
         c.delete()
         p.stock+=1
         p.save()
    except:
        pass
    return redirect('cart:cartview')

def cart_delete(request,m):
    u=request.user
    p=Product.objects.get(id=m)
    try:
       c=Cart.objects.get(user=u,product=p)
       c.delete()
       p.stock += c.quantity
       p.save()
    except:
        pass
    return redirect('cart:cartview')


def orderform(request):
    if request.method=="POST":
        a=request.POST['a']
        pn=request.POST['pn']
        n=request.POST['n']

        #For calculating total bill amount
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.product.price*i.quantity
        print(total)

        #Razorpay connection
        client=razorpay.Client(auth=('rzp_test_dvLzMuNyFnkHZt','PNDD9opDBnUnwGEX1nkoSM1U'))

        #Razorpay order creation
        response_payment=client.order.create(dict(amount=total*100,currency='INR'))
        order_id=response_payment['id'] #Retrive the order id from response
        status=response_payment['status'] #Retrive the status  from response
        if status==("created"):
            p=Payment.objects.create(name=u.username,amount=total+100,order_id=order_id)
            # context={'payment':response_payment,'name':u.username}#Sends the response from view to payment.html
            p.save()

            for i in c:
                o=Order_details.objects.create(product=i.product,user=i.user,phone=pn,address=a,pin=n,order_id=order_id,no_of_items=i.quantity)
                o.save()
            context={'payment':response_payment,'name':u.username}#Sends the response from view to payment.html

            print(response_payment)
            return render(request,"payment.html",context)
    return render(request,"orderform.html")


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login



def orderview(request):
    u=request.user
    o=Order_details.objects.filter(user=u,payment_status="completed")
    context={'orders':o}
    return render(request,'orderview.html',context)


@csrf_exempt
def payment_status(request,p):
    user=User.objects.get(username=p)#Retrives user object
    login(request,user)

    response=request.POST
    print(response)

    #To check the validity of razorpay payment details received from Razorpay
    parm_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    client = razorpay.Client(auth=('rzp_test_dvLzMuNyFnkHZt', 'PNDD9opDBnUnwGEX1nkoSM1U'))
    try:
        status=client.utility.verify_payment_signature(parm_dict) #checking the payment details
        print(status)
        p=Payment.objects.get(order_id=response['razorpay_order_id'])
        p.razorpay_payment_id=response['razorpay_payment_id'],
        p.paid=True
        p.save()

        o=Order_details.objects.filter(order_id=response['razorpay_order_id'])
        for i in o:
            i.payment_status="completed"
            i.save()

        #To remove Cart items for a particular user after successful payment
        c=Cart.objects.filter(user=user)
        c.delete()
    except:
        pass
    return render(request,'payment-status.html')
