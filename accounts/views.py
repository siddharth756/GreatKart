from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from carts.models import Cart, CartItem
from carts.views import _cart_id

#verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import requests

# ------------------ register --------------

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username, password=password)
            user.phone_number = phone_number        
            user.save()
            
            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_varification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request,'Successed, Please check your email to activate account.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()       
            
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


# ------------ login -----------------

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    
                    #getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    #get the cart item from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_list = []
                    item_id = []
        
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_list.append(list(existing_variation)) 
                        item_id.append(item.id)  
                    
                    
                    # get common product in product variation and ex_list and then increasing quantity
                    for pr in product_variation:
                        if pr in ex_list:
                            index = ex_list.index(pr)
                            it_id = item_id[index]
                            item = CartItem.objects.get(id=it_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            
            auth_login(request, user)
            messages.success(request, "You are now logged in.")
            url = request.META.get('HTTP_REFERER')
            try:
                # Query -->  next=/cart/checkout/
                query = requests.utils.urlparse(url).query
                #getting dict like {'next': '/cart/checkout/'}
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)

            except:
                return redirect("accounts:dashboard")
            
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('accounts:login')
        
    return render(request, 'accounts/login.html')


# ------------- logout ---------------

@login_required(login_url='accounts:login')
def user_logout(request):
    auth_logout(request)
    messages.success(request, "Your are logged out.")
    return redirect('accounts:login')


# ------------ (activate account email) -------------

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist): 
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your Account is activated.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('accounts:register')
    
    
# ----------------- dashboard ------------
    
@login_required(login_url='accounts:login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
      
      
# ------------------ Forgot Password ------------------
        
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('accounts:login')
        
        else:
            messages.error(request, 'Account doesn\'t exist.')
            return redirect('accounts:forgotPassword')
            
    return render(request, 'accounts/forgotPassword.html')


# ------------ (reset password validate email) -------------

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist): 
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Password.')
        return redirect('accounts:resetPassword')
    else:
        messages.error(request, 'This link has been expired!.')
        return redirect('accounts:login')
    
def resetPassword(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if new_password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('accounts:login')
        
        else:
            messages.error(request, 'Password doesn\'t match.')
            return redirect('accounts:resetPassword')
        
    else:
        return render(request,'accounts/resetPassword.html')