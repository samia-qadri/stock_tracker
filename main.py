import os
import json
import yfinance as yf
import matplotlib.pyplot as plt

try:
 current_dir= os.path.dirname(__file__)
except NameError:
    current_dir = os.getcwd()
file_path = os.path.join (current_dir,"stocks.json")

try:
      with open(file_path,"r") as file:
        data= json.load(file)
except:
        data = {
            "stocks" : [],
            "total_investment_pkr" : 0,
            "trending": [],
            "pak_stocks_name": {}
        }
try:        
    # This function will fetch information through yahoo finance via yfinance API
    def get_stock_info(symbol):  
        try:   
         stock= yf.Ticker(symbol)
         info= stock.info
         return info  
        except Exception as e:
            print("Error! Check your internet connection. Troubleshot Error.")
            print (e)
            return {}
        
    # to display stock information to avoid code repetition
    # it will also show user gain or loss in particular stock
    def display(value,info,dollar_rate):
        
        purchased_price = value['purchased price']
        if ".KA" in value ['name']:
            try:
                current_price_USD=round(float(input(f"Enter current price of one share of {value['name']} in USD : ")),3)
            except ValueError:
                print("Invalid price !") 
                return 
        else:
            current_price_USD = info.get('regularMarketPrice') 
            if current_price_USD is None:
                print("Can't get value rightnow,may be due to internet problem. Assuming it 0.0 ")
                current_price_USD = 0.0
            
        current_price_pkr = current_price_USD*dollar_rate
        print(f"Name        : {value ['name'] }")
        print(f"Quantity    :  {value ['quantity']}")
        print(f"Purchased Price USD : {purchased_price}")
        print(f"Current Price USD : {current_price_USD}")
        print(f"Current Price PKR : {current_price_pkr}")
        print(f"investment in pkr : {value['investment in pkr']}")
        print("")
        print("Gain/Loss Check : " )
        result = round((current_price_USD-purchased_price)*dollar_rate *value["quantity"],3)
        if result > 0:
            print(f"📈 Gain in PKR: {result}")
        elif result < 0:
            print(f"📉 Loss in PKR: {abs(result)}")
        else:
            print("No gain, no loss.")
        print("--------------")
        
    #  used to add or update a stock , it also saves the changes made in json   
    def user_entry(dollar_rate):
        
        name = input("Enter name of stock :  ").upper()
        try: 
            quantity = int(input("Enter quantity of stock purchased :  "))
            price = round(float(input("Enter price of single stock in USD :  ")),3)
        except ValueError:
                print("Invalid entry !") 
                return    
        price_pkr = price*dollar_rate
        total = quantity*price_pkr 
        
        for value in data["stocks"]:
            if name == value["name"]:
            # calculating average of purchases price of old and new stock :    
                total_quantity = value["quantity"] + quantity
                old_investment = value["quantity"] * value["purchased price"]
                new_investment = quantity * price
                new_avg_price = round((old_investment + new_investment) / total_quantity, 3)
            #it updates
                value["quantity"]+=quantity
                value["purchased price"] = new_avg_price
                value["investment in pkr"] +=total
                data["total_investment_pkr"] += total
                break
        else:
            new_stock = {
                "name": name,
                "quantity" : quantity,
                "purchased price" : price,
                "investment in pkr" : total
                }
            data["total_investment_pkr"] += total
            
            data["stocks"].append(new_stock)  
            
        
        with open(file_path,"w") as file:
         json.dump(data,file,indent=4)
        print("stock added ! ")
        
    # removes specific quantity of stock  
    def remove_stock(dollar_rate):
        name = input("Enter name of stock :  ").upper()
        try:
            quantity = int(input("Enter quantity of stock you want to remove (sold) :  "))
            price = round(float(input("Enter price of single stock in USD :  ")),3)
        except ValueError:
                print("Invalid entry !") 
                return
        price_pkr = price*dollar_rate
        total = quantity*price_pkr 
        for value in data["stocks"]:
            if name == value["name"]:
                
            #it updates i.e remove user defined quantity of stock
                if quantity > value["quantity"]:
                    print(f"You have {value['quantity']}, so you can't sell this {quantity} amount.")
                    return
                value["quantity"]-=quantity
                value["investment in pkr"] -=total
                data["total_investment_pkr"] -= total
                
                if value["quantity"] == 0:
                    data["stocks"].remove(value)
                break 
        else:
            print("Stock not found in portfolio.")    
            
        with open(file_path,"w") as file:
         json.dump(data,file,indent=4)
        print("stock updated ! ")
    # show a particular stock or all stock to user    
    def view_stocks(dollar_rate):
    
        user_choice = input("Do you want to check a particular stock or all ?  ").lower()
        if("particular" in user_choice or "specific" in user_choice):
            targetted_stock=input("Which stock do you want to track: ").upper()
            
            for value in data["stocks"]:
                if targetted_stock == value["name"]:
                    info = get_stock_info(value["name"])
                    display(value,info,dollar_rate)
                    break
            else:
                print("Not found ! Do you want to add a new stock ? ")
                ask_add=input("Yes / No").lower().strip()
                if(ask_add == "yes"):
                    user_entry(dollar_rate)
                    
        elif ("all" in user_choice):
            
            print("\nYour portfolio : ")
            for value in data["stocks"]:
                info = get_stock_info(value["name"]) 
                display(value, info,dollar_rate)
                
            print("The total investment you have made is (in pkr): ",data["total_investment_pkr"])
        else:
            print("Sorry! Couldn't understand. ")
        
        
        # to fetch information of stock via API    
    def info_stock(dollar_rate):
        
        stock = input("About which stock you want to check (e.g: AAPL): ").upper()
        info = get_stock_info(stock)
        
        if "shortName" in info:
            current_price_USD=info.get('regularMarketPrice','Not Available')
            if current_price_USD is None:
                print("Can't get value right now,may be due to internet problem. Assuming it 0.0 ")
                current_price_USD=0.0
            current_price_pkr = current_price_USD*dollar_rate
            
            print("\n----STOCK INFORMATION-----")
            print(f"Company name  :  {info.get('shortName','Not available')}")
            print(f"Current price in USD:  {current_price_USD}")
            print(f"Current price in pkr :  {current_price_pkr}")
            print(f"Market cap :     {info.get('marketCap','Not Available')}")
            print(f"Volume (no.of shares bought and sold) :  {info.get('volume','Not Available')}")
        else:
            print("Sorry ! Couldn't get information. Please enter correct stock symbol")
            
        # to view trending stocks (pre-defined) and fetch their volume, price
    def view_trending(dollar_rate):
        
        print("\n----TRENDING STOCKS -----")
        
        for value in data["trending"] :
            get_info= yf.Ticker(value)
            info=get_info.info
            
            if "shortName" in info:
                print(f"Company name  :  {info.get('shortName','Not Available')}")
                current_price_USD=info.get('regularMarketPrice','Not Available')
                if current_price_USD is None:
                    print("Can't get value right now,may be due to internet problem. Assuming it 0.0 ") 
                    current_price_USD=0.0 
                current_price_pkr=current_price_USD*dollar_rate
                print(f"Current price USD :  {current_price_USD}")
                print(f"Current price in pkr :  {current_price_pkr}")
                print(f"Volume (no.of shares bought and sold) :  {info.get('volume','Not Available')}")
                print("")
            else:
                print("Sorry ! I can't give record of trending stocks at the moment.")  
                
     # it shows the total investment user has made           
    def total_investment():
        print(f"You have total investment of : {data['total_investment_pkr']}  PKR .")   
        print(f"Your shares are in following Stocks : ")        
        for value in data["stocks"]:
            print(value["name"],end="   ") 
        print("")    
        
    # plots graph to visually represent stock data                 
    def plot_graph(graph,dollar_rate):    
        if (graph ==1 ) :
            name=[]    
            volume=[]
            for value in data["trending"]:
                info=get_stock_info(value)
                if (".KA" in value):
                    continue
                stock_volume=info.get('volume',0)
                if stock_volume is None:
                    continue
                volume.append(stock_volume)
                name.append(value)
                    
            plt.bar(name,volume,color="blue")  
            plt.xlabel ("name")
            plt.ylabel ("volume")
            plt.title("Trending stocks ")
            plt.xticks(rotation=45)
            plt.show()
        elif (graph==2):
            currency=input("You want in PKR or USD? ").upper()
            name=[] 
            price=[]
            for value in data["trending"]:
                info=get_stock_info(value)
                if (".KA" in value):
                    continue
                if (currency=="USD"):
                    stock_price=info.get('regularMarketPrice',0)
                elif(currency=="PKR"):
                    get_price=info.get('regularMarketPrice',0)
                    if get_price is None:
                        continue
                    stock_price=get_price*dollar_rate
                else:
                    print("Invalid ! ")
                    return 
                price.append(stock_price)
                name.append(value)
                    
            plt.bar(name,price,color="blue")  
            plt.xlabel ("name")
            if (currency=="USD"):
                plt.ylabel ("price (USD)")
            elif(currency=="PKR"):
                plt.ylabel ("price (PKR)")
            plt.title("Trending stocks ")
            plt.xticks(rotation=45)
            plt.show()
                  
except Exception as e:
    print(e)
