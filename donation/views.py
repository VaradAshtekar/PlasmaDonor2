from django.shortcuts import render, redirect, HttpResponse
from math import ceil
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Contact, Donor, Centers

from bs4 import BeautifulSoup
import requests
import time
#

# ekosh = requests.get('https://www.eraktkosh.in/BLDAHIMS/bloodbank/nearbyBBRed.cnt').text
# center = soup.find_all('tr',class_ = "odd")
# print(center)


html_text = requests.get('https://mahasbtc.org/sbtc/blood-bank-data/').text
soup = BeautifulSoup(html_text, 'lxml')
city_name = soup.find_all('option')

bankname = soup.find_all('td', style='color: #404040; font-size: 14px; padding: 3px 15px;', width='30%')
names_of_banks = []
for centers in enumerate(bankname):
    names_of_banks.append(centers[1].text)
bankaddress = soup.find_all('td', style="color: #404040; font-size: 14px; padding: 3px 15px;", width="50%")
address_of_bank = []
for i in enumerate(bankaddress):
    address_of_bank.append(i[1].text)

for i in range(0, len(names_of_banks)):
    full_center_field = Centers(center_name = names_of_banks[i], address = address_of_bank[i])
    full_center_field.save()

# print(full_center_field)
# for j in names_of_banks:
#     trans_centers = Centers(center_name = j)
#     trans_centers.save()




def index(request):
    return render(request, 'donation/index.html')

def faqs(request):
    return render(request, 'donation/faq.html')

def signupsys(request):
    s_stat = "Register here!!"
    color = "dark"
    if request.method == "POST":

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = firstname + " " + lastname
        phoneno = request.POST.get('phone')
        address = request.POST.get('address')
        bloodgroup = request.POST.get('bloodgroup')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        print(bloodgroup)
        s_stat = "Register here!"

        if password == password2 and len(password) >= 8:
            finalpassword = password
            user = User.objects.create_user(username, email, finalpassword)
            print(user)
            user.phone_number = phoneno
            user.personal_address = address
            user.blood_grp = bloodgroup
            user.save()
            s_stat = "Registration successful!!"
            color = "success"
        elif len(password) < 8:
            s_stat = "Password must be equal to or greater than 8 characters!!"
            color = "danger"
        else:
            s_stat = "Sorry! failed to register! check your passwords once again..."
            color = "danger"

    return render(request, 'donation/register.html', context={"s_stat": s_stat, "color":color })

def compatability(request):
    return render(request, 'donation/compatability.html')

def location(request):


    cities = []
    for i in city_name[2:]:
        cities.append(i.text)
    banks = Centers.objects.values('center_name')
    addressofbank = Centers.objects.values('address')
    names_of_banks = []
    address_of_bank = []
    city_query = request.GET.get('city')
    print(city_query)
    if city_query != None:
        for items in addressofbank:
            if city_query in items['address']:
                address_of_blood_bank = Centers.objects.filter(name__icontains=city_query)
                names_of_banks = [item.center_name for item in address_of_blood_bank]
                address_of_bank = [item.address for item in address_of_blood_bank]
                print(names_of_banks)
            else:
                break


    query = request.GET.get('search')
    if query != None:
        for items in banks:
            if query.lower() == items['center_name'].lower():
                names_of_banks = Centers.objects.filter(center_name=items['center_name']).values_list('center_name', flat=True)

            else:
                names_of_banks = []
                for i in banks:
                    names_of_banks.append(i['center_name'])
                for i in addressofbank:
                    address_of_bank.append(i['address'])
    else:
        for i in banks:
            names_of_banks.append(i['center_name'])
        for i in addressofbank:
            address_of_bank.append(i['address'])


    bank_info = []
    for i in range(0,len(names_of_banks)):
        number = []
        number.append(i+1)
        bank_info.append([names_of_banks[i], address_of_bank[i], number[0]])



    params = {'city': cities, 'bank_info' : bank_info}
    return render(request, 'donation/location.html', params)


def contact(request):
    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contactform = Contact(name=name , email=email, phone=phone, desc=desc)
        contactform.save()
    return render(request, 'donation/contact.html')



def loginsystem(request):
    if request.method == "POST":
        loginusername = request.POST.get('emaillog')
        loginpassword = request.POST.get('password')
        user = authenticate(request, username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            msg = "Successfully logged in!!"
            return redirect("donation:index")
        else:
            msg = "Failed to log in!! please enter right password/ username!!"

        return render(request, 'donation/login.html', context={"msg": msg})

    return render(request, 'donation/login.html')

def donor(request):
    city_name = soup.find_all('option')
    cities = []
    for i in city_name[2:]:
        cities.append(i.text)
    bankname = soup.find_all('td', style='color: #404040; font-size: 14px; padding: 3px 15px;', width='30%')
    names_of_banks = []
    for centers in enumerate(bankname):
        names_of_banks.append(centers[1].text)

    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        userr = User.objects.get(username = request.user)

        if request.method == "POST":

            donor_name = request.POST.get('name')
            donor_gender = request.POST.get('gender')
            donor_address = request.POST.get('address')
            donor_city = request.POST.get('city')
            donor_bloodbank = request.POST.get('bloodbank')
            donor_bloodgroup = request.POST.get('bloodgroup')
            covid_recovery_date = request.POST.get('recovery')
            donor_form = Donor(user_name=donor_name, gender = donor_gender, address = donor_address, city = donor_city, bank_name = donor_bloodbank, blood_grp = donor_bloodgroup, registration_date = datetime.datetime.now(), covid_recovery_date = covid_recovery_date)
            donor_form.save()
            print(donor_form.covid_recovery_date)
        params = {'username':userr, 'city': cities, 'names_of_banks' : names_of_banks}
    return render(request, 'donation/donate.html',params )
