from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List 
from datetime import date

app = FastAPI(title="Expense Tracker API")
#model

class Expense(BaseModel):
    id: int
    title: str 
    amount: float 
    category: str 
    date: date 
expense: List[Expense] = []

@app.get("/")
def home ():
    return{"message":"Expense Tracker API is running successfully"}

# Add Expenses

@app.post("/expenses")
def add_expense(expense: Expense):
    for exp in expenses:
        if exp.id == expnese.id:
            raise HTTPException(status_code=400,detail="Expense ID is already Exists")
    expense.append(expense)
    return{
        "message":"Expense added successfully",
        "expense":expense
    }
# View all expenses

@app.get("/expenses")
def get_all_expenses():
    return expenses 

#Filter by Category

@app.get("/expenses/category/{category}")
def get_expenses_by_category(category:str):
    filtered =[
        expense for expense in expenses 
        if expense.category.lower()== category.lower()
        
    ]
    return filtered 

#Overall Total
@app.get("/expenses/total")
def overall_total():
    total=sum(exp.amount for exp in expenses)
    return{
        "oveall_total": total
    }

#Category-Wise Total
@app.get("/expense/category-total")
def category_total():
    totals={}
    for expense in expenses:
        totals[expenses.category]=totals.get(expense.category,0)+expense.amount
    return totals

#Delete Expense
@app.delete("expenses/{expense_id}")
def delete_expense(expense_id:int):
    for expense in expenses:
        if expense.id==expense_id:
            expenses.remove(expense)
            return {"message":"Expense deleted successfully"}
    raise HTTPException(status_code=404,detail="Expense not found")
        