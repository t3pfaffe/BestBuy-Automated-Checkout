 BestBuy-Automated-Checkout
A bot to constantly run and purchase item on BestBuy.com


Hello all,

Currently the webdriver import will probably only work on Linux as it can easily access chromium from the environment variables. In windows I belive you usally have to download a seperate webdriver.exe and provide that files location in the ChromeDriver() declaration.


Requirements:\
 Selenium\
 Tkinter\
 Chrome webdriver
 
Orginal Release v1.0:\
With this initial release the code does work to at least always add the item to your cart as of 11/29/20 and is able to purchase any item that registers as in stock on the BestBuy or Walmart website. It does require that you give the SKU number of the item you are trying to get. This is easily avaialbe on the products webpage for BestBuy. On Walmart it appears only visible in the products URL.

It works by spawning a webriver instance of Chromium and refreshing the desired page(s) of the items you desire until it is in stock. Then it adds said item to the cart and attempts a checkout. 

In BestBuy it assumes you have an account (probably best to not use an account you use normally) that has a saved address and card. The same is true with Walmart. In either cases the bot may get messed up at checkout in the event that a captcha is called for by the website. There is really nothing that can be done to fix this but hoping you solve the captcha in time. 
  
How to use:

1) Make sure that all required libraries are installed.
2) Rename the "config_" file to "config".
3) (If in Windows) Save the Chrome webdriver in the same directory as BestBuybot.py
4) Open the config file with a text editor and fill in the parameters with your information, if you are an employee of BestBuy there is a field for your employee number.
5) Edit the code and change the field of the config's SKU field to contain the skus that you want(each one separated by commas e.x: 1234,9876).
6) Run bot and Enjoy

Picture of code working:

![BestBuy Bot Succsess](https://user-images.githubusercontent.com/55165705/98168055-df014300-1e9e-11eb-9eeb-f8911be903d2.JPG)


Link to latest version of ChromeWebdriver for windows:
https://chromedriver.chromium.org/downloads
