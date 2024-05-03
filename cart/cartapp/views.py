from . import models
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User

message = ''
cartlist = []  #購買商品串列
customname = ''  #購買者姓名
customphone = ''  #購買者電話
customaddress = ''  #購買者地址
customemail = ''  #購買者電子郵件
paytype= ''
status_num = None

def index(request):
    global cartlist
    if 'cartlist' in request.session:  #若session中存在cartlist就讀出
        cartlist = request.session['cartlist']
    else:  #重新購物
        cartlist = []
    cartnum = len(cartlist)  #購買商品筆數
    productall = models.ProductModel.objects.all()  #取得資料庫所有商品
    return render(request, "index.html", locals())


def usr_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        try:
            login(request, user)
            return redirect("index")
        except:
            return redirect('login')
    elif not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        return HttpResponse('Login Failed')

# def usr_login(request):
#     # Session.objects.all().delete()
#     user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
#     if user is not None:
#         login(request, user)
#         # return HttpResponse('Login Successful')
#         return redirect('index')
#
#     else:
#         return HttpResponse('Login Failed')

def usr_logout(request):
    logout(request)
    # return HttpResponse('Logout Successful')
    return redirect('index')

def usr_register(request):

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            print('save')
            return redirect('login')  # 注册成功后重定向到登录页面
        else:
            print('form is not valid')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

def detail(request, productid=None):  #商品詳細頁面
    product = models.ProductModel.objects.get(id=productid)  #取得商品
    return render(request, "detail.html", locals())

def cart(request):  #顯示購物車
    global cartlist
    cartlist1 = cartlist  #以區域變數傳給模版
    total = 0
    for unit in cartlist:  #計算商品總金額
        total += int(unit[3])
    grandtotal = total + 100  #加入運費總額
    return render(request, "cart.html", locals())

def addtocart(request, ctype=None, productid=None):
    global cartlist
    if ctype == 'add':  #加入購物車
        product = models.ProductModel.objects.get(id=productid)
        flag = True  #設檢查旗標為True
        for unit in cartlist:  #逐筆檢查商品是否已存在
            if product.pname == unit[0]:  #商品已存在
                unit[2] = str(int(unit[2])+ 1)  #數量加1
                unit[3] = str(int(unit[3]) + product.pprice)  #計算價錢
                flag = False  #設檢查旗標為False
                break
        if flag:  #商品不存在
            temlist = []  #暫時串列
            temlist.append(product.pname)  #將商品資料加入暫時串列
            temlist.append(str(product.pprice))  #商品價格
            temlist.append('1')  #先暫訂數量為1
            temlist.append(str(product.pprice))  #總價
            cartlist.append(temlist)  #將暫時串列加入購物車
        # print(cartlist)
        request.session['cartlist'] = cartlist  #購物車寫入session
        return redirect('cart')
    elif ctype == 'update':  #更新購物車
        n = 0
        for unit in cartlist:
            unit[2] = request.POST.get('qty' + str(n), '1')  #取得數量
            unit[3] = str(int(unit[1]) * int(unit[2]))  #取得總價
            n += 1
        request.session['cartlist'] = cartlist
        return redirect('cart')
    elif ctype == 'empty':  #清空購物車
        cartlist = []  #設購物車為空串列
        request.session['cartlist'] = cartlist
        return redirect('index')
    elif ctype == 'remove':  #刪除購物車中商品
        del cartlist[int(productid)]  #從購物車串列中移除商品
        request.session['cartlist'] = cartlist
        return redirect('cart')

def cartorder(request):  #按我要結帳鈕
    global cartlist, message, customname, customphone, customaddress, customemail
    cartlist1 = cartlist
    total = 0
    for unit in cartlist:  #計算商品總金額
        total += int(unit[3])
    grandtotal = total + 100
    customname1 = customname  ##以區域變數傳給模版
    customphone1 = customphone
    customaddress1 = customaddress
    customemail1 = customemail
    message1 = message
    return render(request, "cartorder.html", locals())

def cartok(request):  #按確認購買鈕
    global cartlist, message, customname, customphone, customaddress, customemail, paytype, status_num
    if request.user.is_authenticated:
        user = request.user.id
        # 这里执行已登录用户的操作，例如创建订单并将user_id关联到订单
    else:
        user = None

    # try:
    #     success = request.GET.get('success')
    #     success = int(success)
    # except:
    #     success = 0

    total = 0
    for unit in cartlist:
        total += int(unit[3])
    grandtotal = total + 100
    message = ''
    #抓取name屬性的值


    if request.method == 'POST':
        customname = request.POST.get('CustomerName', '')
        customphone = request.POST.get('CustomerPhone', '')
        customaddress = request.POST.get('CustomerAddress', '')
        customemail = request.POST.get('CustomerEmail', '')
        paytype = request.POST.get('paytype', '')

    customname1 = customname

    user_id = User.objects.get(pk=user) if user else None


    if (customname == '' or customphone == '' or customaddress == '' or customemail == '') and status_num != 0:
        message = '姓名、電話、住址及電子郵件皆需輸入'

        return redirect('cartorder')
    elif paytype == 'Visa' and status_num != 0:
        print('tappay')

        # return render(request, "tappay_payment.html")
        return redirect('tappay_payment')
    else:

        unitorder = models.OrdersModel.objects.create(subtotal=total, shipping=100, grandtotal=grandtotal, customname=customname, customphone=customphone, customaddress=customaddress, customemail=customemail, paytype=paytype, user=user_id) #建立訂單
        for unit in cartlist:  #將購買商品寫入資料庫
            total = int(unit[1]) * int(unit[2])
            unitdetail = models.DetailModel.objects.create(dorder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
        orderid = unitorder.id  #取得訂單id
        mailfrom="jason568911@gmail.com"  #帳號
        mailpw="pqrl tbjh enxp qjtb"  #密碼
        mailto=customemail  #收件者
        mailsubject="正安數位購物網-訂單通知";  #郵件標題
        mailcontent = "感謝您的光臨，您已經成功的完成訂購程序。\n我們將儘快把您選購的商品郵寄給您！ 再次感謝您支持\n您的訂單編號為：" + str(orderid) + "，您可以使用這個編號回到網站中查詢訂單的詳細內容。\n正安數位購物網" #郵件內容
        send_simple_message(mailfrom, mailpw, mailto, mailsubject, mailcontent)  #寄信
        print('send mail')
        cartlist = []
        request.session['cartlist'] = cartlist

        status = None
        return render(request, "cartok.html", locals())

# def cartordercheck(request):  #查詢訂單
#     orderid = request.GET.get('orderid', '')  #取得輸入id
#     customemail = request.GET.get('customemail', '')  #取得輸email
#     if orderid == '' and customemail == '':  #按查詢訂單鈕
#         firstsearch = 1
#     else:
#         order = models.OrdersModel.objects.filter(id=orderid).first()
#
#         if order == None or order.customemail != customemail:  #查不到資料
#             notfound = 1
#         else:  #找到符合的資料
#             details = models.DetailModel.objects.filter(dorder=order)
#     return render(request, "cartordercheck.html", locals())

def cartordercheck(request):  #查詢訂單

    if not request.user.is_authenticated:  # 如果用户未登录
        orderid = request.GET.get('orderid', '')  # 取得輸入id
        customemail = request.GET.get('customemail', '')  # 取得輸email
        if orderid == '' and customemail == '':  # 按查詢訂單鈕
            firstsearch = 1
        else:
            order = models.OrdersModel.objects.filter(id=orderid).first()
            print(order)
            if order is None or order.customemail != customemail:  # 查不到資料
                notfound = 1
            else:  # 找到符合的資料
                details = models.DetailModel.objects.filter(dorder=order)
    else:  # 如果用户已登录
        data_list = []
        data_dic = {}
        is_login = 1
        orders = models.OrdersModel.objects.filter(user=request.user.id)
        # print(len(orders))
        if orders.exists():  # 如果用户有訂單
            # print(orders)
            login_has_order = 1
            for order in orders:
                details = models.DetailModel.objects.filter(dorder=order)
                # print(details)
                data_dic ={
                    "order": order,
                    "details": details
                }
                # print('---------------------')
                # print(data_dic)
                data_list.append(data_dic)  # 将每个订单的详情添加到列表中
            # print(data_list)
            # print(f'data_list長度:{len(data_list)}')
        else:
            logout(request)
            # return HttpResponse('Logout Successful')
            return redirect('cartordercheck')
    return render(request, "cartordercheck.html", locals())

def send_simple_message(mailfrom, mailpw, mailto, mailsubject, mailcontent): #寄信
    global message
    strSmtp = "smtp.gmail.com:587"  #主機
    strAccount = mailfrom  #帳號
    strPassword = mailpw  #密碼
    msg = MIMEText(mailcontent)
    msg["Subject"] = mailsubject  #郵件標題
    mailto1 = mailto  #收件者
    server = SMTP(strSmtp)  #建立SMTP連線
    server.ehlo()  #跟主機溝通
    server.starttls()  #TTLS安全認證
    try:
        server.login(strAccount, strPassword)  #登入
        server.sendmail(strAccount, mailto1, msg.as_string())  #寄信
    except SMTPAuthenticationError:
        message = "無法登入！"
    except:
        message = "郵件發送產生錯誤！"
    server.quit() #關閉連線

import requests
from django.http import JsonResponse

def tappay_payment(request):
    global customemail
    if request.method == 'POST':
        prime = request.POST.get('prime', '')
        email = request.POST.get('email', '')  # 获取电子邮件值
        customemail = email
        url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
        headers = {
            'content-type': 'application/json',
            #自己的帳號
            # 'x-api-key': 'partner_Jwvm9MmtorTjICdIxTHYDA4WnXc1gE5cER8lzXFQf1sAXmAHkTEMbAuL'
            #測試帳號
            'x-api-key': 'partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM'
        }
        payload = {
            # 自己的帳號
            # "partner_key": "partner_Jwvm9MmtorTjICdIxTHYDA4WnXc1gE5cER8lzXFQf1sAXmAHkTEMbAuL",
            # 測試帳號
            "partner_key": "partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM",
            "prime": prime,
            "amount": "1",
            # "merchant_id": "jason82603_CTBC",
            "merchant_id": "GlobalTesting_CTBC",
            "details": "Some item",
            "cardholder": {
                "phone_number": customphone,
                "name": customname,
                "email": email,
                "zip_code": "000",
                "address": customaddress,
                "national_id": "A123456789"
            }
        }
        print(payload)

        response = requests.post(url, json=payload, headers=headers)
        print('----------------------')
        print(response.json())
        global status_num
        status_num =response.json()['status']
        # 返回Tappay API的响应
        return JsonResponse(response.json())
    return render(request, "tappay_payment.html")