
購物網站cart, 使用的資料庫是MYSQL
python manage.py runserver

1.購物網站首頁: 主要有分沒登入跟有登入的模式, 登入的情況下頁面會有所改變 

![image](https://github.com/jason82603/Django_shop/assets/39587624/f2281698-c8e7-47a2-bb58-05612c54b71a)

![image](https://github.com/jason82603/Django_shop/assets/39587624/ad94037a-04bc-45c9-afcb-65896de1f3e5)

2.註冊頁面Register

![image](https://github.com/jason82603/Django_shop/assets/39587624/b1070bcd-0e0f-4483-9f17-9662240614bf)


3.登入頁面

![image](https://github.com/jason82603/Django_shop/assets/39587624/64f2d0ef-10fd-490f-9410-818981e4cf21)

4.查詢訂單

(1) 有登入: 會自動抓取帳號過去的訂單紀錄

![image](https://github.com/jason82603/Django_shop/assets/39587624/75db19e9-c078-4885-ad79-1cb9c29bf11d)

(2) 沒登入: 得手動輸入訂單編號跟信箱

![image](https://github.com/jason82603/Django_shop/assets/39587624/3d1c83b9-5b02-44cc-a910-b07693d3c93c)

5.檢視購物車

![image](https://github.com/jason82603/Django_shop/assets/39587624/8e2dcaad-162f-4ecd-bd0c-4a2c6d33735a)

6.點選結帳: 點選結帳後, 輸入個人資料, 目前付款方式visa功能有特別串接tappay的測試帳號, 能完成類似線上支付的功能

![image](https://github.com/jason82603/Django_shop/assets/39587624/f0653fd6-890b-4d0d-b4b2-5d88abfc2daf)

7.線上支付: 

(1) 這裡信箱填真的話到時會收到訂單信件, visa卡號固定測試號碼:4242 4242 4242 4242, 卡片到期日就填超過當前時間就好, 卡片後三碼固定123

![image](https://github.com/jason82603/Django_shop/assets/39587624/7f7c6d28-7dbb-4255-8f1e-2071d852f7d0)

(2) 點下付款如果有成功, 首先會先去跟tappay申請prime碼, 成功的話會得到一串prime, 後端會把這個prime加入json檔的格式來串接tappay的API, 如果成功會顯示success
    並按下確定後跳轉到完成畫面

![image](https://github.com/jason82603/Django_shop/assets/39587624/a345efe7-cae7-4743-8e0f-da9ceedd43f7)

![image](https://github.com/jason82603/Django_shop/assets/39587624/9e2b2de3-6eec-447e-9430-07f20c7ffc81)

![image](https://github.com/jason82603/Django_shop/assets/39587624/dd5d7240-4d8d-4b0e-bd7c-9bea162f4661)

8.收到信件: 當初如果有寫入正確的信箱就會收到訂單信件

![image](https://github.com/jason82603/Django_shop/assets/39587624/b0cdd631-cea5-4f55-93e9-5ef90e42d4f0)

9.資料庫寫入訂單: 沒顯示user_id的就是沒有登入就直接購物

![image](https://github.com/jason82603/Django_shop/assets/39587624/39f5f563-4910-4567-aba0-f7602af8476c)





