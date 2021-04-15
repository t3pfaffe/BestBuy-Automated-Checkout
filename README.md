 BestBuy-Walmart-Automated-Checkout(ish):
 =======================================
A bot to run and periodically check for stock and purchase items on BestBuy.com or Walmart.com. 

### Hello all,

This is a script heavily modified from [@Konyanj0278](https://github.com/Konyanj0278/BestBuy-Automated-Checkout)'s original work that should hopefully be able to grab items and checkout with the as quickly as possible when they come back into stock. It works by spawning a webriver instance of Chromium and refreshing the desired page(s) of the items you desire until it is in stock. It then adds said item to the cart and attempts a checkout. I am directly @'ing Walmart's and BestBuy's security teams for somehow not having ratelimiters or always on Captcha to prevent these scripts from working.

When it is actually working https://github.com/Strip3s/PhoenixBot/ is a more robust and effective bot. However it's BestBuy script does not work at all at the moment and there are problems with its Walmart checkouts as well. The bot's Target and Gamestop bots have apparently been working as of late so check those out. If your looking to commit code anywhere it would probably be best to help out with anything over there rather than with this side project.

New Release v1.2:
----------------
With this release the code does work to at least always add the item to your cart as of 11/29/20 and is able to purchase any item that registers as in stock on the BestBuy or Walmart website. It does require that you give the SKU number of the item you are trying to get. This is easily avaialbe on the products webpage for BestBuy and On Walmart it appears only visible in the products URL. It may not reliably checkout due to variability and random pressence of Captcha.

Getting Started:
---------------
### Code Dependanceis:
 * Selenium
 * Tkinter
 * Chrome webdriver
 
### Other Requirements/Notes:
- In BestBuy it assumes you have an account (probably best to not use an account you use normally) that has a saved address and card. The same is true with Walmart. In either cases the bot may get messed up at checkout in the event that a captcha is called for by the website. There is really nothing that can be done to fix this but hoping you solve the captcha in time.
- Currently the webdriver import will probably only work on Linux as it can easily access chromium from the environment variables. In windows I belive you usally have to download a seperate webdriver.exe and provide that files location in the ChromeDriver() declaration.
- As mentioned earlier, its best not to use an account on these sites that you would dislike not being able to use incase it gets banned. It is also proably best if you dont use your normal card for the same concerns as well as the fact that you should not be trusting random scripts found on the internet with you card details. To deal with that there are card proxy services you can use. [Privacy.com](https://privacy.com/join/QMYUX) or [Abine Blur](https://dnt.abine.com/#/ref_register/p9PfxnAtt
) is an option for this but the later I belive is paid while the former is free. Even though its free I dont believe it subsists off marketing user data since it is able to collect the ~3% proccessing fee all card vendors get in Visa transactions as "payment." *(Disclaimer my account gets some form of reward points if you use that Privacy.com link).*
  
### How to use:
1) Make sure that all required libraries are installed.
2) Rename the "config_" file to "config".
3) (If in Windows) Save the Chrome webdriver in the same directory as BestBuybot.py
4) Open the config file with a text editor and fill in the parameters with your information, if you are an employee of BestBuy there is a field for your employee number.
5) Edit the code and change the field of the config's SKU field to contain the skus that you want(each one separated by commas e.x: 1234,9876).
6) Run bot and Enjoy

#### Picture of code working:
 ![BestBuy Bot Succsess](https://user-images.githubusercontent.com/55165705/98168055-df014300-1e9e-11eb-9eeb-f8911be903d2.JPG)


#### Link to latest version of ChromeWebdriver for windows:
https://chromedriver.chromium.org/downloads


---------------------------
##### Disclamer: 
######    This code or my opinions on it are not endoresed or supported by the companies BestBuy & Walmart. It is possible that using this code you could be violating your terms of service with both afformentioned companies as well as any 3rd parties utilized in transaction such as Visa or Mastercard. In the event that you do violate such terms of service the developers of this software are not liable for any consequences. Please be smart about using this software, thanks.
