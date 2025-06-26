"""Hello ! This is me Samia Qadri, student of BSSE,UBIT,KU. 
   This is a stock tracker portfolio for user.
   Suggestions and Feedback are always welcome.
   LinkedIn : Samia Qadri. """


import os
import main
try:
                  
    print("WELCOME TO STOCK PORTFOLIO TRACKER: ")
    print("Note: For Pakistani shares, mention '.KA' in name and their visible record is limited")
    print("Internet is needed ! ")
    print("")
    dollar_rate=float(input("Enter Todays dollar rate i.e 1 dollar in pkr value  :  "))
    print("---------")
    run=True
    while run:
        print("\n===========\n")
        print("MENU: ")
        print("Press 1 to add or update a stock")
        print("Press 2 to view stocks and check gain/loss.  ")
        print("Press 3 to remove stock or shares.  ")
        print("Press 4 to search for a stock ,its price and volume (sold and bought). ")
        print("Press 5 to view trending stocks. ")
        print("Press 6 to view graph")
        print("Press 7 to view your total investment.")
        print("Press 8 to exit")
        print("\n===========\n")
        try:
            user_ans=int(input("Enter: "))
            if(user_ans==1):
                main.user_entry(dollar_rate)
            elif( user_ans ==2):
                main.view_stocks(dollar_rate)
            elif( user_ans == 3):
                main.remove_stock(dollar_rate)
            elif( user_ans == 4):
                main.info_stock(dollar_rate)
            elif (user_ans==5):
                main.view_trending(dollar_rate)    
            elif(user_ans==6):
                print("1. Stock and Volume graph.")
                print("2. Stock and price graph. ")
                graph=int(input("Enter  1 or 2 : "))
                main.plot_graph(graph,dollar_rate)
            elif (user_ans== 7):
                main.total_investment()    
            elif (user_ans == 8 ):
                run=False
        except ValueError:
            print("Invalid entry !")
            continue
except Exception as e:
    print(e)            