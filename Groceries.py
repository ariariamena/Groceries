import pickle
import copy
import Ingredients
import Recipe
import Selector
import History
import GroceryList
import Restrictions
import Common

'''
GLOBAL TODOs:
Make it so that all the PromptValid functions take selection as an argument and list the options that match your guess
Make it so a restriction profile can ban a recipe CHECK
Make it so that a menu shows up after all user input
Deal with RemoveItem function when you aren't using a global list
Make it so create ingredient/recipe functions can be done in sequence or one by one
Make it so you can have multiple chefs
Make it so quantity is not restrictive and can be a float
Incorporate meal_type properly
'''

#Currently selected stuff for this week
current_recipes = []
current_restrictions = []
current_chefs = []
ingredients_to_use = []
banned_ingredients = []
grocery_list = []

def RecordHistory(): # TODO
    '''
    Record new historical information
    '''
    return

def DisplayEditCurrentRecipesMenu():
    print '1) Add a recipe'
    print '2) Remove a recipe'
    print '3) See current recipes'
    print '(e)xit to previous menu'
    return

def EditCurrentRecipesMenu():
    global current_recipes
    DisplayEditCurrentRecipesMenu()
    while True:
        selection = raw_input('> ')
        if selection.lower() == 'e':
            break
        elif selection == '1':
            Common.log("Current recipes before: "+'\n'.join([r.name for r in current_recipes]))
            current_recipes = Common.AddItem(current_recipes, 'a recipe', 'recipes', Recipe.ListRecipes, Common.global_state.all_recipes, Recipe.RecipeByName)
            Common.log("Current recipes after: "+'\n'.join([r.name for r in current_recipes]))
        elif selection == '2':
            Common.RemoveItem(current_recipes, 'a recipe', 'recipes', Recipe.ListRecipes, DisplayEditCurrentRecipesMenu, False, False)
        elif selection == '3':
            print '\n'.join([r.name for r in current_recipes])
    return

def DisplaySuggestRecipeMenu():
    print '1) This looks good'
    print '2) Modify manually'
    print '3) Remove some suggestions and fill in remainder automatically'
    print '4) Give all new suggestions'
    print '(e)xit to previous menu'
    return

def SuggestRecipes(menu_func = None): #TODO
    '''
    Suggest a set of candidate Recipes based on global state
    '''

    global current_chefs
    global current_recipes
    global current_restrictions
    global ingredients_to_use
    global banned_ingredients

    suggestions = Selector.SuggestRecipes(Common.global_state, current_recipes, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, Common.global_state.history)
    print 'How does this look?'
    for s in suggestions:
        print '\t' + s.name
    DisplaySuggestRecipeMenu()
    while True:
        selection = raw_input('> ')
        if selection == 'e' or selection == 'E':
            break
        elif selection == '1':
            current_recipes = suggestions
            GenerateList()
            History.Update(current_recipes)
            break
        elif selection == '2':
            current_recipes = suggestions
            EditCurrentRecipesMenu()
            break
        elif selection == '3':
            EditCurrentRecipesMenu()
            SuggestRecipes()
            break
        elif selection == '4':
            SuggestRecipes()
            break
    #TODO figure out what menu to show
    print "done"
    if menu_func:
        menu_func()
    return

def GenerateList(): #TODO
    '''
    Generate a grocery list based on the chosen recipes
    '''
    global current_recipes
    global grocery_list
    if len(current_recipes) == 0:
        print 'Error: No recipes chosen.'
        return None
    grocery_list = GroceryList.MakeGroceryList(current_recipes)
    return grocery_list

def PrintGroceryList(): #TODO
    '''
    Print the current grocery list, or generate a new one if there isn't one.
    '''
    global grocery_list
    if grocery_list == []:
        GenerateList()
    print GroceryList.ListToString(grocery_list)
    return

def Banner():
    '''
    Display the welcome banner
    '''
    print '*************************************'
    print '***          GROCERIES            ***'
    print '*************************************'
    print 'Welcome to the grocery list selector.'
    print 'What would you like to do?'
    return

def DaysToCookMenu():
    '''
    Set number of days you need to cook
    '''

    print "How many days do you need to cook for?"
    while True:
        selection = raw_input('> ')
        if selection.isdigit():
            selection = int(selection)
            if selection > 0:
                Common.global_state.num_days = int(selection)
                DisplayOptionsMenu()
                break
            else:
                continue
    return


def AddRecipeToCurrentRecipes():
    '''
    Set a recipe manually
    '''

    global current_recipes
    Common.AddItem(current_recipes, "a recipe", "recipes", Recipe.ListRecipes, Common.global_state.all_recipes, Recipe.RecipeByName)
    DisplayOptionsMenu()
    return

def IngredientsToUseMenu():
    '''
    Declare ingredients that need to be used up
    '''
    global ingredients_to_use
    Common.AddItem(ingredients_to_use, 'an ingredient to use up', 'ingredients', Ingredients.ListIngredients, Common.global_state.all_ingredients, Ingredients.IngredientByName)
    DisplayOptionsMenu()
    return


def ListCurrentRestrictions():
    global current_restrictions
    print "Current restrictions:"
    for r in current_restrictions:
        print r.name
    return

def RemoveCurrentRestriction(name):
    global current_restrictions
    for r in current_restrictions:
        if r.name == name:
            current_restrictions.remove(r)
    return



def RemoveChef(name):
    global current_chefs
    current_chefs.remove(name)
    return


def DisplayOutOfTownMenu():
    print 'Who is out of town?'
    print '1) Emily'
    print '2) Jason'
    print '3) Cancel'

def OutOfTownMenu():
    DisplayOutOfTownMenu()
    while True:
        selection = raw_input('> ')
        if selection == '3':
            break
        elif selection == '1':
            RemoveCurrentRestriction('Emily')
            RemoveChef('Emily')
            break
        elif selection == '2':
            RemoveCurrent('Jason')
            RemoveChef('Jason')
            break

def DisplayOptionsMenu():
    '''
    Display Options Menu
    '''
    print '--------------------------'
    print '      Options Menu        '
    print '--------------------------'
    print '1) Number of days to cook'
    print '2) Special request'
    print '3) Tell me about ingredients you need to get rid of'
    print '4) Set dietary restrictions'
    print '5) Need quick meals'
    print "6) Someone's out of town"
    print '7) Add dessert'
    print '8) Add snacks'
    print '(e)xit to main menu'
    return

def OptionsMenu():
    '''
    Do options menu
    '''

    global current_restrictions
    DisplayOptionsMenu()
    while True:
            selection = raw_input('> ')
            print selection
            if selection == 'e' or selection == 'E':
                break
            try:
                selection = int(selection)
            except Exception as e:
                continue
            if selection == 1:
                DaysToCookMenu()
            elif selection == 2:
                AddRecipeToCurrentRecipes()
                DisplayOptionsMenu()
            elif selection == 3:
                IngredientsToUseMenu()
            elif selection == 4:
                Restrictions.DietaryRestrictionsMenu(Common.global_state, current_restrictions, DisplayOptionsMenu)
            elif selection == 5:
                Common.global_state.quick_meals = True
            elif selection == 6:
                OutOfTownMenu()
            elif selection == 7:
                Common.global_state.do_dessert = True
            elif selection == 8:
                Common.global_state.do_snacks = True
            else:
                continue
    return

def ImportIngredientsRecipes():
    ingrs = []
    try:
        ingr_file = open('ingredients.txt','r')
        ingrs = ingr_file.readlines()
        ingr_file.close()

    except Exception as e:
        print "Error, could not read ingredient import file\n" + str(e)
    if ingrs != []:
        Ingredients.ImportIngredients(ingrs)
    recs = []
    try:
        rec_file = open('recipes.csv','r')
        recs = rec_file.readlines()
        rec_file.close()
    except Exception as e:
        print "Error, could not read recipe import file\n" + str(e)
    if recs != []:
        Recipe.ImportRecipes(recs)
    return


def DisplayAddEditRecipesIngredientsMenu():
    print '--------------------------'
    print '      Add/Edit Menu       '
    print '--------------------------'
    print '1) Create an Ingredient'
    print '2) Create a Recipe'
    print '3) Modify an Ingredient'
    print '4) Modify a Recipe'
    print '5) List all Ingredients'
    print '6) List all Recipes'
    print '7) Remove an Ingredient'
    print '8) Remove a Recipe'
    print '9) Import Ingredients and Recipes from File'
    print '(e)xit to previous menu'

def AddEditRecipesIngredientsMenu():
    '''
    Menu for adding or modifying recipes or ingredients
    '''

    print "GLobal Statee"
    print str(Common.global_state)

    DisplayAddEditRecipesIngredientsMenu()
    while True:
        selection = raw_input('> ')
        if selection == 'e' or selection == 'E':
            break
        elif selection == '1':
            new_ingredient = Ingredients.CreateNewIngredient()
            if new_ingredient:
                print "Adding ingredient "+new_ingredient.name
                Common.global_state.all_ingredients.append(new_ingredient)
                print str(Common.global_state)
            DisplayAddEditRecipesIngredientsMenu()
        elif selection == '2':
            new_recipe = Recipe.CreateNewRecipe()
            if new_recipe:
                Common.global_state.all_recipes.append(new_recipe)
            DisplayAddEditRecipesIngredientsMenu()
        elif selection == '3':
            Ingredients.EditIngredientMenu(DisplayAddEditRecipesIngredientsMenu)
            DisplayAddEditRecipesIngredientsMenu()
        elif selection == '4':
            Recipe.EditRecipeMenu(DisplayAddEditRecipesIngredientsMenu)
            DisplayAddEditRecipesIngredientsMenu()
        elif selection == '5':
            Ingredients.ListIngredients('list ')
        elif selection == '6':
            Recipe.ListRecipes('list ')
        elif selection == '7':
            Ingredients.RemoveIngredientMenu(DisplayAddEditRecipesIngredientsMenu)
        elif selection == '8':
            Recipe.RemoveRecipeMenu(DisplayAddEditRecipesIngredientsMenu)
        elif selection == '9':
            ImportIngredientsRecipes()

    DisplayMainMenu()
    return

def AddEditHistoryMenu():
    '''
    Menu for adding or modifying history
    '''
    return

def DisplayMainMenu():
    '''
    Display the main menu
    '''
    print '--------------------------'
    print '        Main Menu         '
    print '--------------------------'
    print '1) Suggest recipes'
    print '2) Print current grocery list'
    print '3) Options'
    print '4) Manually modify current grocery list'
    print '5) Add/modify ingredients or recipes'
    print '6) Add/modify history'
    print '7) Load different file'
    print '8) Save'
    print '9) Save as'
    print '(q)uit'

def Main():
    '''
    Do prompts and menus
    '''
    global grocery_list
    global current_chefs
    Banner()
    Common.global_state = Common.LoadState(Common.global_state, current_chefs) #TODO won't change current_chefs. Might not need it to
    current_chefs = copy.copy(Common.global_state.chefs)
    while True:
        DisplayMainMenu()
        selection = raw_input('> ')
        if selection == '1':
            SuggestRecipes()
        elif selection == '2':
            PrintGroceryList()
        elif selection =='3':
            OptionsMenu()
        elif selection == '4':
            grocery_list = GroceryList.ModifyGroceryList(Common.global_state, grocery_list)
        elif selection == '5':
            AddEditRecipesIngredientsMenu()
        elif selection == '6':
            AddEditHistoryMenu()
        elif selection == '7':
            Common.LoadDifferentState(Common.global_state)
        elif selection == '8':
            Common.SaveState(Common.global_state)
        elif selection == '9':
            Common.SaveAsMenu(Common.global_state)
        elif selection == 'q':
            break
        else:
            continue

if __name__ == "__main__":
    Main()
