import Ingredients
import Recipe
import datetime
import Common
import History
from numpy.random import choice

def SelectFirstRecipe(global_state, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, history = Common.History()):
    '''
    Pick first recipe
    Returns:
        Recipe
            Candidate recipe
    '''
    new_recipe = None
    weights = [(WeightFirstRecipe(global_state, r, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, history)) for r in global_state.all_recipes]
    weight_sum = sum(weights)
    if weight_sum == 0:
        print "Error: first recipe choice is over-constrained. Returning a random recipe"
        ch = choice(len(global_state.all_recipes), 1)
        new_recipe = global_state.all_recipes[ch]
        return new_recipe
    weights = [float(w/float(weight_sum)) for w in weights]
    Common.log("Weights for recipes: "+str(weights))
    ch = choice(len(global_state.all_recipes),1, p = weights)
    new_recipe = global_state.all_recipes[ch]
    return new_recipe

def SelectMatchingRecipes(global_state, previous_recipes, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, history = Common.History()):
    '''
    Pick recipes to match previous recipes
    Parameters:
        number_needed : int
            Number of days food is needed for

    Returns:
        Recipe []
            List of matching recipes not including previous
    '''
    new_recipes = previous_recipes
    num_filled = sum([int(r.num_servings) for r in previous_recipes])
    while num_filled < global_state.NumServings():
        weights = [(WeightMatchingRecipe(global_state, r, new_recipes, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, history)) for r in global_state.all_recipes]
        weight_sum = sum(weights)
        if weight_sum == 0:
            print "Warning: Matching recipes are over-constrained. Returning existing list."
            return new_recipes
        weights = [float(w/float(weight_sum)) for w in weights]
        ch = choice(len(global_state.all_recipes),1, p = weights)
        new_recipes.append(global_state.all_recipes[ch])
        num_filled = sum([int(r.num_servings) for r in new_recipes])

    return new_recipes

#Weight Functions
def CalculateDuplicateWeight(recipe, previous_recipes=[]):
    if recipe.name in [r.name for r in previous_recipes]:
        return 0
    return 1

def CalculateOutOfTownWeight(recipe, current_chefs):
    Common.log("Current chefs = "+str(current_chefs))
    if recipe.who_cooks in current_chefs:
        return 1
    else:
        return 0

def CalculateTimeSinceWeight(recipe): # Obsolete perhaps?  Keep around to see behavior.
    '''
    Calculate weight factor based on time since last cooking this recipe
    '''
    today = datetime.date.today()
    last_cooked = recipe.last_cooked
    diff = today-last_cooked
    weeks_since = diff.days/7
    return 1-(2**(-weeks_since/4))

def CalculateMeatWeight(recipe, history = Common.History(), previous_recipes=[]):
    '''
    Calculate weight factor based on meat content
    '''
    Common.log("Calculating meat weight for "+recipe.name)
    if len(history.entries) == 0 and len(previous_recipes) == 0:
        return 1
    last_recipes = history.GetLastRecipes()
    previous_meats = [r.meat_type for r in previous_recipes]
    last_meats_inclusive = previous_meats + [r.meat_type for r in last_recipes]
    current_meat = recipe.meat_type
    Common.log("Previous meats: "+str(previous_meats))
    Common.log("Last meats inclusive: "+str(last_meats_inclusive))
    if len(previous_meats) > 0:
        fraction = len([m for m in previous_meats if m != current_meat])/float(len(previous_meats))
    else:
        fraction = 1
    Common.log("First fraction = "+str(fraction))
    if len(last_meats_inclusive) > 0:
        fraction *= len([m for m in last_meats_inclusive if m != current_meat])/float(len(last_meats_inclusive))
    Common.log("2nd fraction = "+str(fraction))
    return fraction

def CalculateCuisineWeight(recipe, history = Common.History(), previous_recipes=[]):
    '''
    Calculate weight factor based on cuisine Type
    '''
    if recipe.cuisine_type.lower() == 'dessert' or recipe.cuisine_type.lower() == 'snack':
        return 0
    if len(history.entries) == 0 and len(previous_recipes) == 0:
        return 1
    last_recipes = history.GetLastRecipes()
    previous_cuisines = [r.cuisine_type for r in previous_recipes]
    last_cuisines_inclusive = previous_cuisines + [r.cuisine_type for r in last_recipes]
    current_cuisine = recipe.cuisine_type
    if len(previous_cuisines) > 0:
        fraction = len([c for c in previous_cuisines if c != current_cuisine])/float(len(previous_cuisines))
    else:
        fraction = 1
    if len(last_cuisines_inclusive) > 0:
        fraction *= len([c for c in last_cuisines_inclusive if c != current_cuisine])/float(len(last_cuisines_inclusive))
    return fraction

def CalculateLaborDistributionWeight(recipe, global_state, current_chefs, previous_recipes = []):
    '''
    Calculate weight factor based on distributing the labor of cooking
    '''
    if len(current_chefs) < 2:
        return 1
    if len(previous_recipes)>=2:
        chefs = [r.who_cooks for r in previous_recipes]
        occurences = [(i, chefs.count(i)) for i in global_state.chefs]
        for i in occurences:
            other_counts = [o[1] for o in occurences if o[0]!=i[0]]
            if i[1] <= min(other_counts) - 2:
                if recipe.who_cooks != i[0]:
                    return 0
            return 1
    return 1

def CalculateFamilyPackWeight(recipe, previous_recipes = []):
    '''
    Calculate weight factor based on filling out family packs
    '''
    Common.log("Calculating family pack weight for "+recipe.name+" with previous recipes "+", ".join([r.name for r in previous_recipes]))
    fam_pack_ingredients_lists = [p.GetFamilyPackIngredients() for p in previous_recipes]
    Common.log("fam_pack_ingredients_lists = "+str([str(f) for f in fam_pack_ingredients_lists]))
    #Check for duplicates
    if len(fam_pack_ingredients_lists)>1:
        for m in fam_pack_ingredients_lists:
            if len(m) == 0:
                continue
            for n in fam_pack_ingredients_lists:
                if m == n:
                    continue
                common = list(set(m).intersection(set(n)))
                for ing in common:
                    m.remove(ing)
                    n.remove(ing)

    fam_pack_ingredients_sets = [set(j) for j in fam_pack_ingredients_lists]
    Common.log("fam_pack_ingredients_sets = "+str(fam_pack_ingredients_sets))
    for i in range(1, len(fam_pack_ingredients_sets)):
        fam_pack_ingredients_sets[0].union(fam_pack_ingredients_sets[i])
    fam_pack_ingredients = list(fam_pack_ingredients_sets[0])
    Common.log("fam_pack_ingredients = "+str(fam_pack_ingredients))
    if len(fam_pack_ingredients) > 0:
        Common.log("Family pack ingredients exist.  Testing for those. ")
        for i in recipe.GetFamilyPackIngredients():
            if i in fam_pack_ingredients:
                return 1
        return 0
    else:
        Common.log("Length is 0. returning 1")
        return 1

def CalculateServingWeight(recipe, previous_recipes, total_meals_needed):
    '''
    Calculate weight factor based on how many more meals are needed
    '''
    Common.log("CalculatingServingWeight for "+recipe.name+" with previous recipes "+ ", ".join([r.name for r in previous_recipes]))
    Common.log("Total meals needed = "+ str(total_meals_needed))
    num_servings_already_covered = sum([int(r.num_servings) for r in previous_recipes])
    Common.log("Num servings already covered = "+str(num_servings_already_covered))
    num_needed = total_meals_needed - num_servings_already_covered
    Common.log("Recipe num servings = "+str(recipe.num_servings)+" Num needed ="+ str(num_needed))
    if int(recipe.num_servings) > int(num_needed) + 3:
        Common.log("Recipe is too big")
        return 0
    else:
        Common.log("Recipe is not too big")
        return 1

def RecursiveRestrictionList(restriction_profile):
    '''
    Return a list of strings of restrictions to look for
    '''
    profile_strings = []
    for r in restriction_profile.restrictions:
        profile_strings.append(r.name)
        profile_strings += RecursiveRestrictionList(r)
    return profile_strings

def CalculateDietaryRestrictionWeight(recipe, current_restrictions, banned_ingredients):
    '''
    Calculate weight factor based on cuisine Type
    '''
    if len(current_restrictions) == 0:
        return 1
    #Search for this recipe in banned recipes:
    for r in current_restrictions:
        if recipe.name.lower() in [n.name.lower for n in r.banned_recipes]:
            return 0
    strings_to_search = []
    for r in current_restrictions:
        strings_to_search += RecursiveRestrictionList(r)
    ingredients_to_search = []
    ingredients_to_search += banned_ingredients
    ingredients_to_search += [i.banned_ingredients for i in current_restrictions]

    for s in strings_to_search:
        if s in recipe.restrictions:
            return 0
    for i in ingredients_to_search: # This might not work b/c of comparison issues
        for j in recipe.ingredients:
            if i == j:
                return 0
    return 1

def CalculatePreferenceWeight(recipe):
    '''
    Calculate weight factor based on how much we like it
    '''
    weight = recipe.stars
    return weight

def LongCookTime(recipes):
    '''
    Are there already enough recipes that are long?
    '''
    cumulative_time = 1
    for r in recipes:
        cumulative_time *= int(r.time_to_cook) / 40
    if cumulative_time > 4: #TODO adjust as necessary
        return True
    else:
        return False

def CalculateSpeedWeight(recipe, global_state, previous_recipes = []):
    '''
    Calculate weight factor based on speed of cooking
    '''
    if global_state.quick_meals or LongCookTime(previous_recipes):
        weight = 1/float(int(recipe.time_to_cook) **2)
        return weight
    else:
        return 1

def CalculateSchoolWeight(recipe, previous_recipes = []):
    '''
    Calculate weight factor based on whether it can be taken to school
    '''
    if recipe.school_friendly:
        return 1
    elif len(previous_recipes) < 2 or len([r for r in previous_recipes if r.school_friendly == True]) >=2: #TODO make this more like kid freidnly
        return 1
    return 0

def CalculateKidFriendlyWeight(recipe, previous_recipes = []):
    '''
    Calculate weight factor based on whether the kids like it
    '''
    if recipe.kid_friendly:
        return 1
    elif len(previous_recipes) < 1:
        return 1
    elif len(previous_recipes) - len([r for r in previous_recipes if r.school_friendly == True]) < 1:
        return 1
    return 0

def CalculateSeasonWeight(recipe):
    '''
    Calculate weight factor based on season
    '''
    today = datetime.date.today()
    seasons = recipe.Seasons()
    if seasons.find('s') < 0 and History.IsSpring(today) :
        return 0
    if seasons.find('u') < 0 and History.IsSummer(today) :
        return 0
    if seasons.find('f') < 0 and History.IsFall(today) :
        return 0
    if seasons.find('w') < 0 and History.IsWinter(today) :
        return 0
    return 1

def CalculateHistoryWeight(recipe):
    '''
    Calculate weight based on our history
    '''
    last_cooked = recipe.last_cooked
    if last_cooked == None:
        return 1
    today = datetime.date.today()
    diff = last_cooked - today
    if diff.days/7 <=3:
        return 0
    else:
        return log(diff.days)

def CalculatePerishabilityWeight(recipe, previous_recipes = []):
    '''
    Calculate weight factor based on perishability
    '''
    perishable_recipes = [r for r in previous_recipes if r.Perishable()]
    if len(perishable_recipes) >= 2 and recipe.Perishable():
        return 0
    return 1

def CalculateUseUpWeight(recipe, ingredients_to_use = [], previous_recipes = []):
    '''
    Calculate weight factor based on ingredients that need to be used up
    '''
    if len(ingredients_to_use) == 0:
        return 1
    all_previous_ingredients = [i for r in previous_recipes for i in r.ingredients]
    ingredients_unfulfilled = [i for i in ingredients_to_use if i not in all_previous_ingredients]
    if len(ingredients_unfulfilled) == 0:
        return 1
    ingredients_fulfilled = [i for i in recipe.ingredients if i in ingredients_unfulfilled]
    if len(ingredients_fulfilled)>0:
        return 1
    else:
        return 0

#Do All Weights
def WeightFirstRecipe(global_state, recipe, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, history = Common.History()):
    '''

    '''
    Common.log("Weighting recipe "+recipe.name)
    weight = 1
    weight *= CalculateOutOfTownWeight(recipe, current_chefs)
    Common.log("Weight after OutOfTown = "+str(weight))
    weight *= CalculateMeatWeight(recipe, history)
    Common.log("Weight after Meat = "+str(weight))
    weight *= CalculateCuisineWeight(recipe, history)
    Common.log("Weight after Cuisine = "+str(weight))
    weight *= CalculateLaborDistributionWeight(recipe, global_state, current_chefs)
    Common.log("Weight after LaborDistribution = "+str(weight))
    #No family pack distribution for first recipe
    #No serving weight for first recipe
    weight *= CalculateDietaryRestrictionWeight(recipe, current_restrictions, banned_ingredients)
    Common.log("Weight after DietaryRestrictions = "+str(weight))
    weight *= CalculatePreferenceWeight(recipe)
    Common.log("Weight after Preference = "+str(weight))
    weight *= CalculateSpeedWeight(recipe, global_state)
    Common.log("Weight after Speed = "+str(weight))
    #no school weight for first recipe
    #no kid friendly weight for first recipe
    weight *= CalculateSeasonWeight(recipe)
    Common.log("Weight after Season = "+str(weight))
    weight *= CalculateHistoryWeight(recipe)
    Common.log("Weight after History = "+str(weight))
    # no perishability weight for first recipe
    weight *= CalculateUseUpWeight(recipe, ingredients_to_use)
    Common.log("Weight after Useup = "+str(weight))

    return weight

def WeightMatchingRecipe(global_state, recipe, previous_recipes, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, history = Common.History()):
    '''
    '''
    Common.log("Weighting matching recipe "+recipe.name)
    weight = 1
    weight *=CalculateDuplicateWeight(recipe, previous_recipes)
    Common.log("Weight after Duplicate = "+str(weight))
    weight *= CalculateOutOfTownWeight(recipe, current_chefs)
    Common.log("Weight after OutofTown = "+str(weight))
    weight *= CalculateMeatWeight(recipe, history, previous_recipes)
    Common.log("Weight after Meat = "+str(weight))
    weight *= CalculateCuisineWeight(recipe, history, previous_recipes)
    Common.log("Weight after Cuisine = "+str(weight))
    weight *= CalculateLaborDistributionWeight(recipe, global_state, current_chefs, previous_recipes)
    Common.log("Weight after LaborDistribution = "+str(weight))
    weight *= CalculateFamilyPackWeight(recipe, previous_recipes)
    Common.log("Weight after FamilyPack = "+str(weight))
    weight *= CalculateServingWeight(recipe, previous_recipes, global_state.NumServings())
    Common.log("Weight after Serving = "+str(weight))
    weight *= CalculateDietaryRestrictionWeight(recipe, current_restrictions, banned_ingredients)
    Common.log("Weight after DietaryRestrictions = "+str(weight))
    weight *= CalculatePreferenceWeight(recipe)
    Common.log("Weight after Preference = "+str(weight))
    weight *= CalculateSpeedWeight(recipe, global_state, previous_recipes)
    Common.log("Weight after Speed = "+str(weight))
    weight *= CalculateSchoolWeight(recipe, previous_recipes)
    Common.log("Weight after School = "+str(weight))
    weight *= CalculateKidFriendlyWeight(recipe, previous_recipes)
    Common.log("Weight after KidFriendly = "+str(weight))
    weight *= CalculateSeasonWeight(recipe)
    Common.log("Weight after Season = "+str(weight))
    weight *= CalculateHistoryWeight(recipe)
    Common.log("Weight after History = "+str(weight))
    weight *= CalculatePerishabilityWeight(recipe, previous_recipes)
    Common.log("Weight after Preishability = "+str(weight))
    weight *= CalculateUseUpWeight(recipe, ingredients_to_use, previous_recipes)
    Common.log("Weight after Useup = "+str(weight))

    return weight

def SuggestRecipes(global_state, current_recipes, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, history):
    '''
    Suggest recipes based on the global state and current state
    Parameters:
        global_state : GlobalState
            The global state
        current_recipes : list
            list of recipes already chosen
        current_restrictions : list
            list of restrictions
        current_chefs : list
            the available chefs
        ingredients_to_use : list
            Ingredients to prioritize getting rid of
        banned_ingredients : list
            ingredients that have been banned
        history : ??? TODO
            History

    '''

    if len(current_recipes) == 0:
        first_recipe = SelectFirstRecipe(global_state, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, history)
        if first_recipe == None:
            return []
        current_recipes = [first_recipe]
    else:
        first_recipe = current_recipes[0]

    new_recipes = SelectMatchingRecipes(global_state, current_recipes, current_restrictions, current_chefs, ingredients_to_use, banned_ingredients, history)

    return new_recipes
