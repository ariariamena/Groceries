#Classes

import pickle
import copy
import datetime



class RestrictionProfile:
    def __init__(self, name = '', restrictions=[], banned_ingredients=[], banned_recipes=[]):
        '''
        --------------
        Parameters:
        --------------
        name : str
            Name of the restriction profile
        restrictions : list[RestrictionProfile]
            Sublist of restriction profiles
        banned_ingredients : list[Ingredient]
            List of banned ingredients
        banned_recipes : list[Recipe]
            List of banned recipes
        '''
        self.name = name
        self.restrictions = restrictions
        self.banned_ingredients = banned_ingredients
        self.banned_recipes = banned_recipes
    def __str__(self):
        my_str='Restriction Profile '+self.name+'\n\tRestrictions: '
        if len(self.restrictions) > 0:
            my_str += ', '.join([r for r in self.restrictions])
        my_str += '\n\tBanned Ingredients: '
        if len(self.banned_ingredients) > 0:
            my_str += ', '.join([b.name for b in self.banned_ingredients])
        my_str += '\n\tBanned Recipes: '
        if len(self.banned_recipes) > 0:
            my_str += ', '.join([r.name for r in self.banned_recipes])
        return my_str
    def __eq__(self, other):
        return type(self) == type(other) and self.name.lower() == other.name.lower()

class HistEntry:
    def __init__(self, recipes = [], date = datetime.date.today()):
        '''
        HistEntry is a single history entry
        recipes : list[Recipe]
            Recipes chosen on that date
        date : datetime.date
            Date the recipes were chosen
        '''
        self.recipes = recipes
        self.date = date
    def __str__(self):
        return str(self.date)+':\n'+'\n'.join([r.name for r in self.recipes])
    def __cmp__(self, other):
        return self.date > other.date

class History:
    def __init__(self, entries = []):
        self.entries = entries
    def AddEntry(self, entry):
        self.entries.append(entry)
    def AddRecipes(self, recipes):
        self.entries.append(HistEntry(recipes))
    def GetLastRecipes(self):
        if len(self.entries) == 0:
            return []
        return max(self.entries).recipes

class GlobalState:
    def __init__(self, all_recipes = [], all_ingredients = [], history = History(),
            quick_meals = False, do_dessert = False, do_snacks = False, num_days = 7,
            restriction_profiles=[]):
        self.all_recipes = all_recipes
        self.all_ingredients = all_ingredients
        self.history = history
        self.quick_meals = quick_meals
        self.do_dessert = do_dessert
        self.do_snacks = do_snacks
        self.num_days = num_days
        self.restriction_profiles = restriction_profiles
        if restriction_profiles == []:
            self.DefaultRestrictionProfiles()
        self.chefs = ['Emily','Jason']

    def __str__(self):
        self_str = "------ Global State -------"
        self_str += "\nRecipes : " +", ".join([x.name for x in self.all_recipes])
        self_str += "\nIngredients : " +", ".join([x.name for x in self.all_ingredients])
        self_str += "\nHistory : " +str(self.history)
        self_str += "\nQuick Meals : " +str(self.quick_meals)
        self_str += "\nDo Dessert : " +str(self.do_dessert)
        self_str += "\nDo Snacks : " +str(self.do_snacks)
        self_str += "\nNumber of Days : " +str(self.num_days)
        self_str += "\nRestriction Profiles : " + ", ".join([x.name for x in self.restriction_profiles])
        self_str += "\nChefs : " +str(self.chefs)

        return self_str

    def NumServings(self):
        return self.num_days*2

    def DefaultRestrictionProfiles(self):
        print("setting default restriction profiles")
        self.restriction_profiles.append(RestrictionProfile('Fatty'))
        self.restriction_profiles.append(RestrictionProfile('Meat'))
        self.restriction_profiles.append(RestrictionProfile('Beef'))
        self.restriction_profiles.append(RestrictionProfile('Dairy'))
        self.restriction_profiles.append(RestrictionProfile('Nuts'))
        self.restriction_profiles.append(RestrictionProfile('Fish'))
        self.restriction_profiles.append(RestrictionProfile('Soy'))
        return



global_state = GlobalState()
#Load and Save Functions

def GetGlobalState():
    global global_state
    return global_state

def SetGlobalState(state):
    global global_state
    global_state = state
    return

def LoadState(global_state, current_chefs, file_name='GroceryState.grc'):
    '''
    Load the global state, which includes the master ingredient list, master recipe list, total restrictions, and history of recipes used. Use pickle to serialize
    '''
    try:
        state_file = open(file_name,"r")
        global_state = pickle.load(state_file)
        if global_state.restriction_profiles == []:
            global_state.DefaultRestrictionProfiles()
        if global_state.history == []:
            global_state.history = History()
        print "Loading file "
        print str(global_state)
        state_file.close()
    except Exception as e:
        print "An exception occured in LoadState : "+str(e)
        return
    SetDefaultsOnLoad(global_state, current_chefs)
    return global_state

def LoadDifferentState(global_state): #TODO
    return
def SetDefaultsOnSave(global_state): #TODO
    '''
    Reset state parameters to defaults for saving
    '''
    global_state.quick_meals = False
    global_state.do_dessert = False
    global_state.do_snacks = False
    global_state.num_days = 7
    return

def SetDefaultsOnLoad(global_state, current_chefs):
    '''
    Set defaults in load
    '''
    global_state.chefs = ['Emily','Jason'] #TODO there is a bug in here
    current_chefs = global_state.chefs #TODO etc
    return

def SaveState(global_state, file_name = 'GroceryState.grc'):
    '''
    Serialize and save the global state
    '''
    SetDefaultsOnSave(global_state)
    state_file = open(file_name,"w+")
    pickle.dump(global_state, state_file)
    state_file.close()
    return

def ValidFilename(file_name):
    return True

def FileNamePrompt():
    '''
    Explain the criteria for a correct file name
    '''
def SaveAsMenu(global_state):
    '''
    Menu for saving a new file
    '''
    print "File name: (hit 'c' for cancel)"
    while True:
        selection = raw_input('> ')
        if selection == 'c' or selection == 'C':
            break
        elif len(selection > 0) and ValidFilename(selection):
            SaveState(global_state, selection+".grc")
            SaveState(global_state) #The file that loads should be the last one modified
            break
        else:
            print "Invalid file name."
            print FileNamePrompt()
    DisplayMainMenu()
    return

#List Add Functions
def AddItem(the_list, name, name_plural, list_func, current_global_list, search_by_name_func):
    '''
    Add item to a provided list

    Parameters:
        list : list
            List to add the item to
        name : str
            Name of the type of object for the prompt.  Should be of the form <article> <type name>
         name_plural : str
            Name of the type of object in plural form for the prompt
        list_func : function
            Function that lists the available objects of that type
        current_global_list : list
            Global list of that object type
        search_by_name_func : function
            Function that searches for that object by name
    '''
    global global_state
    print 'Enter a name of'+name+'.'
    print 'If you need to see a list of '+name_plural+', type "list" followed by a filter.'
    print "Or, to go back to the previous menu, type 'e'"
    while True:
        selection = raw_input('> ')
        if selection == 'e' or selection == 'E':
            break
        elif selection.lower()[0:4] == 'list':
            list_func(selection, current_global_list)
        elif selection in [r.name for r in current_global_list]:
            r = search_by_name_func(selection, current_global_list)
            if r:
                the_list.append(r)
                break
        else:
            print selection + " not found."
    return the_list
#List Edit Functions
def EditItemMenu(name, name_plural, parent_menu_name, search_by_name_func, current_global_list, edit_item_func, display_parent_menu):
    '''
    Obtain an item to edit and edit it

    Parameters:
        name : str
            Name of item type for prompt
        name_plural : str
            Name of item type in plural for prompts
        parent_menu_name : str
            Name of parent menu
        search_by_name_func : function
            Function that searches for the item by name
        current_global_list : list
            List containing this item
        edit_item_func : function
            Function editing this item
        display_parent_menu : function
            Function that displays the parent menu to this one
    '''
    print 'Name the ' + name + ' you would like to edit.'
    print 'For a list of ' + name_plural + ', type "list" plus any applicable filter'
    print "Or to go back to the " + parent_menu_name + " menu, type 'e'"
    while True:
        selection = raw_input('> ')
        if selection == 'e' or selection == 'E':
            break
        elif selection[0:4] == 'list':
            ListItem(selection, current_global_list)
        else:
            item = search_by_name_func(selection, current_global_list)
            if item:
                new_item = edit_item_func(item)
                if new_item != None:
                    log("Replacing item with " + str(new_item))
                    current_global_list = ReplaceItem(new_item, current_global_list)
                break
            else:
                print selection + " not found."
    display_parent_menu()
    return current_global_list

def ReplaceItem(item, current_global_list):
    log(" current global list before replacement " + str(current_global_list))
    current_global_list = [i if i.name != item.name else item for i in current_global_list]
    log(" current global list after replacement " + str(current_global_list))
    return current_global_list

#List Remove Functions
def RemoveItem(the_list, name, name_plural, list_func, previous_menu, global_list = True, confirm = True):
    '''
    Add item to a provided list

    Parameters:
        list : list
            List to add the item to
        name : str
            Name of the type of object for the prompt.  Should be of the form <article> <type name>
         name_plural : str
            Name of the type of object in plural form for the prompt
        list_func : function
            Function that lists the available objects of that type
        search_by_name_func : function
            Function that searches for that object by name
    '''
    global global_state
    print 'Enter a name of'+name+' to remove.'
    print 'If you need to see a list of '+name_plural+', type "list" followed by a filter.'
    print "Or, to go back to the previous menu, type 'e'"
    while True:
        selection = raw_input('> ')
        if selection == 'e' or selection == 'E':
            break
        elif selection.lower()[0:4] == 'list':
            if global_list:
                list_func(selection)
            else:
                list_func(selection, the_list)
        elif selection in [r.name for r in the_list]:
            for r in the_list:
                if r.name == selection:
                    if confirm:
                        print 'You have chosen to remove the following ' + name.split(" ")[1]
                        print str(r)
                        print 'Confirm your choice (y/n):'
                        while True:
                            selection = raw_input('> ')
                            if selection.lower() == 'y':
                                the_list.remove(r)
                                break
                            elif selection.lower() == 'n':
                                break
                    else:
                        the_list.remove(r)
                    break
            break
        else:
            print selection + " not found."
    previous_menu()
    return the_list

#List List Functions

def ListItem(command, the_list, separator = '\n'):
    '''
    Print a list according to a provided filter

    Parameters:
    command : str
        command of the format 'list <x>', where x is a filter of the start of the word
    '''
    filter = command[5:]
    alphabetical_members = sorted(the_list, key=lambda x: x.name)
    if  len(command) < 6:
        filtered_members = [x.name for x in alphabetical_members]

    else:
        filtered_members = [x.name for x in alphabetical_members if x.name[0:len(filter)]==filter]
    print separator.join(filtered_members)
    return

def SearchItemByName(name, the_list):
    '''
    Search a list for an item by name
    '''
    for x in the_list:
        if x.name.lower() == name.lower():
            return x
    return None

def PromptForName(item_type, object_list):
    print 'Give this ' + item_type + ' a name.'
    name = ''
    while True:
        name = raw_input('> ')
        if name.lower() in [x.name.lower() for x in object_list]:
            print name + ' already in use. Please provide another name:'
            continue
        break
    return name

def PromptParameterString(type_name, parameter_name, validity_func, validity_prompt, default = False): #TODO, check for already existing thing somewhere.
    print "Give " + type_name + " " + parameter_name + "."
    print "Press 'c' to cancel, or 'b' to go back."
    if default:
        print "Press 'd' to accept the default or current value"
    while True:
        selection = raw_input('> ')
        if selection.lower() == 'c' or selection.lower() == 'b':
            return selection
        elif default == True and selection.lower() == 'd':
            return selection
        elif len(selection) > 0 and validity_func(selection):
            return selection
        else:
            print "Invalid input."
            print validity_prompt()

def PromptParameterMultiple(type_name, prompt_type, parameter_name, validity_func = None, validity_prompt = None, default = False):
    print 'Would you like to add ' + parameter_name + ' to this ' + type_name + " (y/n)?"
    print '(c)ancel, (b)ack'
    parameters = []
    while True:
        selection = raw_input('> ')
        if selection.lower() == 'f' or selection.lower() == 'n':
            break
        elif selection.lower() == 'b' or selection.lower() == 'c':
            return selection
        elif selection.lower() == 'y':
            if prompt_type == 'string':
                parameters.append(PromptParameterString(type_name, parameter_name, validity_func, validity_prompt, default))
            else:
                parameters.append(PromptParameterYesNo(type_name, parameter_name, default))
            print 'Would you like to add ' + parameter_name + ' to this ' + type_name + " (y/n)?"
            print '(c)ancel, (b)ack'
    return parameters


def PromptParameterYesNo(type_name, parameter_name, default = False):
    print "Is this " + type_name + " " + parameter_name + "? (y/n)"
    print "Press 'c' to cancel, or 'b' to go back."
    if default:
        print "Press 'd' to accept the default or current value"
    while True:
        selection = raw_input('> ')
        if selection.lower() == 'c' or selection.lower() == 'b':
            return selection
        elif default == True and selection.lower() == 'd':
            return selection
        elif selection.lower() == 'y':
            return True
        elif selection.lower() == 'n':
            return False
        else:
            continue
def ValidBool(val):

    if val == '1' or val == '0':
        return True
    print val + " len: "+str(len(val))
    return False

def PromptValidBool():
    print "Use 1 for True, 0 for False"

def ValidNum(num):
    try:
        float(num)
        return float(num) > 0
    except ValueError:
        return False

def PromptValidNum():
    print "Provide a number greater than 0"

def log(string_to_log):
    print str(string_to_log)
