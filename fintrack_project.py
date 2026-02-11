# add_category()        --> add expense category
# add_expense()         --> add new expense record
# update_expense()      --> update existing expense
# delete_expense()      --> delete expense entry
# search_by_date()      --> find expenses by date
# category_report()     --> category-wise expense analytics
# set_budget()          --> set monthly budget limit
# budget_alert()        --> check if monthly budget exceededs


from sqlalchemy import create_engine,Column,String,Integer,ForeignKey,Date,text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

#database connection
engine = create_engine("sqlite:///Cli_Finance_Manager.db")

Base=declarative_base()

#session maker
Session=sessionmaker(bind=engine)
session=Session()

class Categories(Base):
    __tablename__="categories"
    
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False) #nuallable=false-->decides column should be empty or not
    
    expenses=relationship("Expense",back_populates="category")
    
#Relationship-->We are creating one to many relationship between category and expenses where each expense have one category using category but one category can have more expenses
class Expense(Base):
    __tablename__="expenses"
    
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    amount=Column(Integer,nullable=False)
    date=Column(String,nullable=False)
    
    category_id=Column(Integer,ForeignKey("categories.id"))
    category=relationship("Categories",back_populates="expenses")
   
    
class Subscription(Base):
    __tablename__="subscriptions"
    
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    amount=Column(Integer,nullable=False)
    next_date=Column(Date,nullable=False)
    
class Budgets(Base):
    __tablename__="budgets"
    
    id=Column(Integer,primary_key=True)
    month=Column(String,nullable=False)
    limit=Column(Integer,nullable=False)
    
    
#ADD_CATEGORY    
def add_category():
    name=input("Category name: ")5
    session.add(Categories(name=name))
    session.commit()
    print("Category added")
     
#ADD_EXPENSE   
def add_expense():
    title=input("Expenses title: ")
    amount=int(input("Amount: "))
    date=input("Date(YYYY-MM-DD): ")
    category_id=int(input("Category ID: "))
        
    session.add(Expense(
        title=title,amount=amount,date=date,category_id=category_id))
    session.commit()
    print("Expense added")
    
    #UPDATE_EXPENSE
def update_expense():
    eid=int(input("Expense id: "))
    #check given id to existing id and check
    expense=session.query(Expense).filter(Expense.id==eid).first()
    
    
    if expense:
        expense.title=input("New title: ")
        expense.amount=int(input("New amount: "))
        expense.date=input("New date (YYYY-MM-DD): ")
        session.commit()
        print("Expense updated")
    else:
        print("Expense not found")
        
#DELETE EXPENSE
def delete_expense():
    eid=int(input("Expense ID: "))
    expense=session.query(Expense).filter(Expense.id==eid).first()
        
    if expense:
        session.delete(expense)
        session.commit()
        print("Expense deleted")
    else:
        print("Expense not found")
            
def search_by_date():
    date=input("Enter date (YYYY-MM-DD): ")
    expenses=session.query(Expense).filter(Expense.date==date).all()
    
    for e in expenses:
        print(e.title, "-",e.amount,"-",e.date)
            
def category_report():
    query="""SELECT c.name,SUM(e.amount) FROM categories c JOIN expenses e ON c.id = e.category_id GROUP BY c.name"""
    result=session.execute(text(query))
        
    for name,result in result:
        print(name,":",total)
            
def set_budget():
    month=input("Month (YYYY-MM): ")
    limit=int(input("Monthly limit: "))
        
    session.add(Budgets(month=month,limit=limit))
    session.commit()
    print("Budget set")
        
def budget_alert():
    month = input("Enter month (YYYY-MM): ")

    #Fetches all expenses of a given month from the database.
    expenses = session.query(Expense)\
        .filter(Expense.date.like(f"{month}%"))\
        .all()

    total = 0
    for e in expenses:
        total += e.amount

    #Fetches the budget record for a specific month from the database.    
    budget = session.query(Budgets)\
        .filter(Budgets.month == month)\
        .first()

    if not budget:
        print("No budget set")
    elif total > budget.limit:
        print("Budget exceeded by", total - budget.limit)
    else:
        print("Within budget")


while True:
    print(""" ----FINTRACK PRO----
          1.Add Category
          2.Add Expense
          3.Update Expense
          4.Delete Expense
          5.Search Expense by Date
          6.Category-wise Expense Report
          7.Set Monthly Budget
          8.Budget Alert
          9.Exit
          """)
    
    choice = input("Choose: ")
    
    if choice =="1":
        add_category()

    elif choice == "2":
        add_expense()
        
    elif choice == "3":
        update_expense()
        
    elif choice == "4":
        delete_expense()
        
    elif choice == "5":
        search_by_date()
        
    elif choice == "6":
        category_report()
        
    elif choice == "7":
        set_budget()
        
    elif choice == "8":
        budget_alert()
        
    elif choice == "9":
        print("Exiting FinTrack ")
        break
    
    else:
        print("Invalid choice")












       