# INDEX 📋

* **Mislabot**  
  + [**About project**](#about-project) ⭐
  + [**Preview**](#preview) 🔍
  + [**Technologies**](#technologies) 💻
  + [**Setup**](#setup) 🔧
  + [**Usage**](#usage) 📋
  + [**Status**](#status) ⚪
  + [**Contact**](#contact) 📞

# About project⭐

**Date**: April, 2024.   
**Duration**: 7 days.

This project was developed in order to learn **Rasa** and create a custom chatbot from scratch. It's a task of creating a chatbot for the CIPFP Mislata website.

# Preview🔍

Web Chatbot

![GIF](https://github.com/Hukex/Mislabot/blob/main/readmefiles/web.gif?raw=true)
 
Telegram Bot

![GIF](https://github.com/Hukex/Mislabot/blob/main/readmefiles/telegram.gif?raw=true)

> <img src="extras/mislabot.png" height="300"/>

# Technologies💻

* **RASA**
* **AWS EC2**
* **FLASK**
* **APACHE**
* **TELEGRAM**
* **PYTHON**

# Setup🔧

``` bash
git clone https://github.com/Hukex/Mislabot.git
```
If you want to try the bot, you can deploy it locally by installing all requirements for Rasa. Additionally, you have *mislabotweb.html* for loading in your browser.

However, if you want to deploy it for use on Telegram, you'll need an SSL certificate for HTTPS because Telegram only supports this. You'll also need a domain, but you could use the nip.io DNS service. This will help you avoid the need for a domain. In my case, I used Let's Encrypt for SSL.

I used AWS EC2 because it was the server available to me at the time, but you have all the necessary configuration to make it work. I also have the Apache configuration file *httpd.conf* available in case you need it.

``` bash
rasa train
rasa run actions
rasa run --enable-api --cors
```


# Usage📋

You can search for it on Telegram **Misla_bot** or [**Web**](https://18.214.170.176.nip.io/). 

However, please note that my server may be down because it consumes resources and was only used for practice.

# Status⚪

**Finished.**

It was for practice so its finished

# Contact📞

My name is [Fernando](https://www.linkedin.com/in/fevm/), you can contact me if you desire!

## 😃 Thanks for reading. 👋
