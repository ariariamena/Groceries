import Common
import datetime

history_list=[]

def load_history(filename):
    global history_list
    '''
    load history of which recipes were chosen as a function of time
    A history is a dict with 'Date' and 'Recipes' as keys
    '''

def update_time_since(recipe):
    '''
    Update the time_since field in the provided recipe obj
    '''
    global history_list

def IsSpring(date):
    return date.month >= 4 and date.month <= 5

def IsSummer(date):
    return date.month >= 6 and date.month <= 8

def IsFall(date):
    return date.month >= 9 and date.month <= 10

def IsWinter(date):
    return date.month >= 11 or date.month <= 3

def Update(recipes, date = datetime.date.today()):
    '''
    Add recipes to global history and update the individual recipes in global_state
    '''
    history = Common.global_state.history
    history.entries.append(Common.HistEntry(recipes))
    Common.global_state.history = history

    for r in recipes:
        r.last_cooked = date
        Common.global_state.all_recipes = [a if a.name != r.name else r for a in Common.global_state.all_recipes]
    return
