import Ingredients
import Common
import Restrictions
import copy

valid_cuisine_types = ['chinese', 'indian', 'african', 'american', 'mexican','italian',
        'french', 'spanish', 'middle eastern', 'cajun', 'thai', 'soup', 'meat', 'dessert', 'snack']
max_stars = 10
class Recipe:
    def __init__(self, name='', ingredients=[], last_cooked=None,
    cuisine_type='', who_cooks='', num_servings=0, stars=-1, time_to_cook=-1, school_friendly=True, kid_friendly=True, restrictions=[], directions=[], history = []):
        '''
        Recipe class stores data about a recipe

        Parameters:
            name: str
                Name of the Recipe
            ingredients: list
                list of ingredients in the recipe by name as a dict with keys ingr_obj, quantity, and unit
            last_cooked: datetime.date
                date of last cooking
            cuisine_type: str
                Type of cuisine, e.g. "Mexican" or "Chinese"
            meat_type : str
                Type of meat, e.g. "Beef" or "Veggie"
            who_cooks: str
                Who typically cooks this recipe
            num_servings: int
                Number of servings for the whole family this recipe provides
            stars: int
                How many stars this recipe gets 1 (okay) 5 (best ever!!!!!)
            time_to_cook: int
                How long it takes to cook in minutes
            school_friendly: bool
                Can you take this to school / work easily
            kid_friendly: bool
                Will our kids eat it?
            restrictions: list
                list of restrictions that bar this recipe, including individual restriction profiles
            directions : list
                For later implementation of directions

        TODO: Consider including directions
        '''
        self.name = name
        self.ingredients=ingredients
        self.last_cooked=last_cooked
        self.cuisine_type=cuisine_type
        self.who_cooks=who_cooks
        self.num_servings=num_servings
        self.stars=stars
        self.time_to_cook=time_to_cook
        self.school_friendly=school_friendly
        self.kid_friendly=kid_friendly
        self.meat_type=self.GetMeatType()
        self.restrictions=restrictions
        self.directions = directions
        self.history = history

    def __str__(self):
        border = int((24-len(self.name))/2)
        self_string = '-'*border + self.name + '-'*border
        self_string += "\nCuisine : " + self.cuisine_type
        self_string += "\nCooked By : " + str(self.who_cooks)
        self_string += "\nNumber of Servings : " + str(self.num_servings)
        self_string += "\nTime to Cook : " + str(self.time_to_cook) +" minutes"
        self_string += "\nKid-Friendly : " + str(self.kid_friendly)
        self_string += "\nSchool/Work-Friendly : " + str(self.school_friendly)
        self_string += "\nMeat-Type : " + str(self.meat_type)
        self_string += "\nRestrictions : " + ', '.join([r.name for r in self.restrictions])
        self_string += "\nRating : " + '*'*self.stars

        self_string += "\nIngredients :\n " + '-'*border + "\n\t" + "\n\t".join([i.GroceryStoreFormatString() for i in self.ingredients])
        self_string += "\nDirections :\n " + '-'*border + "\n\t- " + "\n\t- ".join(self.directions)
        return self_string
    def __eq__(self, other):
        return type(self) == type(other) and self.name.lower() == other.name.lower()

    def Contains(self, name):
        '''
        Does this recipe contain ingredient with name given.
        '''
        if name in [x['ingr_obj'].name for x in self.ingrendients]:
            return True
        else:
            return False
    def GetMeatType(self):
        '''
        What kind of meat is in this
        '''
        for i in self.ingredients: # TODO: doesn't account for multiple-meat recipes
            if i.meat_type != '':
                return i.meat_type
        return 'vegetarian'
    def Perishable(self):
        '''
        Are there perishable ingredients in this recipe?
        '''
        for i in self.ingredients: # TODO: doesn't account for multiple-meat recipes
            if i.perishable == True:
                return True
        return False
    def Seasons(self):
        seasons = 'sufw'
        for i in self.ingredients:
            seasons = ''.join([x for x in seasons if x in i.seasons])
        return seasons

    def UpdateRecipeHistory(self, date = None):
        '''
        Update the history of this recipe
        '''
        if date == None:
            self.last_cooked = datetime.date.today()
            self.history.append(datetime.date.today())
        else:
            self.last_cooked = date
            self.history.append(date)

    def GetFamilyPackIngredients(self):
        return [i.name for i in self.ingredients if i.family_pack == True]
    def GetDirections(self):
        border="___________________\n"
        directions = border + "Ingredients:\n" + border + "\n".join([i.GroceryStoreFormatString() for i in self.ingredients])
        directions += "\n" + border + "Directions:\n" + border + "\n".join(self.directions)
        return directions

def PromptRecParameterString(parameter_name, validity_func, validity_prompt, default = False):
    return Common.PromptParameterString('recipe', parameter_name, validity_func, validity_prompt, default)

def PromptRecParameterYesNo(parameter_name, default = False):
    return Common.PromptParameterYesNo('recipe', parameter_name, default)

def PromptRecParameterStringMultiple(parameter_name, validity_func, validity_prompt, default = False):
    return Common.PromptParameterMultiple('recipe', 'string', parameter_name, validity_func, validity_prompt, default)

def PromptRecParameterInt(parameter_name, default = False):
    return Common.PromptParameterString('recipe', parameter_name, Common.ValidNum, Common.PromptValidNum, default)

def ValidName(name):
    if name.lower() in [r.name.lower() for r in Common.global_state.all_recipes]:
        return False
    return True

def PromptValidName(): #TODO
    print 'Name already chosen.  Choose a different name.'
    return

def PromptRecName(recipe, doall=True):
    name = PromptRecParameterString('a name', ValidName, PromptValidName)
    if name.lower() == 'c':
        return None
    elif name.lower() == 'b':
        if doall == False:
            return recipe
        recipe = PromptRecName(recipe)
    else:
        recipe.name = name
        if doall:
            recipe = PromptRecIngredients(recipe)
    return recipe

def ValidIngredient(ingr_name):

    if ingr_name in [i.name for i in Common.global_state.all_ingredients]: # Need to get the global state
        return True
    else:
        return False

def PromptValidIngredient():

    print "Valid ingredient names are: "
    Common.ListItem("list ", Common.global_state.all_ingredients, ', ')
    print 'Would you like to add an ingredient (y/n)?'
    while True:
        selection = raw_input('> ')
        if selection.lower() == 'y':
            new_ingredient = Ingredients.CreateNewIngredient()
            if new_ingredient != None:
                Common.global_state.all_ingredients.append(new_ingredient)
            break
        elif selection.lower() == 'n':
            break
    return

def PromptRecIngredients(recipe, doall=True):
    ingredients = PromptRecParameterStringMultiple("an ingredient", ValidIngredient, PromptValidIngredient, default = False)
    if str(ingredients).lower() == 'b':
        if doall:
            recipe = PromptRecName(recipe)
    elif str(ingredients).lower() == 'c':
        return recipe
    else:

        ingredient_objs = [copy.deepcopy(Common.SearchItemByName(i, Common.global_state.all_ingredients)) for i in ingredients]
        recipe.ingredients = ingredient_objs
        recipe.meat_type = recipe.GetMeatType()
        for i in ingredient_objs:
            print 'Ingredient ' + i.name + ":"
            i = Ingredients.PromptIngrQuantity(i)
            if i == None:
                return recipe
            i = Ingredients.PromptIngrUnit(i)
            if i == None:
                return recipe
        if doall:
            recipe = PromptRecCuisineType(recipe)
    return recipe

def ValidCuisineType(cuisine_type):
    if cuisine_type.lower() in valid_cuisine_types:
        return True
    else:
        return False

def PromptValidCuisineType():
    print "Valid cuisine types are:"
    print ", ".join(valid_cuisine_types)
    return

def PromptRecCuisineType(recipe, doall=True):
    cuisine_type = PromptRecParameterString('a type of cuisine', ValidCuisineType, PromptValidCuisineType)
    if cuisine_type.lower() == 'c':
        return None
    elif cuisine_type.lower() == 'b':
        if doall:
            recipe = PromptRecIngredients(recipe)
    else:
        recipe.cuisine_type = cuisine_type
        if doall:
            recipe = PromptRecChef(recipe)
    return recipe

def ValidChef(chef):

    if chef.lower() in [c.lower() for c in Common.global_state.chefs]:
        return True
    else:
        return False

def PromptValidChef():

    print "Valid chefs are:"
    print ", ".join(Common.global_state.chefs)

def PromptRecChef(recipe, doall=True):
    chef = PromptRecParameterString('a chef', ValidChef, PromptValidChef)
    if chef.lower() == 'c':
        return None
    elif chef.lower() == 'b':
        if doall:
            recipe = PromptRecCuisineType(recipe)
    else:
        recipe.who_cooks = chef
        if doall:
            recipe = PromptRecNumServings(recipe)
    return recipe


def PromptRecNumServings(recipe, doall=True):
    num_servings = PromptRecParameterInt('the number of meals for everyone')
    if num_servings.lower() == 'c':
        return None
    elif num_servings.lower() == 'b':
        if doall:
            recipe = PromptRecChef(recipe)
    else:
        recipe.num_servings = int(num_servings)
        if doall:
            recipe = PromptRecTimeToCook(recipe)
    return recipe

def PromptRecTimeToCook(recipe, doall=True):
    time_to_cook = PromptRecParameterInt('the time to cook in minutes')
    if time_to_cook.lower() == 'c':
        return None
    elif time_to_cook.lower() == 'b':
        if doall:
            recipe = PromptRecNumServings(recipe)
    else:
        recipe.time_to_cook = int(time_to_cook)
        if doall:
            recipe = PromptRecStars(recipe)
    return recipe

def ValidStars(num):
    if Common.ValidNum(num):
        if int(num) <= max_stars:
            return True
    return False

def PromptValidStars():
    print 'Choose a number between 1 and ' + str(max_stars) + '.'

def PromptRecStars(recipe, doall=True):
    stars = PromptRecParameterString('a rating from 1 to 10 (1 = meh, 10 = best EVER!)', ValidStars, PromptValidStars)
    if stars.lower() == 'c':
        return None
    elif stars.lower() == 'b':
        if doall:
            recipe = PromptRecTimeToCook(recipe)
    else:
        recipe.stars = int(stars)
        if doall:
            recipe = PromptRecSchoolFriendly(recipe)
    return recipe

def PromptRecSchoolFriendly(recipe, doall=True):
    school_friendly = PromptRecParameterYesNo('possible to take to work/school', True)
    if school_friendly == True or school_friendly == False:
        recipe.school_friendly = school_friendly
        if doall:
            recipe = PromptRecKidFriendly(recipe)
    elif school_friendly.lower() == 'd':
        if doall:
            recipe = PromptRecKidFriendly(recipe)
    elif school_friendly.lower() == 'b':
        if doall:
            recipe = PromptRecStars(recipe)
    else:
        return recipe
    return recipe

def PromptRecKidFriendly(recipe, doall=True):
    kid_friendly = PromptRecParameterYesNo('a recipe the kids like', True)
    if kid_friendly == True or kid_friendly == False:
        recipe.kid_friendly = kid_friendly
        if doall:
            recipe = PromptRecRestrictions(recipe)
    elif school_friendly.lower() == 'd':
        if doall:
            recipe = PromptRecRestrictions(recipe)
    elif school_friendly.lower() == 'b':
        if doall:
            recipe = PromptRecSchoolFriendly(recipe)
    else:
        return recipe
    return recipe

def ValidRestriction(restriction):

    restrictions = [r.name.lower() for r in Common.global_state.restriction_profiles]
    if restriction.lower() in restrictions:
        return True
    return False

def PromptValidRestriction():
    print "The restrictions available are: "

    print ', '.join([r.name for r in Common.global_state.restriction_profiles])
    return

def PromptRecRestrictions(recipe, doall=True):
    restriction_strings = PromptRecParameterStringMultiple("a restriction", ValidRestriction, PromptValidRestriction, default = False)
    if str(restriction_strings).lower() == 'b':
        if doall:
            recipe = PromptRecKidFriendly(recipe)
    elif str(restriction_strings).lower() == 'c':
        return recipe
    else:
        restrictions = [Restrictions.RestrictionByName(s, Common.global_state.restriction_profiles) for s in restriction_strings]
        Common.log("restrictions to add: "+str(restrictions)+"\n"+str([str(r) for r in restrictions]))
        recipe.restrictions = restrictions
        if doall:
            recipe = PromptRecDirections(recipe)
    return recipe

def ValidDirection(direction):
    if direction.find('\n') < 0:
        return True
    return false

def PromptValidDirection():
    print "Give one direction at a time"
    return

def PromptRecDirections(recipe, doall=True):
    directions = PromptRecParameterStringMultiple("a direction", ValidDirection, PromptValidDirection, default = True)
    if str(directions).lower() == 'b':
        if doall:
            recipe = PromptRecName(recipe)
    elif str(directions).lower() == 'c':
        return recipe
    elif str(directions).lower() == 'd':
        if doall:
            recipe = ReviewAndSaveRecipe(recipe)
    else:
        recipe.directions = directions
        if doall:
            recipe = ReviewAndSaveRecipe(recipe)
    return recipe

def ReviewAndSaveRecipe(recipe):
    print 'You have created the recipe: '
    print str(recipe)
    print 'Do you wish to save it? (y/n)'
    while True:
        selection = raw_input('> ')
        if selection.lower() == 'y':
            return recipe
        elif selection.lower() == 'n':
            return None
    return recipe

def CreateNewRecipe():
    '''
    Define new recipe to include in master recipe list

    Parameters:
        recipe_list : Recipe []
            List of all existing recipes

    Returns:
        Recipe []
            List of all existing recipes
    '''
    new_recipe = Recipe()
    new_recipe = PromptRecName(new_recipe)
    Common.log(str(new_recipe))
    return new_recipe

def PromptBadImportParameter(recipe_name, parameter_type, val, prompt_valid):
    print "ImportError: Recipe " + recipe_name + " has bad " + parameter_type + ": " + val
    prompt_valid()
    return

def ValidParameters(parameters):
    try:
        valid = True
        print '\n'.join(parameters)
        if len(parameters) < 10:
            if len(parameters) ==0:
                print 'Recipe has no parameters'
                return False
            print 'Recipe '+parameters[0]+ ' has too few parameters.'
        name = parameters[0]
        ingredients = parameters[1].split(':')
        Common.log(str(ingredients))
        Common.log("Ingredients in "+name)
        for i in ingredients:
            print i
        ingredient_data = [{'name':i.split(';')[0],'quantity':i.split(';')[1],'unit':i.split(';')[2]} for i in ingredients]
        for i in ingredient_data:
            if Ingredients.IngredientByName(i['name']) == None:
                PromptBadImportParameter(name, 'ingredient name', i['name'], PromptValidIngredient)
                valid = False
            if not Common.ValidNum(i['quantity']):
                valid = False
                PromptBadImportParameter(name, 'ingredient quantity', i['quantity'], Common.PromptValidNum)
            if not Ingredients.ValidUnit(i['unit']):
                valid = False
                PromptBadImportParameter(name, 'ingredient unit', i['unit'], Ingredients.PromptValidUnit)
        if not ValidCuisineType(parameters[2]):
            valid = False
            PromptBadImportParameter(name, 'cuisine type', parameters[2], PromptValidCuisineType)
        if not ValidChef(parameters[3]):
            valid = False
            PromptBadImportParameter(name, 'chef', parameters[3], PromptValidChef)
        if not Common.ValidNum(parameters[4]):
            valid = False
            PromptBadImportParameter(name, 'number of servings', parameters[4], Common.PromptValidNum)
        if not Common.ValidNum(parameters[5]):
            valid = False
            PromptBadImportParameter(name, 'time to cook', parameters[5], Common.PromptValidNum)
        if not Common.ValidNum(parameters[6]):
            valid = False
            PromptBadImportParameter(name, 'rating', parameters[6], Common.PromptValidNum)
        if not Common.ValidBool(parameters[7]):
            valid = False
            PromptBadImportParameter(name, 'school/work friendliness', parameters[7], Common.PromptValidBool)
        if not Common.ValidBool(parameters[8]):
            valid = False
            PromptBadImportParameter(name, 'kid friendliness', parameters[8], Common.PromptValidBool)
        restrictions = parameters[9].split(':')
        Common.log("Restrictions are "+str(restrictions)+'  '+str(len(restrictions)))
        for r in restrictions:
            if r == '':
                continue
            if not ValidRestriction(r):
                valid = False
                PromptBadImportParameter(name, 'restriction', r, PromptValidRestriction)
        return valid
    except Exception as e:
        return False


def ImportRecipes(rec_lines):
    rec_lines = rec_lines[1:] #ignore header
    num_added = 0
    for r in rec_lines:
        parameters = r.replace('\n','').split(',')

        if ValidParameters(parameters):
            name = parameters[0]
            #Ingredients(Name;quantity;unit:),CuisineType,Chef,NumServings,TimeToCook(Minutes),Stars,School/WorkFriendly,KidFriendly,Restrictions(: separated),Directions(:separated)
            ingredients = parameters[1].split(':')
            ingredient_data = [{'name':i.split(';')[0],'quantity':float(i.split(';')[1]),'unit':i.split(';')[2]} for i in ingredients]
            ingredient_objs = []
            for i in ingredient_data:
                ingr_copy = copy.deepcopy(Ingredients.IngredientByName(i['name']))
                ingr_copy.quantity = i['quantity']
                ingr_copy.unit = i['unit']
                ingredient_objs.append(ingr_copy)
            cuisine_type = parameters[2]
            chef = parameters[3]
            num_servings = int(parameters[4])
            time_to_cook = int(parameters[5])
            stars = int(parameters[6])
            school_friendly = True if parameters[7]=='1' else False
            kid_friendly = True if parameters[8]=='1' else False
            restriction_strings = parameters[9].split(':')
            if restriction_strings == ['']:
                restrictions = []
            else:
                restrictions = [Restrictions.RestrictionByName(r) for r in restriction_strings]
            directions = parameters[10].split(':')
                #elf, name='', ingredients=[], last_cooked=None,cuisine_type='', who_cooks='', num_servings=0, stars=-1, time_to_cook=-1, school_friendly=True, kid_friendly=True, restrictions=[], directions=[], history = []
            new_recipe = Recipe(name, ingredient_objs, None, cuisine_type, chef, num_servings, stars, time_to_cook, school_friendly, kid_friendly, restrictions, directions)
            if RecipeByName(name) is not None:
                Common.log('Ingredient already imported.  Replacing parameters')
                old_recipe = RecipeByName(name)
                new_recipe.history = old_recipe.history
                new_recipe.last_cooked = old_recipe.last_cooked
                Common.global_state.all_recipes=[r if r.name.lower() != name.lower() else new_recipe for r in Common.global_state.all_recipes]
            else:
                Common.global_state.all_recipes.append(new_recipe)
                num_added += 1
        else:
            continue
    return num_added

def EditParameter(recipe, parameter_func):
    new_recipe = parameter_func(recipe, False)
    if new_recipe:
        new_recipe = ReviewAndSaveRecipe(new_recipe)
        if new_recipe:
            DisplayEditRecipeMenu()
            return new_recipe
    DisplayEditRecipeMenu()
    return None



def DisplayEditRecipeMenu():
    print '--------------------------'
    print '    Edit Recipe Menu      '
    print '--------------------------'
    print '1) Modify ingredients'
    print '2) Modify cuisine'
    print '3) Modify chef'
    print '4) Modify number of servings'
    print '5) Modify time to cook'
    print '6) Modify rating'
    print '7) Modify school/work friendly'
    print '8) Modify kid friendly'
    print '9) Modify restrictions'
    print '10) Modify directions'
    print '(e)xit to previous menu'

def EditRecipe(recipe):
    new_recipe = copy.deepcopy(recipe)
    DisplayEditRecipeMenu()
    while True:
        selection = raw_input('> ')
        if selection.lower() == 'e':
            break
        elif selection == '1':
            new_recipe = EditParameter(new_recipe, PromptRecIngredients)
        elif selection == '2':
            new_recipe = EditParameter(new_recipe, PromptRecCuisineType)
        elif selection == '3':
            new_recipe = EditParameter(new_recipe, PromptRecChef)
        elif selection == '4':
            new_recipe = EditParameter(new_recipe, PromptRecNumServings)
        elif selection == '5':
            new_recipe = EditParameter(new_recipe, PromptRecTimeToCook)
        elif selection == '6':
            new_recipe = EditParameter(new_recipe, PromptRecStars)
        elif selection == '7':
            new_recipe = EditParameter(new_recipe, PromptRecSchoolFriendly)
        elif selection == '8':
            new_recipe = EditParameter(new_recipe, PromptRecKidFriendly)
        elif selection == '9':
            new_recipe = EditParameter(new_recipe, PromptRecRestrictions)
        elif selection == '10':
            new_recipe = EditParameter(new_recipe, PromptRecDirections)
    return new_recipe

def EditRecipeMenu(display_parent_menu_func): #TODO
    '''
    Prompt user to modify a recipe
    '''
    #TODO This will do for now, but make an actual menu
    new_global_list = Common.EditItemMenu('a recipe', 'recipes', 'recipe and ingredient menu',
        RecipeByName, Common.global_state.all_recipes, EditRecipe, display_parent_menu_func)
    Common.global_state.all_recipes = new_global_list
    return

def ListRecipes(command, recipe_list=[]): #TODO make this so it has one arg everywhere
    '''
    Print a list of recipes according to a provided filter

    Parameters:
    command : str
        command of the format 'list <x>', where x is a filter of the start of the word
    '''
    rec_list = recipe_list
    if len(rec_list) == 0:
        rec_list = Common.global_state.all_recipes
    Common.ListItem(command, rec_list)
    return

def RemoveRecipeMenu(previous_menu):
    Common.RemoveItem(Common.global_state.all_recipes, 'a recipe', 'recipes', ListRecipes, previous_menu)

def RecipeByName(name, recipes=[]):
    rec_copy = copy.deepcopy(recipes)
    if len(rec_copy) == 0:
        rec_copy = Common.global_state.all_recipes
    return Common.SearchItemByName(name, rec_copy)
