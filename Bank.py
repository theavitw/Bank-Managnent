import  sqlite3

con  =  sqlite3.connect ('Bank8.db')
cursor  =  con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Branch(branch_name varchar(30), NAccounts int(5));")
cursor.execute("CREATE TABLE IF NOT EXISTS Customer (account_Number int(10),name varchar(30));")
cursor.execute("CREATE TABLE IF NOT EXISTS Account( account_Number int(5), account_type int(1) , balance int(10));")

class AccountType:
    CHECKING = 1
    SAVINGS = 2
    LOAN = 3

class Account:
    def __init__(self, accountNumber, accountType, balance=0):
        self.accountNumber = accountNumber
        self.accountType = accountType
        self.balance = balance
        
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError('Insufficient balance')
        self.balance -= amount
    
    def getBalance(self):
        return self.balance
class Customer:
    def __init__(self, name):
        self.name = name
        self.accounts = []


    def addAccount(self, account):
        self.accounts.append(account)
        for Account in self.accounts:
            cursor.execute("""INSERT INTO Account (account_Number,account_type , balance)\
            VALUES (?,?,?) """,(Account.accountNumber,Account.accountType,Account.balance))
        con.commit()
    def getAccount(self, accountNumber):
        for account in self.accounts:
            if account.accountNumber == accountNumber:
                return account
        return None
class Branch:
    def __init__(self, name):
        self.name = name
        self.customers = []
        self.accountNumberCounter = 1
    
    def addCustomer(self, customer):
        self.customers.append(customer)
        for Customers in self.customers:
            for Acc in Customers.accounts:
                cursor.execute("""INSERT INTO Customer(account_Number ,name)\
                VALUES (?,?) """,(Acc.accountNumber,Customers.name))
        con.commit()
    def getCustomer(self, name):
        for customer in self.customers:
            if customer.name == name:
                return customer
        return None
    
    def createAccount(self, customer, accountType , balance = 0):
        account = Account(self.accountNumberCounter, accountType , balance)
        customer.addAccount(account)
        self.accountNumberCounter += 1
        return account.accountNumber

class Bank:
    def __init__(self, name, fileName):
        self.name = name
        self.branches = []
        self.fileName = fileName


    def addBranch(self, branch):
        self.branches.append(branch)
        for Branches in self.branches:
            cursor.execute("""INSERT INTO Branch(branch_name,NAccounts)\
            VALUES (?,?) """,(Branches.name,Branches.accountNumberCounter))
        con.commit()
        self.writeToFile()
    def getBranch(self, name):
        for branch in self.branches:
            if branch.name == name:
                return branch
        return None

    def readFromFile(self):
        try:
            with open(self.fileName, 'r') as file:
                for line in file:
                    data = line.strip().split(",")
                    
                    if len(data) == 2:
                        branch = Branch(data[0])
                        self.addBranch(branch)
                    elif len(data) == 3:
                        customer = Customer(data[0])
                        account = Account(int(data[2]), AccountType[data[3]])
                        customer.addAccount(account)
                        branch = self.getBranch(data[1])
                        if branch:
                            branch.addCustomer(customer)
                        else:
                            branch = Branch(data[3])
                            branch.addCustomer(customer)
                            self.addBranch(branch)
        except FileNotFoundError:
            pass
    
    def writeToFile(self):
        with open(self.fileName, 'w') as file:
            for branch in self.branches:
                for customer in branch.customers:
                    for account in customer.accounts:
                                file.write(f"Customer_name : {customer.name},branch_name : {branch.name},account no.: {account.accountNumber} ,account type : {account.accountType} , account balance : {account.balance}\n")
                                
                                

if __name__ == '__main__':

    bank = Bank('My Bank', 'data.txt')
    bank.readFromFile()
    
    
    branch1 = Branch('Branch 1')
    bank.addBranch(branch1)
    
    
    customer1 = Customer('John Smith')
    customer2 = Customer("Avit")
    accountNumber1 = branch1.createAccount(customer1, AccountType.CHECKING)
    accountNumber2 = branch1.createAccount(customer2,AccountType.LOAN,10000)
   
    account1 = customer1.getAccount(accountNumber1)
    account2 = customer2.getAccount(accountNumber2)
    account1.deposit(100)
   
    
    
    
    branch1.addCustomer(customer1)
    branch1.addCustomer(customer2)
    e = cursor.execute("Select * from branch")
    print(e.fetchall())
    f = cursor.execute("select * from Customer")
    print(f.fetchall())
    t = cursor.execute("select * from Account")
    print(t.fetchall())
    bank.writeToFile()
    con.close()