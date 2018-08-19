import Common
import Ingredients
import copy

def MakeGroceryList(recipes):
    '''
    Give a set of recipes, and get a grocery list
    Parameters:
        recipes : Recipe []
            List of recipes you're getting
    Returns:
        Ingredient []
            List of ingredients
    '''
    # name='', location='Other', staple=False, seasons='sufw', perishable=False, family_pack=False, quantity = 0, unit = '', store_quantity = 1, meat_type = ''):
    grocery_list = []
    for r in recipes:
        ingr = r.ingredients
        for i in ingr:
            if i.name not in [g.name for g in grocery_list]:
                grocery_list.append(i)
            else:
                next((x for x in grocery_list if x.name == i.name), None).store_quantity+=1
    grocery_list = SortIngredients(grocery_list)

    return grocery_list

def IngredientVal(ingredient):
    location = ingredient.location
    return Ingredients.valid_locations.index(location)

def SortIngredients(ingredients):
    '''
    Sort a list of ingredients in grocery store order
    '''
    ingredients_copy = copy.deepcopy(ingredients)
    sorted_ingredients = []
    while len(sorted_ingredients) < len(ingredients):
        #find minimum ingredient:
        vals = [IngredientVal(i) for i in ingredients_copy]
        minimum_ingr_val = min(vals)
        index = vals.index(minimum_ingr_val)
        sorted_ingredients.append(ingredients_copy[index])
        del ingredients_copy[index]
    return sorted_ingredients

def RemoveCommonIngredients(ingredients):
    '''
    Remove ingredients that you probably already have, selectively
    '''
    Common.log("ingredients before staple reduction: "+str([i.staple for i in ingredients]))
    reduced_ingredients = [i for i in ingredients if i.staple == False]
    Common.log("ingredients after staple reduction: "+str([i.staple for i in reduced_ingredients]))
    return reduced_ingredients

def ListToString(ingredients):
    '''
    Turn a list of ingredients to a string
    '''
    list_str = '\n--------------------------'
    list_str += '       Grocery List       '
    list_str += '--------------------------\n'
    sorted_ingredients = SortIngredients(ingredients)
    list_str+='\n'.join([i.GroceryStoreFormatString() for i in sorted_ingredients])
    list_str+="\n"
    return list_str

def AddIngredientToGroceryListMenu(global_state, grocery_list):
    grocery_list = Common.AddItem(grocery_list, 'an ingredient', 'ingredients', Ingredients.ListIngredients, global_state.all_ingredients, Ingredients.IngredientByName)
    return grocery_list #TODO consider whether to add quantity as an option

def DisplayModifyGroceryListMenu():
    print '--------------------------'
    print '    Modify Grocery List   '
    print '--------------------------'
    print '1) Add an ingredient'
    print '2) Remove an ingredient'
    print '3) Remove staples'
    print '(e)xit to grocery list menu' #TODO verify that's where this goes
    return

def ModifyGroceryList(global_state, grocery_list):
    '''
    Allow user to modify the grocery list
    '''
    DisplayModifyGroceryListMenu()
    while True:
        selection = raw_input('> ')
        if selection == 'e' or selection == 'E':
            break
        elif selection == '1':
            grocery_list = AddIngredientToGroceryListMenu(global_state, grocery_list)
        elif selection == '2':
            grocery_list = RemoveIngredientFromGroceryListMenu(global_state, grocery_list)
        elif selection == '3':
            grocery_list = RemoveCommonIngredients(grocery_list)
    return grocery_list

def RemoveIngredientFromGroceryListMenu(global_state, grocery_list):
    grocery_list = Common.RemoveItem(grocery_list, 'an ingredient', 'ingredients', ListGroceryIngredients, DisplayModifyGroceryListMenu, False, False)
    return grocery_list

def ListGroceryIngredients(command, grocery_list):
    Common.ListItem(command, grocery_list)
    return
