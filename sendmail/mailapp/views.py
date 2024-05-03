from django.shortcuts import render
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPAuthenticationError, SMTPException

def index(request):
	strSmtp = "smtp.gmail.com:587"  #主機
	strAccount = "使用者gmail帳號"  #帳號
	strPassword = "使用者gmail密碼"  #密碼
	
	content = "這是寄送郵件測試，請勿回覆！"  #郵件內容
	msg = MIMEText(content)
	#msg = MIMEText(content, "plain", "utf-8")
	#content = "<h2>GMAIL寄信</h2><p>這是寄送郵件測試，請勿回覆！</p>"  #郵件內容
	#msg = MIMEText(content, "html")
	msg["Subject"] = "線上寄信"  #郵件標題
	mailto = "收件者電子郵件"  #收件者
	#mailto = ["收件者電子郵件"]  #收件者
	#mailto = ["收件者電子郵件一", "收件者電子郵件二"]

	server = SMTP(strSmtp)  #建立SMTP連線
	server.ehlo()  #跟主機溝通
	server.starttls()  #TTLS安全認證
	try:
		server.login(strAccount, strPassword)  #登入
		server.sendmail(strAccount, mailto, msg.as_string())  #寄信
		hint = "郵件已發送！"
	except SMTPAuthenticationError:
		hint = "無法登入！"
	except:
		hint = "郵件發送產生錯誤！"
	server.quit()  #關閉連線

	return render(request, "index.html", locals())
