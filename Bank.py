import sqlite3
import random
import string

con = sqlite3.connect('Bank88.db')
cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Branch(branch_name varchar(30),Number_of_Accounts int(10));")
cursor.execute("CREATE TABLE IF NOT EXISTS Customer (name varchar(30) , surname varchar(30),Mobile_Number int(10), account_Number int(10),account_type int(10));")
cursor.execute("CREATE TABLE IF NOT EXISTS Account( account_Number int(10) Primary Key, account_type int(1) , branch_name varchar(30),balance int(10));")
class AccountType:
    Checking = 1
    Savings = 2
    Loan = 3

class Account:
    def __init__(self, accountNumber, accountType, balance):
        self.accountNumber = accountNumber
        self.accountType = accountType
        self.balance = balance
        
        
    
    def deposit():
        
        try: 
            Acc = int(input("Enter Account Number :"))
            a = str(Acc)
            branch_naam = input("Enter Branch name:")
            name = input("Enter name as per account  : ")
            if not name.isalpha:
                print("Enter Valid Name??")
            else:
                surname = input("Enter surname as per account :")
                if not name.isalpha:
                    print("Enter Valid SurName??")
                else:
       
                    mobile = input("Enter Your Mobile number:")
                    t = str(Acc)
                    r = cursor.execute("""Select balance from Account INNER JOIN Customer ON
                            Account.account_Number = Customer.account_Number 
                            where name = (?) and surname = (?) and Account.account_Number = (?) and Mobile_Number = (?) and Account.branch_name = (?)""" , (name,surname,a,mobile,branch_naam))
        
                    mk = r.fetchone()
                    lo = list(mk)
                    p = lo[0]
                    b = int(input("Enter Amount to deposit : "))
                    l = p + b
                    
                    cursor.execute("""UPDATE Account SET balance = (?)
                                            where account_Number = (?)""" , (l,t))
                        
                    con.commit()
                    print("Amount Has Been Credited !!")
        except TypeError : 
            print("Account Not In DataBase !!!")
        
    def withdraw():
        try: 
            Acc = int(input("Enter Account Number :"))
            a = str(Acc)
            branch_naam = input("Enter Branch name:")
            name = input("Enter name as per account  : ")
            if not name.isalpha:
                print("Enter Valid Name??")
            else:
                surname = input("Enter surname as per account :")
                if not name.isalpha:
                    print("Enter Valid SurName??")
                else:
       
                    mobile = input("Enter Your Mobile number:")
                    t = str(Acc)
                    r = cursor.execute("""Select balance from Account INNER JOIN Customer ON
                            Account.account_Number = Customer.account_Number 
                            where name = (?) and surname = (?) and Account.account_Number = (?) and Mobile_Number = (?) and Account.branch_name = (?)""" , (name,surname,a,mobile,branch_naam))
                    
                    mk = r.fetchone()
                    lo = list(mk)
                    p = lo[0]
                    b = int(input("Enter Amount to Withdarw : "))
                    if b <= p:
                        l = p - b
                        
                        cursor.execute("""UPDATE Account SET balance = (?)
                                                where account_Number = (?)""" , (l,t))
                            
                        con.commit()
                        print("Amount Has Been Debited !!")
                    else:
                        print("Insufficient Balance")
        except TypeError : 
            print("Account Not In DataBase !!!")
        
    
    def getBalance():
        try:
            Acc = int(input("Enter Account Number :"))
            a = str(Acc)
            branch_naam = input("Enter Branch name:")
            name = input("Enter name as per account  : ")
            if not name.isalpha:
                print("Enter Valid Name??")
            else:
                surname = input("Enter surname as per account :")
                if not name.isalpha:
                    print("Enter Valid SurName??")
                else:
                    mobile = input("Enter Your Mobile number:")
                    y = cursor.execute("""Select balance from Account INNER JOIN Customer ON
                            Account.account_Number = Customer.account_Number 
                            where name = (?) and surname = (?) and Account.account_Number = (?) and Mobile_Number = (?) and Account.branch_name = (?)""" , (name,surname,a,mobile,branch_naam))
                    lo = y.fetchone()
                    p = list(lo)
                    for i in p:
                        print("Balance in your account is:" + str(i))
        except TypeError:
                print("Account Number,name,surname or mobilenumber is incorrect  ")
        except ValueError:
                print("Invalid Input !!!")
class Branch:
    
            
    def __init__(self, name):
        self.name = name
        self.customers = []
        self.accountNumberCounter = 0
        if not hasattr(Branch, 'accountNumberCounter'): 
            Branch.accNumberCounter = self.accountNumberCounter 
            
        Branch.accountNumberCounter = self.accountNumberCounter
        Branch.name = self.name    
            
    
    def addCustomer(self, customer):
        self.customers.append(customer)
        
        for Customers in self.customers:
            for Acc in Customers.accounts:
                
                cursor.execute("""INSERT INTO Customer(account_Number, Mobile_Number ,name ,surname , account_type)\
                VALUES (?,?,?,?,?) """,(Acc.accountNumber,Customers.MObileNumber,Customers.name ,Customers.surname , Acc.accountType))
                
        
    def getCustomer():
        try:
            Acc = int(input("Enter Account Number :"))
            a = str(Acc)
            y = cursor.execute("""Select Customer.account_Number, Customer.account_type , Customer.name , Customer.surname , Account.branch_name , Customer.Mobile_Number from Customer INNER JOIN Account ON
                                  Account.account_Number = Customer.account_Number 
                                  where Account.account_Number = (?)""" , [a])
            lo = y.fetchall()
            
            for i in lo:
                for j in range(0,len(i)):
                    print(i[j])
            
        except TypeError:
                print("Account Number,name,surname or mobilenumber is incorrect  ")
        except ValueError:
                print("Invalid Input !!!")
    
    def createAccount(self,account_number, customer, accountType , balance = 0):
        account = Account(account_number, accountType , balance)
        customer.addAccount(account)
        return account.accountNumber
class Customer(Branch,Account):
    def __init__(self, name , surname , MObileNumber):
        self.name = name
        self.surname = surname
        self.accounts = []
        self.MObileNumber = MObileNumber
    

    def addAccount(self, account):
        self.accounts.append(account)
        for Account in self.accounts:
            
            cursor.execute("""INSERT INTO Account (branch_name,account_Number,account_type , balance)\
            VALUES (?,?,?,?) """,(Branch.name,Account.accountNumber,Account.accountType,Account.balance))
            
        con.commit()
    def getAccount():
       try:
           
           name = input("Enter name as per account  : ")
           if not name.isalpha:
               print("Enter Valid Name??")
           else:
               surname = input("Enter surname as per account :")
               if not name.isalpha:
                   print("Enter Valid SurName??")
               else:
                   mobile = int(input("Enter mobile number :"))
                   o = str(mobile)
                   y = cursor.execute("""Select Customer.account_Number , Customer.account_type, Customer.name , Customer.surname , Account.branch_name , Customer.Mobile_Number from Customer INNER JOIN Account ON
                                         Account.account_Number = Customer.account_Number 
                                         where Customer.name = (?) and Customer.surname = (?) and Customer.Mobile_Number = (?)""" , (name,surname,o))
                   lo = y.fetchall()
                   
                   for i in lo:
                       for j in range(0,len(i)):
                           print(i[j])
           
       except TypeError:
               print("Account Number,name,surname or mobilenumber is incorrect  ")
       except ValueError:
               print("Invalid Input !!!")
class Bank(Branch):
    def __init__(self, name):
        self.name = name
        self.branches = []
        

    def addBranch(self, branch):
        self.branches.append(branch)
        e = cursor.execute("""SELECT Number_of_Accounts from branch\
        where branch_name = (?) """,(Branch.name))
        o = e.fetchone()
        print(o)
        if o == None:
            Branch.accNumberCounter = 1
            cursor.execute("""INSERT INTO Branch(branch_name,Number_of_Accounts)\
            VALUES (?,?) """,(Branch.name,Branch.accNumberCounter))
            con.commit()
        else:
            p = list(o)
            for i in p:
                s = i
            Branch.accNumberCounter = s + 1
            cursor.execute("""UPDATE Branch SET Number_of_Accounts = (?) WHERE
            branch_name = (?)""",(Branch.accNumberCounter,Branch.name))
            con.commit()
        
    def getBranch():
        r = cursor.execute("""SELECT branch_name From Branch""")
        o = r.fetchall()
        if o == None:
            print("There is not any branch available")
        else:
            print("List of all available branches: ")
            for i in o:
                for j in range(0,len(i)):
                    print(i[j])

def CreateAccount():
    try:
        a = (input("Enter Name : "))
        if not a.isalpha():
            print("Please enter only alphabetical characters for your name.")
        else:
        
            f = str(input("Enter a surname:"))
            
            if not f.isalpha():
                    print("Please enter only alphabetical characters for your surnamename.")
            else:
                    g = int(input("Enter Mobile Numner : "))
                    if len(str(g)) != 10:
                        print("Lenght Of Mobile number must equal 10:")
                    else:
                        s = True
                        while(s):
                                b = ''.join(random.choice(string.digits) for _ in range(8))
                               
                                
                                r = cursor.execute("""SELECT balance from Account Where account_Number = (?)""",[b])
                                o = r.fetchone()
                                if o == None:
                                    c = int(input("Enter the account type:"))
                                    if c >= 4:
                                        print("Enter valid account type:")
                                    else:
                                        d = input("Eneter Branch name:")
                                        e = int(input("Enter Opening Balance : "))
                                        
                                        
                                        branch1 = Branch(d)
                                        bank.addBranch(branch1)
                                            
                                        customer1 = Customer(a,f,g)
                                    
                                        branch1.createAccount(b,customer1,c,e)
                                                                            
                                        branch1.addCustomer(customer1)
                                        
                                        print("Account is created !!! With Account Number = "+ b+ " And Account Type is : " + str(c))
                                        s = False
            
              
    except ValueError:
        print("Invalid Input !!!")
    
    con.commit()

bank = Bank('Bank')
s = True
while(s):
    try:
        print('''
                  1. ADD/OPEN ACCOUNT 
                  2. DEPOSIT 
                  3. WITHDRAW
                  4. Show Balance
                  5 .Customer Information
                  6. Account Information
                  7. Get Branches
                  8. Close
                  
                  ''')
        c = int(input("Enter Your Choice :   "))
        if c == 1:
            CreateAccount()
        elif c == 2:
           Account.deposit()
        elif c == 3:
            Account.withdraw()
        elif c == 4 :
            Account.getBalance()
        elif c== 5:
            Branch.getCustomer()
        elif c == 6 :
            Customer.getAccount()
        elif c == 7:
            Bank.getBranch()
        elif c == 8:
            s = False
            con.close()
        else:
            print("Enter Value 1 to 8")
        
    except ValueError:
        print("Invalid Input !!!")
        continue
