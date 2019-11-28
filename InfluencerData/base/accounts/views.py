from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserCreationForm, UserLoginForm, editpro
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import business_profile_dataSerializers
from django.shortcuts import get_object_or_404
from .models import *
import requests
import base64
from datetime import datetime
from requests_oauthlib import OAuth1
import requests
User = get_user_model()





def register(request, *args, **kwargs):
    userme = request.user
    if userme.is_authenticated:
        return HttpResponseRedirect("/")
    else:
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, "accounts/register.html", context)


def login_view(request, *args, **kwargs):
    userme = request.user
    if userme.is_authenticated:
        return HttpResponseRedirect("/profile")
    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            return HttpResponseRedirect("/profile")
        return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def check_bizz(name, user__name):
    if business_profile_data.objects.filter(username=user__name):
        return True
    else:
        data = business_profile_data()
        data.username = user__name
        data.first_name = ''
        data.company_category = ''
        data.website = ''
        data.email = name
        data.number = '0'
        data.founded = '1996-12-26'
        data.field_of_interest = ''
        data.overview = ''
        data.location = ''
        data.address = ''
        data.company_size = '0'
        data.save()
        print('user created')
        return True


def check_creator(name, user__name):
    if creator_profile_data.objects.filter(username=user__name):
        return True
    else:
        data = creator_profile_data()
        data.username = user__name
        data.skills = ''
        data.artist_category = ''
        data.website = ''
        data.email = name
        data.number = '0'
        data.description = ''
        data.location = ''
        data.address = ''
        data.gender = ''
        data.save()
        print('user created')
        return True


def profile(request):
    userme = request.user
    user_name_ = request.user.username
    if userme.is_authenticated:
        if request.user.category == 'Creator':

            try:
                connected = SocialAccount.objects.filter(user=request.user.id)
                selected = selected_connections.objects.filter(username= MyUser.objects.get(id = request.user.id))
            except:
                selected = ''

            user_obj = User.objects.get(id = request.user.id)
            print('selected :: ',selected)
            return render(request, 'accounts/creator.html', {'user_obj':user_obj,'selected':selected,'connected':connected})
        elif request.user.category == 'Business':

            user_obj = User.objects.get(id = request.user.id)
            return render(request, 'accounts/business.html', {'user_obj':user_obj,})
        else:
            # print('choose category')
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

@login_required(login_url='/')
def change_password(request):
    userme = request.user
    if userme.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, form.user)
                return redirect('/profile/')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {
            'form': form
        })
    else:
        return HttpResponseRedirect("/")

@login_required(login_url='/')
def edit_profile(request):
    userme = request.user
    if userme.is_authenticated:
        if request.method == 'POST':
            form = editpro(request.POST or None, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/profile')
        else:
            form = editpro(instance=request.user)
            context = {'form': form}
            return render(request, 'accounts/edit_profile.html', context)

    else:
        return HttpResponseRedirect("/")


def edit_business(request):
    userme = request.user
    if userme.is_authenticated:
        cat = request.user.category
        if cat == 'Business':
            if request.method == 'POST':
                poll = business_profile_data.objects.get(username=request.user.username)
                form = busi_data(request.POST or None, instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
            else:
                poll = business_profile_data.objects.get(username=request.user.username)
                form = busi_data(instance=poll)
                context = {'form': form}
                return render(request, 'accounts/business_edit.html', context)
    else:
        return HttpResponseRedirect("/")


def edit_creator(request):
    userme = request.user
    if userme.is_authenticated:
        cat = request.user.category
        if cat == 'Creator':
            if request.method == 'POST':
                poll = creator_profile_data.objects.get(username=request.user.username)
                form = creator_data(request.POST or None, instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
            else:
                poll = creator_profile_data.objects.get(username=request.user.username)
                form = creator_data(instance=poll)
                context = {'form': form}
                return render(request, 'accounts/creator_edit.html', context)
        else:
            HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def edit_me(request):
    userme = request.user
    if userme.is_authenticated:

        cat = MyUser.objects.get(id = request.user.id).category
        print(cat)
        if cat == 'Creator':

            if request.method == 'POST':
                print('POST is is')
                poll = creator_profile_data.objects.get(username=MyUser.objects.get(id = request.user.id))
                form = creator_data(request.POST, instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
                else:
                    return HttpResponse('error')
            else:
                poll = creator_profile_data.objects.get(username=MyUser.objects.get(id = request.user.id))
                form = creator_data(instance=poll)
                context = {'form': form}
                return render(request, 'accounts/creator_edit.html', context)
        elif cat == 'Business':
            if request.method == 'POST':
                poll = business_profile_data.objects.get(username=request.user)
                form = busi_data(request.POST or None, instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
                else:
                    return HttpResponse('error')
            else:
                poll = business_profile_data.objects.get(username=request.user)
                form = busi_data(instance=poll)
                context = {'form': form}
                return render(request, 'accounts/business_edit.html', context)

        else:
            return HttpResponseRedirect("/")

    else:
        return HttpResponseRedirect("/")

@login_required(login_url='/')
def connect(request):
    lmao = SocialAccount.objects.filter(user=request.user.id)
    data = user_connection_data.objects.get(username=request.user.id)
    connection_count = SocialAccount.objects.filter(user=request.user.id).count()
    selection_count = selected_connections.objects.filter(username=request.user.id).count()
    return render(request, 'accounts/lol.html', {'lmao': lmao, 'data': data, })

@login_required(login_url='/')
def profile_user(request,username):
    obj = get_object_or_404(MyUser, username = username)
    alertwork = ''
    alertcollab = ''
    samesender = ""
    if obj.category == 'Creator':
        data = creator_profile_data.objects.get(username = obj)
    elif obj.category == 'Business':
        data = business_profile_data.objects.get(username = obj)
    else:
        pass

    platforms = selected_connections.objects.filter(username = obj)

    count = 0
    facebook_count = 0
    twitter_count = 0
    linkedin_count = 0
    youtube_count = 0

    for x in platforms:
       if x.provider == 'facebook':
           try:
               new_ = facebook_data.objects.get(account = x)
               count = new_.fan_count + count
               facebook_count = facebook_count+ new_.fan_count
           except:
               pass
       elif x.provider == 'google':
           try:
               new_ = youtube_data.objects.get(account=x)
               count = new_.fan_count + count
               youtube_count = youtube_count + new_.fan_count
           except:
               pass
       elif x.provider == 'twitter':
           try:
               new_ = twitter_data.objects.get(account=x)
               count = new_.fan_count + count
               twitter_count = twitter_count + new_.fan_count
           except:
               pass
       elif x.provider == 'linkedin':
           try:
               new_ = linkedin_data.objects.get(account=x)
               count = new_.fan_count + count
               linkedin_count = linkedin_count + new_.fan_count
           except:
               pass
       else:
           pass


    if request.method == 'POST':
        if 'work' in request.POST:
            from datetime import datetime
            new_obj = notifications()
            new_obj.username = MyUser.objects.get(username = username)
            new_obj.sender = MyUser.objects.get(id = request.user.id).username
            new_obj.message = 'Hey! '+username+', i would like to work with you. Head over to my profile to contact me. Thanks '+new_obj.sender
            new_obj.sender_url = 'https://localhost:8000/'+new_obj.sender+'/'
            new_obj.notification_type = 100
            new_obj.datetime = datetime.now()
            if new_obj.sender == username:
                samesender = "Can't send yourself request!"
            else:
                new_obj.save()
                alertwork = 'Request Sent Successfully!'


        elif 'collab' in request.POST:
            from datetime import datetime
            new_obj = notifications()
            new_obj.username = MyUser.objects.get(username=username)
            new_obj.sender = MyUser.objects.get(id=request.user.id).username
            new_obj.message = 'Hey! ' + username + ', i would like to collab with you. Head over to my profile to contact me. Thanks ' + new_obj.sender
            new_obj.sender_url = 'https://localhost:8000/' + new_obj.sender + '/'
            new_obj.notification_type = 200
            new_obj.datetime = datetime.now()
            if new_obj.sender == username:
                samesender = "Can't send yourself request!"
            else:
                new_obj.save()
                alertcollab = 'Request Sent Successfully!'
        else:
            pass


    return render(request, 'accounts/profile_page.html', {'obj':obj,'data':data,'platforms':platforms,'count':count,
                                                           'facebook_count':facebook_count,'twitter_count':twitter_count,
                                                          'linkedin_count':linkedin_count, 'youtube_count':youtube_count,
                                                          'alertwork':alertwork,'alertcollab':alertcollab,'samesender':samesender})

@login_required(login_url='/')
def see_notifications(request):
    all = notifications.objects.filter(username = MyUser.objects.get(id = request.user.id),mark_as_read_all=False, read=False).order_by('-datetime')[:15]
    unread = notifications.objects.filter(username = MyUser.objects.get(id = request.user.id),mark_as_read_all=False, read=False)
    work = notifications.objects.filter(username = MyUser.objects.get(id = request.user.id), notification_type =100, read=False)
    collab = notifications.objects.filter(username=MyUser.objects.get(id=request.user.id), notification_type=200, read=False)

    if request.method == 'POST':
        if 'allread' in request.POST:
            print('all read')
            for x in unread:
                x.mark_as_read_all = True
                x.read = True
                x.read_datetime = datetime.now()
                x.save()
            return  redirect('/notifications')


        if 'markread' in request.POST:
            print('one read')
            new_obj = notifications.objects.get(username=MyUser.objects.get(id=request.user.id), id = request.POST['markread'])
            new_obj.read = True
            new_obj.read_datetime = datetime.now()
            new_obj.save()
    return render(request, 'accounts/notifications.html',{'work':work,'collab':collab,'all':all})


def long_live_facebook(existing_token):
    import facebook
    lol = existing_token
    graph = facebook.GraphAPI(lol)
    app_id = '1990551177704465'
    app_secret = '38942534de2eeb787551d1cf9d1d0dac'
    extended_token = graph.extend_access_token(app_id, app_secret)
    final = extended_token['access_token']
    return final

@login_required(login_url='/')
def facebookconfigure(requset):
    return HttpResponse('nothing here!')



@login_required(login_url='/')
def configure(request):
    account = []
    error_connected = ''
    pack_error = ''
    obj = SocialAccount.objects.filter(user=request.user.id)
    for x in range(len(obj)):
        account.append(obj[x])

    data = user_connection_data.objects.get(username=request.user.id)

    selected = selected_connections.objects.filter(dirtybit=request.user.dirtybit, selected=True)
    not_selected = selected_connections.objects.filter(dirtybit=request.user.dirtybit, selected=False)
    import requests
    if 'facebook' in request.POST:
        print(request.POST['facebook'])
        object = request.POST['facebook']
        facetoken = get_object_or_404(SocialToken, id=request.POST['facebook'])
        all_account = get_object_or_404(SocialAccount, user=request.user, id=request.POST['facebook'])
        obj1 = requests.get("https://graph.facebook.com/me?fields=accounts&access_token=" + str(facetoken))
        par = obj1.json()
        accs = par['accounts']['data']
        print('going to configure page')

        return render(request, 'accounts/page-configrue.html', {'accs': accs, 'object': object})


    elif 'facebook-model' in request.POST:
        obj = request.POST['facebook-model'].split(',,,,,')
        if not selected_connections.objects.filter(account_uid=obj[0]):
            print(obj[0])
            print(obj[1])
            print(obj[2])
            print(obj[3])
            print('selecting facebook page')

            obj_create = selected_connections()
            obj_create.username = MyUser.objects.get(id=request.user.id)
            obj_create.dirtybit = request.user.dirtybit
            obj_create.provider = 'facebook'
            obj_create.account_token = SocialToken.objects.get(id=obj[3])
            obj_create.access_token = obj[1]
            obj_create.long_token = long_live_facebook(obj[1])
            obj_create.extra_data = SocialAccount.objects.get(user=request.user.id, id=obj[3]).extra_data
            obj_create.access_expiry = SocialToken.objects.get(id=obj[3]).expires_at
            obj_create.account_name = obj[2]
            obj_create.account_uid = obj[0]
            obj_create.selected = True
            obj_create.save()

            data.total_seleceted_connections += 1
            data.save()
            init_noti(obj_create.username, 300)
        else:
            error_connected = 'Account Already Connected !'
            pass


    elif 'google' in request.POST:

        if SocialAccount.objects.filter(user=request.user.id, id=request.POST['google']).exists():
            if not selected_connections.objects.filter(
                    account_uid=SocialAccount.objects.get(user=request.user.id, id=request.POST['google']).uid):
                obj_create = selected_connections()
                obj_create.username = MyUser.objects.get(id=request.user.id)
                obj_create.dirtybit = request.user.dirtybit
                obj_create.provider = 'google'
                obj_create.access_token = SocialToken.objects.get(id=request.POST['google']).token
                obj_create.extra_data = SocialAccount.objects.get(user=request.user.id,
                                                                  id=request.POST['google']).extra_data
                obj_create.access_expiry = SocialToken.objects.get(id=request.POST['google']).expires_at
                obj_create.account_name = SocialAccount.objects.get(user=request.user.id,
                                                                    id=request.POST['google']).extra_data['email']
                obj_create.account_uid = SocialAccount.objects.get(user=request.user.id,
                                                                   id=request.POST['google']).uid
                obj_create.selected = True
                obj_create.save()
                obj_create.save()


                data.total_seleceted_connections += 1
                data.save()


                # print(SocialAccount.objects.filter(user=request.user.id, id = request.POST['google']))
                # print(SocialToken.objects.get(id = request.POST['google']).account)
                # print(request.POST['google'])

            else:
                error_connected = 'Account Already Connected !'
                pass
        else:
            return redirect('/404')

    elif 'pinterest' in request.POST:

        if SocialAccount.objects.filter(user=request.user.id, id=request.POST['pinterest']).exists():
            if not selected_connections.objects.filter(
                    account_uid=SocialAccount.objects.get(user=request.user.id, id=request.POST['pinterest']).uid):

                obj_create = selected_connections()
                obj_create.username = MyUser.objects.get(id=request.user.id)
                obj_create.dirtybit = request.user.dirtybit
                obj_create.provider = 'pinterest'
                obj_create.account_token = SocialToken.objects.get(id=request.POST['pinterest'])
                obj_create.access_token = SocialToken.objects.get(id=request.POST['pinterest'])

                obj_create.access_token_secret = ''

                obj_create.extra_data = SocialAccount.objects.get(user=request.user.id,
                                                                  id=request.POST['pinterest']).extra_data

                obj_create.account_name = SocialAccount.objects.get(user=request.user.id,
                                                                    id=request.POST['pinterest']).extra_data['first_name']

                obj_create.account_uid = SocialAccount.objects.get(user=request.user.id,
                                                                   id=request.POST['pinterest']).uid
                obj_create.selected = True
                obj_create.save()

                data.total_seleceted_connections += 1
                data.save()


            else:
                error_connected = 'Account Already Connected !'
                pass

    elif 'linkedin' in request.POST:
        import requests
        import json

        if SocialAccount.objects.filter(user=request.user.id, id=request.POST['linkedin']).exists():
            if not selected_connections.objects.filter(
                    account_uid=SocialAccount.objects.get(user=request.user.id, id=request.POST['linkedin']).uid):

                obj_create = selected_connections()
                obj_create.username = MyUser.objects.get(id=request.user.id)
                obj_create.dirtybit = request.user.dirtybit
                obj_create.provider = 'linkedin'
                obj_create.account_token = SocialToken.objects.get(id=request.POST['linkedin'])
                obj_create.access_token = SocialToken.objects.get(id=request.POST['linkedin'])

                obj_create.extra_data = SocialAccount.objects.get(user=request.user.id,
                                                                  id=request.POST['linkedin']).extra_data
                obj_create.access_expiry = SocialToken.objects.get(id=request.POST['linkedin']).expires_at


                url = "https://api.linkedin.com/v2/me"
                text = 'Bearer '+ str(obj_create.access_token)
                headers = {
                    'Authorization': text,
                }

                response = requests.request("GET", url, headers=headers)
                print(response.json())
                obj = response.json()
                obj_create.account_name = str(obj['firstName']['localized']['en_US']) +' '+ str(obj['lastName']['localized']['en_US'])

                # obj_create.account_name = SocialAccount.objects.get(user=request.user.id,
                #                                                     id=request.POST['linkedin']).extra_data[
                #                               'firstName']['localized']['en_US'] + ' ' + \
                #                           SocialAccount.objects.get(user=request.user.id,
                #                                                     id=request.POST['linkedin']).extra_data[
                #                               'lastName']['localized']['en_US']

                obj_create.account_uid = SocialAccount.objects.get(user=request.user.id,
                                                                   id=request.POST['linkedin']).uid
                obj_create.selected = True
                obj_create.save()
                # ---------------


                data.total_seleceted_connections += 1
                data.save()


                # print(SocialAccount.objects.filter(user=request.user.id, id = request.POST['twitter']))
                # print(SocialToken.objects.get(id = request.POST['twitter']).account)
                # print(request.POST['twitter'])

            else:
                error_connected = 'Account Already Connected !'
                pass

    elif 'twitter' in request.POST:

        if SocialAccount.objects.filter(user=request.user.id, id=request.POST['twitter']).exists():
            if not selected_connections.objects.filter(
                    account_uid=SocialAccount.objects.get(user=request.user.id, id=request.POST['twitter']).uid):

                obj_create = selected_connections()
                obj_create.username = MyUser.objects.get(id=request.user.id)
                obj_create.dirtybit = request.user.dirtybit
                obj_create.provider = 'twitter'
                obj_create.account_token = SocialToken.objects.get(id=request.POST['twitter'])
                obj_create.access_token = SocialToken.objects.get(id=request.POST['twitter'])

                obj_create.access_token_secret = SocialToken.objects.get(id=request.POST['twitter']).token_secret

                obj_create.extra_data = SocialAccount.objects.get(user=request.user.id,
                                                                  id=request.POST['twitter']).extra_data
                obj_create.access_expiry = SocialToken.objects.get(id=request.POST['twitter']).expires_at
                obj_create.account_name = SocialAccount.objects.get(user=request.user.id,
                                                                    id=request.POST['twitter']).extra_data['name']
                obj_create.account_uid = SocialAccount.objects.get(user=request.user.id,
                                                                   id=request.POST['twitter']).uid
                obj_create.selected = True
                obj_create.save()

                data.total_seleceted_connections += 1
                data.save()


            else:
                error_connected = 'Account Already Connected !'
                pass

    elif 'facebook-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['facebook-remove']).uid
        print('var is ',var)
        count_var1 = selected_connections.objects.filter(username=request.user.id, extra_data__icontains=var).count()
        print('related accounts :: ', count_var1)

        # var1 = selected_connections.objects.filter(username=request.user.id, extra_data__icontains=var).delete()
        try:
            print('tried deleting')
            var1 = selected_connections.objects.filter(username=request.user.id, extra_data__icontains=var)
            if var1:
                var1.delete()
                data.total_seleceted_connections -= count_var1
                data.save()
                print('deleted')
        except:
            pass

        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['facebook-remove']).delete()

        # data.total_seleceted_connections -= count_var1
        # data.save()


        return redirect('/configure')

    elif 'google-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['google-remove']).uid
        # var1 = selected_connections.objects.filter(username=request.user.id, extra_data__icontains=var).delete()
        try:
            var1 = selected_connections.objects.get(username=request.user.id, account_uid=var)
            if var1:
                var1.delete()
                data.total_seleceted_connections -= 1
                data.save()
        except:
            pass

        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['google-remove']).delete()
        # data.total_seleceted_connections -= 1
        # data.save()


        return redirect('/configure')

    elif 'twitter-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['twitter-remove']).uid
        try:
            var1 = selected_connections.objects.get(username=request.user.id, account_uid=var)
            if var1:
                var1.delete()
                data.total_seleceted_connections -= 1
                data.save()
        except:
            pass
        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['twitter-remove']).delete()
        # data.total_seleceted_connections -= 1
        # data.save()


        return redirect('/configure')

    elif 'pinterest-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['pinterest-remove']).uid
        # var1 = selected_connections.objects.filter(username=request.user.id, account_uid=var).delete()

        try:
            var1 = selected_connections.objects.get(username=request.user.id, account_uid=var)
            if var1:
                var1.delete()
                data.total_seleceted_connections -= 1
                data.save()
        except:
            pass

        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['pinterest-remove']).delete()
        # data.total_seleceted_connections -= 1
        # data.save()


        return redirect('/configure')

    elif 'linkedin-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['linkedin-remove']).uid
        # var1 = selected_connections.objects.filter(username=request.user.id, account_uid=var).delete()

        try:
            var1 = selected_connections.objects.get(username=request.user.id, account_uid=var)
            if var1:
                var1.delete()
                data.total_seleceted_connections -= 1
                data.save()
        except:
            pass


        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['linkedin-remove']).delete()



        return redirect('/configure')

    else:
        pass


    return render(request, 'accounts/configure.html', {'account': account, 'not_selected': not_selected,
                                                       'selected': selected, 'error_connected': error_connected,
                                                       'pack_error': pack_error, })




@login_required(login_url='/')
def insights(request):
    if request.user.is_authenticated:
        selected = selected_connections.objects.filter(username = MyUser.objects.get(id = request.user.id))
        allon = True

        for x in selected:
            if x.auto_sync == False:
                allon = False
                break
            else:
                allon = True


        if request.method == 'POST':
            if 'all-off' in request.POST:
                selected = selected_connections.objects.filter(username=MyUser.objects.get(id=request.user.id))
                for x in selected:
                    x.auto_sync = False
                    x.save()
                return redirect('/insights')

            if 'all-on' in request.POST:
                selected = selected_connections.objects.filter(username=MyUser.objects.get(id=request.user.id))
                for x in selected:
                    x.auto_sync = True
                    x.save()
                return redirect('/insights')

        return render(request, 'accounts/insights.html', {'selected':selected,'allon':allon})
    else:
        return redirect('/')



def fetch_facebook_data(user,uid):
    facebook_data.objects.get_or_create(
        username = MyUser.objects.get(id = user),
        account = selected_connections.objects.get(username = MyUser.objects.get(id= user), account_uid= uid)
    )
    obj = facebook_data.objects.get(username = MyUser.objects.get(id = user),
        account = selected_connections.objects.get(username = MyUser.objects.get(id= user), account_uid= uid))

    account_details = selected_connections.objects.get(username = MyUser.objects.get(id= user), account_uid= uid)

    data = requests.get("https://graph.facebook.com/v4.0/"+account_details.account_uid+"?fields=id%2Cabout%2Cname%2Cbio%2Cbusiness%2Ccategory%2Cfan_count%2Cfeatured_video%2Cartists_we_like%2Cconnected_instagram_account%2Ccover%2Ccountry_page_likes%2Cengagement%2Cimpressum%2Cinfluences%2Cnew_like_count%2Coverall_star_rating%2Cprice_range%2Crating_count%2Ctalking_about_count%2Cunread_message_count%2Cunread_notif_count%2Cunseen_message_count%2Cverification_status%2Cwebsite%2Cwere_here_count%2Cratings.limit(100)%7Brating%7D%2Clikes&access_token="+account_details.long_token)
    json_obj = data.json()

    obj.name = account_details.account_name

    try:
        obj.bio = json_obj['bio']
    except:
        pass
    
    obj.fb_id = json_obj['id']
    
    try:
        obj.business_name = json_obj['business_name']
    except:
        pass

    try:
        obj.featured_video_desc = json_obj['featured_video']['description']
    except:
        pass
    
    try:
        obj.artists_we_like = json_obj['artists_we_like']
    except:
        pass
    
    try:
        obj.connected_instagram_account = json_obj['connected_instagram_account']['id']
    except:
        pass
      
    try:
        obj.cover_source = json_obj['cover']['source']
    except:
        pass

    try:
        obj.about = json_obj['about']
    except:
        pass

    try:
        obj.impressum = json_obj['impressum']
    except:
        pass
    obj.category = json_obj['category']
    obj.fan_count = json_obj['fan_count']
    obj.country_page_likes = json_obj['country_page_likes']
    obj.engagement = json_obj['engagement']['count']
    obj.new_like_count = json_obj['new_like_count']
    obj.talking_about_count = json_obj['talking_about_count']
    obj.unread_message_count= json_obj['unread_message_count']
    obj.unread_notif_count= json_obj['unread_notif_count']
    obj.unseen_message_count= json_obj['unseen_message_count']
    obj.were_here_count= json_obj['were_here_count']
    obj.verification_status= json_obj['verification_status']

    try:
        obj.website = json_obj['website']
    except:
        pass

    try:
        obj.rating_count = json_obj['rating_count']
    except:
        pass

    try:
        obj.overall_star_rating = json_obj['overall_star_rating']
    except:
        pass

    obj.save()
    return data



def fetch_linkedin_data(user, uid):
    linkedin_data.objects.get_or_create(
        username=MyUser.objects.get(id=user),
        account=selected_connections.objects.get(username=MyUser.objects.get(id=user), account_uid=uid)
    )
    obj = linkedin_data.objects.get(username=MyUser.objects.get(id=user),
                                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user),
                                                                             account_uid=uid))

    account_details = selected_connections.objects.get(username=MyUser.objects.get(id=user), account_uid=uid)

    url = "https://api.linkedin.com/v2/me/"
    text = 'Bearer ' + str(account_details.access_token)
    headers = {
        'Authorization': text,
    }

    response = requests.request("GET", url, headers=headers)
    answer = response.json()
    print(answer)

    obj.name = account_details.account_name
    obj.linkedin_id = uid
    obj.name = str(answer['firstName']['localized']['en_US'])+' '+str(answer['lastName']['localized']['en_US'])
    obj.save()
    return True

def fetch_twitter_data(user,uid):
    twitter_data.objects.get_or_create(
        username=MyUser.objects.get(id=user),
        account=selected_connections.objects.get(username=MyUser.objects.get(id=user), account_uid=uid)
    )
    obj = twitter_data.objects.get(username=MyUser.objects.get(id=user),
                                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user),
                                                                             account_uid=uid))

    home = selected_connections.objects.get(username=user, account_uid=uid)
    TWITTER_CONSUMER_KEY = '1Vd9j6RGv01MeGpMhqbgGhP5l'
    TWITTER_CONSUMER_SECRET = 'XxXOZD0mwVrdEcKFkT2qsIlP7scJKIBhqBueH03sw01rEilQjJ'
    FETCH_TIMELINE = 'https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=' + home.account_uid + '&count=2'
    oauth = OAuth1(TWITTER_CONSUMER_KEY,
                   client_secret=TWITTER_CONSUMER_SECRET,
                   resource_owner_key=str(home.access_token),
                   resource_owner_secret=str(home.access_token_secret))
    req = requests.get(url=FETCH_TIMELINE, auth=oauth)
    json_data = req.json()

    obj.twitter_id = json_data[0]['user']['id']
    obj.name = json_data[0]['user']['name']
    obj.screen_name = json_data[0]['user']['screen_name']
    obj.location = json_data[0]['user']['location']
    obj.description = json_data[0]['user']['description']
    obj.website = json_data[0]['user']['entities']['url']['urls'][0]['display_url']
    obj.fan_count = json_data[0]['user']['followers_count']
    obj.friends_count = json_data[0]['user']['friends_count']
    obj.listed_count = json_data[0]['user']['listed_count']
    obj.created_at = json_data[0]['user']['created_at']
    obj.favourites_count = json_data[0]['user']['favourites_count']
    obj.verified = json_data[0]['user']['verified']
    obj.profile_background_color = json_data[0]['user']['profile_background_color']
    obj.profile_background_image_url_https = json_data[0]['user']['profile_background_image_url_https']
    obj.profile_image_url_https =  json_data[0]['user']['profile_image_url_https']
    obj.profile_banner_url = json_data[0]['user']['profile_banner_url']
    obj.save()
    return True

def check_insights(request,uid):
    if request.user.is_authenticated:
        user = MyUser.objects.get(id = request.user.id)
        user_id = MyUser.objects.get(id=request.user.id).id
        selected = get_object_or_404(selected_connections, username = user, account_uid = uid)
        isenabled = selected.auto_sync


        if selected.auto_sync == True:
            print('Fetching Data')
            selected.last_sync = datetime.now()
            selected.save()
            pro = selected.provider
            if pro == 'facebook':
                facebook_data.objects.get_or_create(
                    username=MyUser.objects.get(id=user_id),
                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user_id), account_uid=uid)
                )
                final_obj = facebook_data.objects.get(username=MyUser.objects.get(id=user_id),
                                                      account=selected_connections.objects.get(
                                                          username=MyUser.objects.get(id=user_id), account_uid=uid))

                fetch_facebook_data(user_id,uid)
            elif pro == 'linkedin':
                linkedin_data.objects.get_or_create(
                    username=MyUser.objects.get(id=user_id),
                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user_id), account_uid=uid)
                )
                final_obj = linkedin_data.objects.get(username=MyUser.objects.get(id=user_id),
                                                      account=selected_connections.objects.get(
                                                          username=MyUser.objects.get(id=user_id), account_uid=uid))

                fetch_linkedin_data(user_id, uid)

            elif pro == 'google':
                print('google')
                youtube_data.objects.get_or_create(
                    username=MyUser.objects.get(id=user_id),
                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user_id), account_uid=uid)
                )
                final_obj = youtube_data.objects.get(username=MyUser.objects.get(id=user_id),
                                                      account=selected_connections.objects.get(
                                                          username=MyUser.objects.get(id=user_id), account_uid=uid))


            elif pro == 'twitter':
                twitter_data.objects.get_or_create(
                    username=MyUser.objects.get(id=user_id),
                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user_id), account_uid=uid)
                )
                final_obj = twitter_data.objects.get(username=MyUser.objects.get(id=user_id),
                                                      account=selected_connections.objects.get(
                                                          username=MyUser.objects.get(id=user_id), account_uid=uid))


                fetch_twitter_data(user_id,uid)

            elif pro == 'instagram':
                print('instagram')
            elif pro == 'pinterest':
                print('pinterest')
            else:
                pass

        else:
            pro = selected.provider
            if pro == 'facebook':
                facebook_data.objects.get_or_create(
                    username=MyUser.objects.get(id=user_id),
                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user_id), account_uid=uid)
                )
                final_obj = facebook_data.objects.get(username=MyUser.objects.get(id=user_id),
                                                account=selected_connections.objects.get(
                                                    username=MyUser.objects.get(id=user_id), account_uid=uid))

            elif pro == 'linkedin':
                linkedin_data.objects.get_or_create(
                    username=MyUser.objects.get(id=user_id),
                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user_id), account_uid=uid)
                )
                final_obj = linkedin_data.objects.get(username=MyUser.objects.get(id=user_id),
                                                      account=selected_connections.objects.get(
                                                          username=MyUser.objects.get(id=user_id), account_uid=uid))


            elif pro == 'google':

                youtube_data.objects.get_or_create(
                    username=MyUser.objects.get(id=user_id),
                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user_id), account_uid=uid)
                )
                final_obj = youtube_data.objects.get(username=MyUser.objects.get(id=user_id),
                                                     account=selected_connections.objects.get(
                                                         username=MyUser.objects.get(id=user_id), account_uid=uid))
                form = youtube_data_form(instance = final_obj)

            elif pro == 'twitter':
                twitter_data.objects.get_or_create(
                    username=MyUser.objects.get(id=user_id),
                    account=selected_connections.objects.get(username=MyUser.objects.get(id=user_id), account_uid=uid)
                )
                final_obj = twitter_data.objects.get(username=MyUser.objects.get(id=user_id),
                                                     account=selected_connections.objects.get(
                                                         username=MyUser.objects.get(id=user_id), account_uid=uid))


            elif pro == 'instagram':
                print('instagram')
            elif pro == 'pinterest':
                print('pinterest')
            else:
                pass


        if request.method=='POST':
            if 'btn-sync-now' in request.POST:
                print(request.POST['btn-sync-now'])
                print('Fetching Data')
                selected.last_sync = datetime.now()
                selected.save()

                pro = selected.provider
                if pro == 'facebook':
                    fetch_facebook_data(user_id, uid)
                elif pro == 'linkedin':
                    fetch_linkedin_data(user_id, uid)
                elif pro == 'google':
                    print('google sync now ')
                elif pro == 'twitter':
                    fetch_twitter_data(user_id, uid)
                elif pro == 'instagram':
                    print('instagram')
                elif pro == 'pinterest':
                    print('pinterest')
                else:
                    pass



            elif 'btn-on' in request.POST:
                print('button On')
                print(request.POST['btn-on'])
                obj = selected_connections.objects.get( username = user, account_uid = uid)
                obj.auto_sync = True
                obj.last_sync = datetime.now()
                obj.save()
                return redirect('/check-insights/'+obj.account_uid)
            elif 'btn-off' in request.POST:
                print(request.POST['btn-off'])
                print('button OFF')
                obj = selected_connections.objects.get( username = user, account_uid = uid)
                obj.auto_sync = False
                obj.save()
                return redirect('/check-insights/'+obj.account_uid)
            elif 'submit_det' in request.POST:
                final_obj = youtube_data.objects.get(username=MyUser.objects.get(id=user_id),
                                                     account=selected_connections.objects.get(
                                                         username=MyUser.objects.get(id=user_id), account_uid=uid))

                form = youtube_data_form(request.POST, instance=final_obj)

                print('recieved')

                if form.is_valid():
                    print('valid form')
                    form.save()
            else:
                pass

        return render(request,'accounts/check-insights.html',{'selected':selected,'isenabled':isenabled,
                                                              'final_obj':final_obj,'form':form})
    else:
        return redirect('/')


@login_required(login_url='/')
def search(request):
    form = search_form()
    user = MyUser.objects.get(id = request.user.id)
    result = ''
    obj1 = []
    obj2 = []
    obj3 = []
    if request.method == 'POST':
        form = search_form(request.POST,)
        if form.is_valid():
            form = form.save(commit=False)
            form.username = user
            form.save()
            print('Location is ::',form.location)
            print('Platform is ::', form.platform)
            print('Category is ::', form.category)
            print('valid')
            obj1 = creator_profile_data.objects.filter(location__icontains = form.location).exclude(username = MyUser.objects.get(id = request.user.id))
            obj2 = []
            obj3 = []
            obj4 = []

            for x in obj1:
                if form.category in x.artist_category:
                    obj2.append(x)
                    print(x.username, 'have same category')
                    if selected_connections.objects.filter(username = x.id,provider = form.platform):
                        obj3.append(x)
                else:
                    pass

            for x in obj2: # same location and category
                print(x)

            for x in obj3: # same location and category and platform
                print(x.username)

            return render(request, 'accounts/search.html', {'form':form,'obj1':obj1,'obj2':obj2,'obj3':obj3,'platform':form.platform})



    return render(request, 'accounts/search.html', {'form':form,'obj1':obj1,'obj2':obj2,'obj3':obj3,})