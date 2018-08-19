import Common
import Recipe
import Ingredients
import copy

def DisplayDietaryRestrictionsMenu():
    #TODO See current restrictions, Remove restrictions
    print '--------------------------'
    print ' Dietary Restrictions Menu'
    print '--------------------------'
    print '1) Low fat'
    print '2) Low beef'
    print '3) No meat'
    print '4) No dairy'
    print '5) No nuts'
    print '6) No fish/shellfish'
    print '7) No soy'
    print '8) No spicy foods'
    print '9) Ban other ingredient'
    print '10) Remove restriction'
    print '11) Choose restriction profile'
    print '12) Create restriction profile'
    print '13) Edit restriction profile'
    print '(e)xit to options menu'
    return

#Restriction Profiles
def DisplayCreateRestrictionProfileMenu():
    print '--------------------------'
    print ' Restriction Profile Menu '
    print '--------------------------'
    print '1) Add a restriction'
    print '2) Ban an ingredient'
    print '3) Ban a recipe'
    print '(s)ave profile'
    print '(c)ancel'

def CreateRestrictionProfile(global_state):
    DisplayCreateRestrictionProfileMenu()
    restriction_profile = Common.RestrictionProfile()
    while True:
        selection = raw_input('> ')
        if selection == 'c' or selection == 'C':
            DisplayDietaryRestrictionsMenu()
            return None
        elif selection == 's' or selection == 'S':
            name = Common.PromptForName('restriction profile', global_state.restriction_profiles)
            if len(name) > 0:
                restriction_profile.name = name
            break
        elif selection == '1':
            restriction_profile = AddRestrictionMenu(restriction_profile, DisplayCreateRestrictionProfileMenu)
        elif selection == '2':
            restriction_profile = BanIngredientMenu(restriction_profile)
        elif selection == '3':
            restriction_profile = BanRecipeMenu(restriction_profile)
    print 'The following profile has been created: '
    print str(restriction_profile)
    print 'Would you like to save it (y/n)'
    while True:
        selection = raw_input('> ')
        if selection == 'y' or selection == 'Y':
            global_state.restriction_profiles.append(restriction_profile)
            break
        elif selection == 'n' or selection == 'N':
            break
    DisplayDietaryRestrictionsMenu()
    return

def DisplayAddRestrictionMenu():
    print '--------------------------'
    print ' Restriction Profile Menu '
    print '--------------------------'
    print '1) Low fat'
    print '2) Low beef'
    print '3) No meat'
    print '4) No dairy'
    print '5) No nuts'
    print '6) No fish/shellfish'
    print '7) No soy'
    print '8) No spicy food'
    print '(e)xit to Dietary Restrictions Menu'


def AddRestrictionMenu(restriction_profile,prev_menu):
    DisplayAddRestrictionMenu()
    while True:
        selection = raw_input('> ')
        if selection == 'e' or selection == 'E':
            break
        if selection == '1':
            restriction_profile.restrictions.append(Common.RestrictionProfile('Fatty'))
        if selection == '2':
            restriction_profile.restrictions.append(Common.RestrictionProfile('Beef'))
        if selection == '3':
            restriction_profile.restrictions.append(Common.RestrictionProfile('Meat'))
        if selection == '4':
            restriction_profile.restrictions.append(Common.RestrictionProfile('Dairy'))
        if selection == '5':
            restriction_profile.restrictions.append(Common.RestrictionProfile('Nuts'))
        if selection == '6':
            restriction_profile.restrictions.append(Common.RestrictionProfile('Fish'))
        if selection == '7':
            restriction_profile.restrictions.append(Common.RestrictionProfile('Soy'))
        if selection == '8':
            restriction_profile.restrictions.append(Common.RestrictionProfile('Spicy'))

    prev_menu()
    return restriction_profile

def BanIngredientMenu(profile = None): #TODO fix so that this works with global banned ingredients
    '''
    Declare ingredients that should be banned under a restriction profile
    '''
    try:
        new_profile = copy.copy(profile)
    except Exception as e:
        new_profile = None
    global banned_ingredients
    ban_list = banned_ingredients
    if profile:
        ban_list = new_profile.banned_ingredients
    Common.AddItem(ban_list, 'an ingredient to ban', 'ingredients', Ingredients.ListIngredients, Common.global_state.all_ingredients, IngredientByName)
    DisplayDietaryRestrictionsMenu() # TODO display correct menu
    return profile

def BanRecipeMenu(profile = None):
    '''
    Declare recipes that will be banned under a restriction profile
    '''
    try:
        new_profile = copy.copy(profile)
    except Exception as e:
        new_profile = None
    if profile == None:
        return None
    ban_list = new_profile.banned_recipes
    Common.AddItem(ban_list, 'a recipe to ban', 'recipes', Recipe.ListRecipes, Common.global_state.all_recipes, RecipeByName)
    DisplayDietaryRestrictionsMenu() # TODO display correct menu
    return profile

def EditRestrictionProfileMenu(global_state):
    Common.EditItemMenu('a restriction profile', 'restriction profiles','dietary restrictions menu',
        SearchRestrictionProfileByName, global_state.restriction_profiles, EditRestrictionProfile, DisplayDietaryRestrictionsMenu)
    return

def DisplayEditRestrictionMenu():
    print '--------------------------'
    print ' Edit Dietary Restriction '
    print '      Profile Menu        '
    print '--------------------------'
    print '1' #TODO

def ChooseRestrictionProfile(global_state, current_restrictions):
    Common.AddItem(current_restrictions, 'a restriction', 'restrictions', Restrictions.ListRestrictions, global_state.restriction_profiles, RestrictionByName)
    return


def DietaryRestrictionsMenu(global_state, current_restrictions, prev_menu):
    '''
    Set Dietary Restrictions
    '''
    DisplayDietaryRestrictionsMenu()
    while True:
        selection = raw_input('> ')
        if selection == 'e' or selection == 'E':
            break
        elif selection == '1':
            current_restrictions.append(Common.RestrictionProfile("Fatty"))
        elif selection == '2':
            current_restrictions.append(Common.RestrictionProfile("Beef"))
        elif selection == '3':
            current_restrictions.append(Common.RestrictionProfile("Meat"))
        elif selection == '4':
            current_restrictions.append(Common.RestrictionProfile("Dairy"))
        elif selection == '5':
            current_restrictions.append(Common.RestrictionProfile("Nuts"))
        elif selection == '6':
            current_restrictions.append(Common.RestrictionProfile("Fish"))
        elif selection == '7':
            current_restrictions.append(Common.RestrictionProfile("Soy"))
        elif selection == '8':
            current_restrictions.append(Common.RestrictionProfile("Spicy"))
        elif selection == '9':
            BanIngredientMenu()
        elif selection == '10':
            RemoveRestrictionMenu()
        elif selection == '11':
            ChooseRestrictionProfile()
        elif selection == '12':
            CreateRestrictionProfile(global_state)
        elif selection == '13':
            EditRestrictionProfile()
    prev_menu()
    return

def EditRestrictionProfile():
    DisplayEditRestrictionMenu()
    #TODO
    return

def RemoveRestrictionMenu(global_state, current_restrictions):
    Common.RemoveItem(current_restrictions, 'a restriction', 'restrictions', ListCurrentRestrictions, global_state)
    DisplayDietaryRestrictionsMenu()
    return

def ListRestrictions(command, global_state):
    Common.ListItem(command,global_state.restriction_profiles)
    return

def RestrictionByName(name, restrictions=[]):
    res_copy = copy.deepcopy(restrictions)
    if len(res_copy) == 0:
        res_copy = Common.global_state.restriction_profiles
    return Common.SearchItemByName(name, res_copy)

def SearchRestrictionProfileByName(restriction_profiles, name):
    return Common.SearchItemByName(name, restriction_profiles)
