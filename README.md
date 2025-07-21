# locyanAutoCheckIn
根据[操作文档](./https://docs.locyanfrp.cn/api/doc-5617190)创建一个应用，重定向地址填`https://dashboard.locyanfrp.cn/callback/auth/oauth/localhost`<br>
记住appid，打开此网页得到refresh_token `https://dashboard.locyanfrp.cn/auth/oauth/authorize?app_id=此处替换&scopes=Sign.Info&redirect_url=https://dashboard.locyanfrp.cn/callback/auth/oauth/localhost?port=5000&ssl=false&path=/oauth/callback`<br>
在 Settings → Secrets and variables → Actions中分别创建两个变量`ID`和`TOKEN`并填入appid和refresh_token<br>
在Actions中启动
