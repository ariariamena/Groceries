import Common
import copy

valid_locations = ['Produce:Front', 'Produce:LeftSide', 'Produce:Asian', 'Produce:Middle', 'Produce:Herbs',
    'Produce:Back', 'Produce:RightSide', 'Produce', 'Cheese', 'Meat', 'Fish',
    'Bakery', 'Back:ButterAndCheese', 'Back:Yogurt', 'WholeNuts', 'GF', 'Frozen','Frozen:Vegetable','Frozen:IceCream'
    'Frozen:Fruit', 'Pharmacy', 'International','International:Canned', 'International:Mexican',
    'International:Indian','International:EastAsian', 'Pasta', 'Tomato', 'Rice', 'Soup', 'Condiments','Baking', 'Snacks',
    'Cereal', 'PBJ', 'Juice', 'Alcohol', 'MilkAndEggs','TP', 'Detergents', 'SchoolSupplies','Other']

valid_meat_types = ['beef', 'chicken', 'turkey', 'pork', 'fish','eggs','mutton']

valid_units = ['cup', 'cups', 'Tbs', 'tsp', 'box', 'bag', '', 'bunch', 'unit', 'oz','can','cans','bottle','pint','quart','half-gallon', 'gallon']
#TODO finish this up
class Ingredient:
    def __init__(self, name='', location='Other', staple=False, seasons='sufw',
        perishable=False, family_pack=False, quantity = 0, unit = '', store_quantity = 1, meat_type = ''):
        '''
        Parameters:
        name : str
            Ingredient name
        location : str
            Location in grocery store. Valid options are:

        staple : bool
            Is this a staple around our house or do we buy it every time?
        seasons : str
            string containing seasons that the ingredient is available
            s = spring
            u = summer
            f = fall
            w = winter
        perishable : bool
            Will this item perish in less than a week?
        family_pack : bool
            Is this item a family pack item that needs to be spread across multiple dishes?
        '''
        self.name=name
        self.staple=staple
        self.seasons=seasons
        self.perishable=perishable
        self.location=location
        self.family_pack=family_pack
        #For recipes
        self.quantity = quantity
        self.unit = unit
        self.store_quantity = store_quantity
        self.meat_type = meat_type

    def __str__(self):
        border = int((24-len(self.name))/2)
        self_string = '-'*border + self.name + '-'*border
        self_string += "\nLocation : " + self.location
        self_string += "\nStaple : " + str(self.staple)
        self_string += "\nPerishable : " + str(self.perishable)
        self_string += "\nSeasons : " + str(self.seasons)
        self_string += "\nFamily Pack : " + str(self.family_pack)
        return self_string

    def __eq__(self, other):
        return type(self) == type(other) and self.name.lower() == other.name.lower()
    def __cmp__(self, other): # Determine location ordering
        if type(self) != type(other):
            return cmp(self, Ingredient())
        return cmp(self.GroceryStoreValue(), other.GroceryStoreValue())

    def GroceryStoreValue(self):
        global valid_locations
        vl = [v.lower() for v in valid_locations]
        return vl.index(self.location.lower())

    def GroceryStoreFormatString(self):
        format_str = self.name+"\t"+str(self.quantity)+" "+self.unit
        if self.store_quantity > 1:
            format_str += " x"+str(self.store_quantity)
        return format_str

def PromptIngrParameterString(parameter_name, validity_func, validity_prompt, default = False):
    return Common.PromptParameterString('ingredient', parameter_name, validity_func, validity_prompt, default)

def PromptIngrParameterYesNo(parameter_name, default = False):
    return Common.PromptParameterYesNo('ingredient', parameter_name, default)

def PromptIngrParameterInt(parameter_name, default = False):
    return Common.PromptParameterString('ingredient',parameter_name, Common.ValidNum, Common.PromptValidNum, default)


def ValidName(name): #TODO
    if name.lower() in [i.name.lower() for i in Common.global_state.all_ingredients]:
        return False
    return True

def PromptValidName(): #TODO
    print 'Name already chosen.  Choose a different name.'
    return

def PromptIngrName(ingredient):
    name = PromptIngrParameterString('a name', ValidName, PromptValidName)
    if name.lower() == 'c':
        return None
    elif name.lower() == 'b':
        ingredient = PromptIngrName(ingredient)
    else:
        ingredient.name = name
        ingredient = PromptIngrLocation(ingredient)
    return ingredient

def ValidLocation(location): #TODO
    global valid_locations
    if location in valid_locations:
        return True
    else:
        return False

def PromptValidLocation(): #TODO
    print "Invalid location.  Valid locations are:"
    print ", ".join(valid_locations)
    return ''

def PromptIngrLocation(ingredient):
    location = PromptIngrParameterString('a grocery store location', ValidLocation, PromptValidLocation)
    if location.lower() == 'c':
        return None
    elif location.lower() == 'b':
        ingredient = PromptIngrName(ingredient)
    else:
        ingredient.location = location
        ingredient = PromptIngrStaple(ingredient)
    return ingredient

def PromptIngrStaple(ingredient):
    staple = PromptIngrParameterYesNo('a staple', True)
    if staple == True or staple == False:
        ingredient.staple = staple
        ingredient = PromptIngrSeasons(ingredient)
    elif staple.lower() == 'd':
        ingredient = PromptIngrSeasons(ingredient)
    elif staple.lower() == 'b':
        ingredient = PromptIngrLocation(ingredient)
    else:
        return ingredient
    return ingredient

def ValidSeasons(seasons): #TODO
    for i in seasons:
        if i not in ['s','u','f','w']:
            return False
    return True

def PromptValidSeasons(): #TODO
    print 'Print a string that includes only the letters (s)pring, s(u)mmer, (f)all, (w)inter. e.g. "sufw".'
    return ''

def PromptIngrSeasons(ingredient):
    seasons = PromptIngrParameterString('seasonal', ValidSeasons, PromptValidSeasons, True)
    if seasons.lower() == 'c':
        return None
    elif seasons.lower() == 'b':
        ingredient = PromptIngrStaple(ingredient)
    elif seasons.lower() == 'd':
        ingredient = PromptIngrPerishable(ingredient)
    else:
        ingredient.seasons = seasons.lower()
        ingredient = PromptIngrPerishable(ingredient)
    return ingredient

def PromptIngrPerishable(ingredient):
    perishable = PromptIngrParameterYesNo('perishable', True)
    if perishable == True or perishable == False:
        ingredient.perishable = perishable
        ingredient = PromptIngrFamilyPack(ingredient)
    elif perishable.lower() == 'd':
        ingredient = PromptIngrFamilyPack(ingredient)
    elif perishable.lower() == 'b':
        ingredient = PromptIngrSeasons(ingredient)
    else:
        return ingredient
    return ingredient

def PromptIngrFamilyPack(ingredient):
    family_pack = PromptIngrParameterYesNo('a family pack', True)
    if family_pack == True or family_pack == False:
        ingredient.family_pack = family_pack
        ingredient = PromptMeatType(ingredient)
    elif family_pack.lower() == 'd':
        ingredient = PromptMeatType(ingredient)
    elif family_pack.lower() == 'b':
        ingredient = PromptIngrPerishable(ingredient)
    else:
        return ingredient
    return ingredient

def ValidMeatType(meat_type):
    if meat_type.lower() in valid_meat_types or meat_type=='':
        return True
    else:
        return False

def PromptValidMeatType():
    print "Valid meat types are: " + ', '.join(valid_meat_types)
    return

def PromptMeatType(ingredient):
    meat_type = PromptIngrParameterYesNo('meat', True)
    if meat_type == True:
        while True:
            meat_type = PromptIngrParameterString('meat type', ValidMeatType, PromptValidMeatType)
            if meat_type.lower() == 'd':
                ingredient = ReviewAndSaveIngredient(ingredient)
                return ingredient
            elif meat_type.lower() == 'b':
                ingredient = PromptIngrPerishable(ingredient)
                return ingredient
            else:
                ingredient.meat_type = str(meat_type).lower()
                ingredient = ReviewAndSaveIngredient(ingredient)
                return ingredient
    elif meat_type == False:
        ingredient = ReviewAndSaveIngredient(ingredient)
    if str(meat_type).lower() == 'd':
        ingredient = ReviewAndSaveIngredient(ingredient)
    elif str(meat_type).lower() == 'b':
        ingredient = PromptIngrPerishable(ingredient)
    return ingredient

def PromptIngrQuantity(ingredient):
    quantity = PromptIngrParameterInt('a quantity') # TODO make a float
    if quantity.lower() == 'b' or quantity.lower() == 'd':
        return ingredient
    elif quantity.lower() == 'c':
        return None
    else:
        ingredient.quantity = float(quantity)
    return ingredient

def ValidUnit(unit):
    ''' All units are valid'''
    return True
def PromptValidUnit():
    print "Valid units are: "
    print ', '.join(valid_units)
    return

def PromptIngrUnit(ingredient):
    unit = PromptIngrParameterString('unit', ValidUnit, PromptValidUnit)
    if unit.lower() == 'c':
        return None
    elif unit.lower() == 'b' or unit.lower() == 'd':
        return ingredient
    else:
        ingredient.unit = unit.lower()
    return ingredient

def ReviewAndSaveIngredient(ingredient):
    print 'You have created the ingredient: '
    print str(ingredient)
    print 'Do you wish to save it? (y/n)'
    while True:
        selection = raw_input('> ')
        if selection.lower() == 'y':
            return ingredient
        elif selection.lower() == 'n':
            return None
    return ingredient

def CreateNewIngredient():
    '''
    Define a new ingredient return it.  Prompts the user with parameters to modify
    '''
    new_ingredient = Ingredient()
    new_ingredient = PromptIngrName(new_ingredient)
    print str(new_ingredient)
    return new_ingredient

def PromptBadImportParameter(ingredient_name, parameter_type, value, prompt_valid):
    print "ImportError: Ingredient " + ingredient_name + " has bad " + parameter_type + ": " + value
    prompt_valid()
    return



def ValidParameters(parameters):
    valid = True
    name = parameters[0]
    if not ValidLocation(parameters[1]):
        valid = False
        PromptBadImportParameter(name, 'location', parameters[1], PromptValidLocation)
    if not Common.ValidBool(parameters[2]):
        valid = False
        PromptBadImportParameter(name, 'staple', parameters[2], Common.PromptValidBool)
    if not ValidSeasons(parameters[3]):
        valid = False
        PromptBadImportParameter(name, 'season', parameters[3], PromptValidSeasons)
    if not Common.ValidBool(parameters[4]):
        valid = False
        PromptBadImportParameter(name, 'perishability', parameters[4], Common.PromptValidBool)
    if not Common.ValidBool(parameters[5]):
        valid = False
        PromptBadImportParameter(name, 'family pack', parameters[5], Common.PromptValidBool)
    if len(parameters) > 6 and not ValidMeatType(parameters[6]):
        valid = False
        print "length of parameters = "+str(len(parameters))
        print "length of parameter 6 = "+str(len(parameters[6]))+"  value = "+hex(ord(parameters[6][0]))
        PromptBadImportParameter(name, 'meat type', parameters[6], PromptValidMeatType)
    return valid

def ImportIngredients(ingr_lines):
    ingr_lines = ingr_lines[1:] #ignore header
    num_added = 0
    for i in ingr_lines:
        parameters = i.replace('\n','').replace('\t',',').replace('\x0d','').split(',')
        if ValidParameters(parameters):
            name = parameters[0]
            location = parameters[1]
            staple = True if parameters[2] == '1' else False
            seasons = parameters[3]
            perishable = True if parameters[4] == '1' else False
            family_pack = True if parameters[5][0] == '1' else False
            meat__type = ''
            if len(parameters) > 6:
                 meat__type = parameters[6].replace('\n','')
            new_ingredient = Ingredient(name, location, staple, seasons, perishable, family_pack, meat_type = meat__type)
            if IngredientByName(name) is not None:
                Common.log('Ingredient already imported.  Replacing parameters')
                Common.global_state.all_ingredients=[i if i.name.lower() != name.lower() else new_ingredient for i in Common.global_state.all_ingredients]
            else:
                Common.log('Adding ingredient to global list: '+ name)
                Common.global_state.all_ingredients.append(new_ingredient)
                num_added += 1
        else:
            continue
    return num_added

def EditIngredient(ingredient):
    new_ingredient = Ingredient()
    new_ingredient.name = ingredient.name
    new_ingredient = PromptIngrLocation(new_ingredient)
    return new_ingredient

def EditIngredientMenu(display_parent_menu_func): #TODO
    '''
    Prompt user to modify an ingredient
    '''
    #TODO This will do for now, but make an actual menu
    new_global_list = Common.EditItemMenu('an ingredient', 'ingredients', 'recipe and ingredient menu',
        IngredientByName, Common.global_state.all_ingredients, EditIngredient, display_parent_menu_func)
    Common.global_state.all_ingredients = new_global_list
    return

def ListIngredients(command, ingredients_list = []): #TODO make this so it has one arg everywhere
    '''
    Print a list of ingredients according to a provided filter

    Parameters:
    command : str
        command of the format 'list <x>', where x is a filter of the start of the word
    '''
    ingr_list = ingredients_list
    if len(ingr_list) == 0:
        ingr_list = Common.global_state.all_ingredients
    Common.ListItem(command, ingr_list)
    return

def RemoveIngredientMenu(previous_menu):
    Common.RemoveItem(Common.global_state.all_ingredients, 'an ingredient', 'ingredients', ListIngredients, previous_menu)

def IngredientByName(name, ingredients=[]):
    ingr_copy = copy.deepcopy(ingredients)
    if len(ingredients) == 0:
        ingr_copy = Common.global_state.all_ingredients
    return Common.SearchItemByName(name, ingr_copy)
