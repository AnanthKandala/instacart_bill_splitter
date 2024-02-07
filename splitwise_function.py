from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser


def create_expense(expenses, creditor, expense_title):
    consumer_key = "" #replace with your consumer key from splitwise
    consumer_secret = "" #replace with your consumer secret from splitwise
    access_token = {'access_token': '', 'token_type': 'bearer'}
    splitwise_Id = {'name': splitwise_id} #replace with your splitwise id
    s = Splitwise(consumer_key, consumer_secret)
    s.setOAuth2AccessToken(access_token)
    #creating a new expense
    expense = Expense()
    expense.setCost(str(sum(expenses.values())).zfill(2))
    expense.setDescription(expense_title)

    #adding users to the expense
    expense_users = {person:ExpenseUser() for person in expenses.keys()}
    for person, expense_user in expense_users.items():
        expense_user.setId(splitwise_Id[person])
        expense_user.setOwedShare(str(expenses[person]).zfill(2))
    for person in expenses.keys():
        if person == creditor:
            expense_users[creditor].setPaidShare(str(sum(expenses.values())).zfill(2))
        else:
            expense_users[person].setPaidShare('0.00')
        expense.addUser(expense_users[person])
    newExpense, errors = s.createExpense(expense)
    assert errors==None, 'There was an error in creating the expense'
    print(newExpense.getId())
    return newExpense.getId()