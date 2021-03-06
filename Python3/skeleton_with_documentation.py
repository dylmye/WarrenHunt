#Skeleton Program code for the AQA A Level Paper 1 2017 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.4.1 programming environment
""" AQA 2017 Skeleton Program

This program is the basis for the 'Rabbits & Foxes' 2017 AQA Computer Science A Level program.

The documentation style is based on the Google documentation style, available here: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

Version 3.0.2
"""

import enum
import random
import math

class Location:
  """
  Location is used in the Simulation class as a very basic level grid
  """
  def __init__(self):
    self.Fox = None
    self.Warren = None
 
class Simulation:
  """
  Simulation sets up the whole Rabbits & Foxes simulation, and is customisable.

  Args:
      LandscapeSize (int): Width and Height for landscape grid on which Animals etc. are placed
      InitialWarrenCount (int): How many Warrens to initiate with
      InitialFoxCount (int): How many Foxes to initiate with
      Variability (int): Something to do with chance/randomness in Warrens
      FixedInitialLocations (bool): Don't use random locations for Warrens?

  Attributes:
      __ViewRabbits (str)
      __TimePeriod (int)
      __WarrenCount (int)
      __FoxCount (int)
      __ShowDetail (bool)
      __LandscapeSize (int)
      __Variability (int): Something to do with chance/randomness in Warrens
      __FixedInitialLocations (bool)
      __Landscape (list)
  """
  def __init__(self, LandscapeSize, InitialWarrenCount, InitialFoxCount, Variability, FixedInitialLocations):
    self.__ViewRabbits = ""
    self.__TimePeriod = 0
    self.__WarrenCount = 0
    self.__FoxCount = 0
    self.__ShowDetail = False
    self.__LandscapeSize = LandscapeSize
    self.__Variability = Variability
    self.__FixedInitialLocations = FixedInitialLocations
    self.__Landscape = []
    for Count1 in range (self.__LandscapeSize):
      LandscapeRow = []
      for Count2 in range (self.__LandscapeSize):
        LandscapeLocation = None
        LandscapeRow.append(LandscapeLocation)
      self.__Landscape.append(LandscapeRow)
    self.__CreateLandscapeAndAnimals(InitialWarrenCount, InitialFoxCount, self.__FixedInitialLocations)
    self.__DrawLandscape()
    MenuOption = 0
    while (self.__WarrenCount > 0 or self.__FoxCount > 0) and MenuOption != 5:
      print()
      print("1. Advance to next time period showing detail")
      print("2. Advance to next time period hiding detail")
      print("3. Inspect fox")
      print("4. Inspect warren")
      print("5. Exit")
      print()
      MenuOption = int(input("Select option: "))
      if MenuOption == 1:
        self.__TimePeriod += 1
        self.__ShowDetail = True
        self.__AdvanceTimePeriod()
      if MenuOption == 2:
        self.__TimePeriod += 1
        self.__ShowDetail = False
        self.__AdvanceTimePeriod()
      if MenuOption == 3:
        x = self.__InputCoordinate("x")
        y = self.__InputCoordinate("y")
        if not self.__Landscape[x][y].Fox is None:
          self.__Landscape[x][y].Fox.Inspect()
      if MenuOption == 4:
        x = self.__InputCoordinate("x")
        y = self.__InputCoordinate("y")
        if not self.__Landscape[x][y].Warren is None:
          self.__Landscape[x][y].Warren.Inspect()
          self.__ViewRabbits = input("View individual rabbits (y/n)? ")
          if self.__ViewRabbits == "y":
            self.__Landscape[x][y].Warren.ListRabbits()
    input()
    
  def __InputCoordinate(self, CoordinateName):
    """
    Takes an input co-ordinate and processes it as an int

    Note:
      Validation needed: 0 < CoordinateName < (self.__LandscapeSize - 1)

    Args:
      CoordinateName (str): Requires string 'x' or 'y'
    
    Attributes:
      Coordinate (int): User-inputted coordinate value
    
    Returns:
      int: Specified coordinate value
    """
    Coordinate = int(input("  Input " + CoordinateName + " coordinate:"))
    return Coordinate
  
  def __AdvanceTimePeriod(self):
    """
    Advances game by killing, destroying, aging, etc. Adapts to settings (self.__ShowDetail, Warren.Inspect(), etc)
    """
    NewFoxCount = 0
    if self.__ShowDetail:
      print()
    for x in range (0, self.__LandscapeSize):
      for y in range (0, self.__LandscapeSize):
        if not self.__Landscape[x][y].Warren is None:
          if self.__ShowDetail:
            print("Warren at (", x, ",", y, "):", sep = "")
            print("  Period Start: ", end = "")
            self.__Landscape[x][y].Warren.Inspect()

          if self.__FoxCount > 0:
            self.__FoxesEatRabbitsInWarren(x, y)

          if self.__Landscape[x][y].Warren.NeedToCreateNewWarren():
            self.__CreateNewWarren()
          self.__Landscape[x][y].Warren.AdvanceGeneration(self.__ShowDetail)

          if self.__ShowDetail:
            print("  Period End: ", end = "")
            self.__Landscape[x][y].Warren.Inspect()
            input()
            
          if self.__Landscape[x][y].Warren.WarrenHasDiedOut():
            self.__Landscape[x][y].Warren = None
            self.__WarrenCount -= 1
    for x in range (0, self.__LandscapeSize):
      for y in range (0, self.__LandscapeSize):
        if not self.__Landscape[x][y].Fox is None:
          if self.__ShowDetail:
            print("Fox at (", x, ",", y, "): ", sep = "")
          self.__Landscape[x][y].Fox.AdvanceGeneration(self.__ShowDetail)

          if self.__Landscape[x][y].Fox.CheckIfDead():
            self.__Landscape[x][y].Fox = None
            self.__FoxCount -= 1
          else:
            if self.__Landscape[x][y].Fox.ReproduceThisPeriod():
              if self.__ShowDetail:
                print("  Fox has reproduced. ")
              NewFoxCount += 1
            if self.__ShowDetail:
              self.__Landscape[x][y].Fox.Inspect()
            self.__Landscape[x][y].Fox.ResetFoodConsumed()

    if NewFoxCount > 0:
      if self.__ShowDetail:
        print("New foxes born: ")
      for f in range (0, NewFoxCount):
        self.__CreateNewFox()
    if self.__ShowDetail:
      input()
    self.__DrawLandscape()
    print()

  def __CreateLandscapeAndAnimals(self, InitialWarrenCount, InitialFoxCount, FixedInitialLocations):
    """
    Initiates the warrens and foxes and their respective locations

    Args:
      InitialWarrenCount (int): Number of warrens the user starts with
      InitialFoxCount (int): Number of foxes to begin with
      FixedInitialLocations (bool): Whether to initiate with non-random variables 
    
    Attributes:
      __Landscape (list): Initialised Grid to place things on
    """
    for x in range (0, self.__LandscapeSize):
      for y in range (0, self.__LandscapeSize):
        self.__Landscape[x][y] = Location()
    if FixedInitialLocations:
      self.__Landscape[1][1].Warren = Warren(self.__Variability, 38)
      self.__Landscape[2][8].Warren = Warren(self.__Variability, 80) 
      self.__Landscape[9][7].Warren = Warren(self.__Variability, 20)
      self.__Landscape[10][3].Warren = Warren(self.__Variability, 52)
      self.__Landscape[13][4].Warren = Warren(self.__Variability, 67)
      self.__WarrenCount = 5
      self.__Landscape[2][10].Fox = Fox(self.__Variability)
      self.__Landscape[6][1].Fox = Fox(self.__Variability)
      self.__Landscape[8][6].Fox = Fox(self.__Variability)
      self.__Landscape[11][13].Fox = Fox(self.__Variability)
      self.__Landscape[12][4].Fox = Fox(self.__Variability)
      self.__FoxCount = 5
    else:
      for w in range (0, InitialWarrenCount):
        self.__CreateNewWarren()
      for f in range (0, InitialFoxCount):
        self.__CreateNewFox()

  def __CreateNewWarren(self):
    """
    Initiates another warren at random coordinates
    
    Attributes:
      x (int)
      y (int)
    """
    x = random.randint(0, self.__LandscapeSize - 1)
    y = random.randint(0, self.__LandscapeSize - 1)
    while not self.__Landscape[x][y].Warren is None:
      x = random.randint(0, self.__LandscapeSize - 1)
      y = random.randint(0, self.__LandscapeSize - 1)
    if self.__ShowDetail:
      print("New Warren at (", x, ",", y, ")", sep = "")
    self.__Landscape[x][y].Warren = Warren(self.__Variability)
    self.__WarrenCount += 1
  
  def __CreateNewFox(self):
    x = random.randint(0, self.__LandscapeSize - 1)
    y = random.randint(0, self.__LandscapeSize - 1)
    while not self.__Landscape[x][y].Fox is None:
      x = random.randint(0, self.__LandscapeSize - 1)
      y = random.randint(0, self.__LandscapeSize - 1)
    if self.__ShowDetail:
      print("  New Fox at (", x, ",", y, ")", sep = "")
    self.__Landscape[x][y].Fox = Fox(self.__Variability)
    self.__FoxCount += 1

  def __FoxesEatRabbitsInWarren(self, WarrenX, WarrenY):
    """
    Kills rabbits near foxes

    Args:
      WarrenX (int): Given Warren x coordinate
      WarrenY (int): Given Warren y coordinate
    
    Attributes:
      RabbitCountAtStartOfPeriod (int): um
      Dist (int): Distance between the fox and the warren
      PercentToEat (int): What percent of the warren the fox will, um, consume
      RabbitsToEat (int): Number of rabbits ready to face death
      FoodConsumed (int): RabbitsToEat if RabbitsToEat < RabbitCount
    """
    RabbitCountAtStartOfPeriod = self.__Landscape[WarrenX][WarrenY].Warren.GetRabbitCount()
    for FoxX in range(0, self.__LandscapeSize):
      for FoxY in range (0, self.__LandscapeSize):
        if not self.__Landscape[FoxX][FoxY].Fox is None:
          Dist = self.__DistanceBetween(FoxX, FoxY, WarrenX, WarrenY)
          if Dist <= 3.5:
            PercentToEat = 20
          elif Dist <= 7:
            PercentToEat = 10
          else:
            PercentToEat = 0
          RabbitsToEat = int(round(float(PercentToEat * RabbitCountAtStartOfPeriod / 100)))
          FoodConsumed = self.__Landscape[WarrenX][WarrenY].Warren.EatRabbits(RabbitsToEat)
          self.__Landscape[FoxX][FoxY].Fox.GiveFood(FoodConsumed)
          if self.__ShowDetail:
            print("  ", FoodConsumed, " rabbits eaten by fox at (", FoxX, ",", FoxY, ").", sep = "")

  def __DistanceBetween(self, x1, y1, x2, y2):
    """
    Calculates the distance between two objects at the given coordinates

    Args:
      x1 (int): First object's x coordinate
      y1 (int): First object's y coordinate
      x1 (int): Second object's x coordinate
      y2 (int): Second object's y coordinate
    
    Returns:
      int: returns the square root of (x1 - x2)^2 added to (y1 - y2)^2
    """
    return math.sqrt((pow(x1 - x2, 2) + pow(y1 - y2, 2)))

  def __DrawLandscape(self):
    """
    Pretty-prints a representation of the current state of the Landscape, battleships-style
    """
    print()
    print("TIME PERIOD:", self.__TimePeriod)
    print()
    print("   ", end = "")
    for x in range (0, self.__LandscapeSize):
      if x < 10:
        print(" ", end = "")
      print(x, "|", end = "")
    print()
    for x in range (0, self.__LandscapeSize * 4 + 3):
      print("-", end = "")
    print()
    for y in range (0, self.__LandscapeSize):
      if y < 10:
        print(" ", end = "")
      print("", y, "|", sep = "", end = "")
      for x in range (0, self.__LandscapeSize):
        if not self.__Landscape[x][y].Warren is None:
          if self.__Landscape[x][y].Warren.GetRabbitCount() < 10:
            print(" ", end = "")
          print(self.__Landscape[x][y].Warren.GetRabbitCount(), end = "")
        else:
          print("  ", end = "")
        if not self.__Landscape[x][y].Fox is None:
          print("F", end = "")
        else:
          print(" ", end = "")
        print("|", end = "")
      print()

class Warren:
  """
  Warren class creates a building for rabbits to live in, aka a "warren"

  Args:
      Variability (int): Something to do with chance/randomness in Warrens
      RabbitCount (int, optional): Number of Rabbits initially in Warren (defaults to 0)

  Attributes:
      __MAX_RABBITS_IN_WARREN (int): Hard limit on warren population size
      __RabbitCount (int): Number of Rabbits initially in Warren
      __PeriodsRun (int): iterator counter for periods
      __AlreadySpread (bool): Whether the warren contains the maximum amount of rabbits already
      __Variability (int): Something to do with chance/randomness in Warrens
      __Rabbits (list): List of objects (Rabbit class instances) associated with warren 
  """
  def __init__(self, Variability, RabbitCount = 0):
    self.__MAX_RABBITS_IN_WARREN = 99
    self.__RabbitCount = RabbitCount
    self.__PeriodsRun = 0
    self.__AlreadySpread = False
    self.__Variability = Variability
    self.__Rabbits = []
    for Count in range(0, self.__MAX_RABBITS_IN_WARREN):
      self.__Rabbits.append(None)
    if self.__RabbitCount == 0:
      self.__RabbitCount = int(self.__CalculateRandomValue(int(self.__MAX_RABBITS_IN_WARREN / 4), self.__Variability))
    for r in range (0, self.__RabbitCount):
      self.__Rabbits[r] = Rabbit(self.__Variability)

  def __CalculateRandomValue(self, BaseValue, Variability):
    """
    Calculates a pseudo-random value for Variability

    Args:
      BaseValue (int): ???
      Variability (int): Something to do with chance/randomness in Warrens
    
    Returns:
      int: random value based on BaseValue and Variability
    """
    return BaseValue - (BaseValue * Variability / 100) + (BaseValue * random.randint(0, Variability * 2) / 100)

  def GetRabbitCount(self): 
    """
    Getter for private variable self.__RabbitCount
    
    Returns:
      int: value of self.__RabbitCount
    """
    return self.__RabbitCount
  
  def NeedToCreateNewWarren(self): 
    """
    Tells you if you need to make a new warren (if you haven't hit max rabbits)
    
    Returns:
      bool: If a new Warren is requied
    """
    if self.__RabbitCount == self.__MAX_RABBITS_IN_WARREN and not self.__AlreadySpread:
      self.__AlreadySpread = True
      return True
    else:
      return False
    
  def WarrenHasDiedOut(self):
    """
    Getter for private variable self.__RabbitCount, with a twist - returns True if any rabbits exist. A weird alternative to `if(GetRabbitCount() > 0)`
    
    Returns:
      bool: True if any rabbits are still alive
    """
    if self.__RabbitCount == 0:
      return True
    else:
      return False

  def AdvanceGeneration(self, ShowDetail):
    """
    Advances rabbits by, um, killing them

    Note:
      Could be simplified into one if/else with a nested if for ln 408
    """
    self.__PeriodsRun += 1
    if self.__RabbitCount > 0:
      self.__KillByOtherFactors(ShowDetail)
    if self.__RabbitCount > 0:
      self.__AgeRabbits(ShowDetail)
    if self.__RabbitCount > 0 and self.__RabbitCount <= self.__MAX_RABBITS_IN_WARREN:
      if self.__ContainsMales():
        self.__MateRabbits(ShowDetail)
    if self.__RabbitCount == 0 and ShowDetail:
      print("  All rabbits in warren are dead")
    
  def EatRabbits(self, RabbitsToEat):
    """
    Brutally destroys rabbits

    Args:
      RabbitsToEat (int): Number of Rabbits to 'eat'

    Attributes:
      DeathCount (int): Iterator counter for rabbits murdered for the while loop
      RabbitsToEat (int): Clone of self.RabbitsToEat to manipulate
      RabbitNumber (int): Randomly chosen number used as the index in the self.__Rabbits list to pick for murder
    
    Returns:
      int: kinda useless, just the same as self.RabbitsToEat
    """
    DeathCount = 0
    if RabbitsToEat > self.__RabbitCount:
      RabbitsToEat = self.__RabbitCount
    while DeathCount < RabbitsToEat:
      RabbitNumber = random.randint(0, self.__RabbitCount - 1)
      if not self.__Rabbits[RabbitNumber] is None:
        self.__Rabbits[RabbitNumber] = None
        DeathCount += 1
    self.__CompressRabbitList(DeathCount)
    return RabbitsToEat

  def __KillByOtherFactors(self, ShowDetail):
    """
    Massacres rabbits for other reasons

    Args:
      ShowDetail (bool): config option - whether to print what's going on

    Attributes:
      DeathCount (int): Iterator counter for rabbits murdered
    """
    DeathCount = 0
    for r in range (0, self.__RabbitCount):
      if self.__Rabbits[r].CheckIfKilledByOtherFactor():
        self.__Rabbits[r] = None
        DeathCount += 1
    self.__CompressRabbitList(DeathCount)
    if ShowDetail:
      print(" ", DeathCount, "rabbits killed by other factors.")

  def __AgeRabbits(self, ShowDetail):
    DeathCount = 0
    for r in range (0, self.__RabbitCount):
      self.__Rabbits[r].CalculateNewAge()
      if self.__Rabbits[r].CheckIfDead():
        self.__Rabbits[r] = None
        DeathCount += 1
    self.__CompressRabbitList(DeathCount)
    if ShowDetail:
      print(" ", DeathCount, "rabbits die of old age.")

  def __MateRabbits(self, ShowDetail):
    """
    Creates young rabbits

    Args:
      ShowDetail (bool): config option - whether to print what's going on

    Attributes:
      Mate (int): Randomly chosen male Rabbit
      Babies (int): Iterative counter for how many rabbits are born
    """
    Mate = 0
    Babies = 0 
    for r in range (0, self.__RabbitCount):
      if self.__Rabbits[r].IsFemale() and self.__RabbitCount + Babies < self.__MAX_RABBITS_IN_WARREN:
        Mate = random.randint(0, self.__RabbitCount - 1)
        while Mate == r or self.__Rabbits[Mate].IsFemale():
          Mate = random.randint(0, self.__RabbitCount - 1)
        CombinedReproductionRate = (self.__Rabbits[r].GetReproductionRate() + self.__Rabbits[Mate].GetReproductionRate()) / 2
        if CombinedReproductionRate >= 1:
          self.__Rabbits[self.__RabbitCount + Babies] = Rabbit(self.__Variability, CombinedReproductionRate)
          Babies += 1
    self.__RabbitCount = self.__RabbitCount + Babies
    if ShowDetail:
      print(" ", Babies, "baby rabbits born.")

  def __CompressRabbitList(self, DeathCount):
    """
    A.K.A Corpse Compactor, removes dead rabbits when DeathCount > 0

    Args:
      DeathCount (int): Number of dead Rabbits

    Attributes:
      ShiftFrom (int): ???
      ShiftTo (int): ???
    """
    if DeathCount > 0:
      ShiftTo = 0
      ShiftFrom  = 0
      while ShiftTo < self.__RabbitCount - DeathCount:
        while self.__Rabbits[ShiftFrom] is None:
          ShiftFrom += 1
        if ShiftTo != ShiftFrom:
          self.__Rabbits[ShiftTo] = self.__Rabbits[ShiftFrom]
        ShiftTo += 1
        ShiftFrom += 1
      self.__RabbitCount = self.__RabbitCount - DeathCount

  def __ContainsMales(self):
    """
    True if any male rabbits are still alive

    Returns:
      bool: True if any male rabbits exist, otherwise False
    """
    Males = False
    for r in range (0, self.__RabbitCount):
      if not self.__Rabbits[r].IsFemale():
        Males = True
    return Males

  def Inspect(self):
    """
    Prints how many times the game has advanced, with the number of rabbits still alive.
    """
    print("Periods Run", self.__PeriodsRun, "Size", self.__RabbitCount)

  def ListRabbits(self):
    """
    Lists details of each rabbit if there are any rabbits still alive
    """
    if self.__RabbitCount > 0:
      for r in range (0, self.__RabbitCount):
        self.__Rabbits[r].Inspect()

class Animal:
  _ID = 1

  def __init__(self, AvgLifespan, AvgProbabilityOfDeathOtherCauses, Variability):
    """
    Animal is a generic class with properties shared by all animals.

    Args:
        AvgLifespan (int): The average lifespan rate, set by us humans
        AvgProbabilityOfDeathOtherCauses (float): The average probability of death from other causes (non-fox)
        Variability (int): Something to do with chance/randomness in Warrens

    Attributes:
        _NaturalLifespan (int): How long Animal lives
        _ProbabilityOfDeathOtherCauses (int): Actual probability of death from other causes (non-fox)
        _IsAlive (bool): set to false when deded
        _ID (int): set to 1 by default, see ln 547, then with every new Animal it increases by 1, see ln 570
        _Age (int): starts at 0
    """
    self._NaturalLifespan = int(AvgLifespan * self._CalculateRandomValue(100, Variability) / 100)
    self._ProbabilityOfDeathOtherCauses = AvgProbabilityOfDeathOtherCauses * self._CalculateRandomValue(100, Variability) / 100
    self._IsAlive = True
    self._ID = Animal._ID
    self._Age = 0
    Animal._ID += 1

  def CalculateNewAge(self):
    """
    Increases age of animal, 'kills' animal if now older than self._NaturalLifespan
    """
    self._Age += 1
    if self._Age >= self._NaturalLifespan:
      self._IsAlive = False

  def CheckIfDead(self): 
    """
    Getter for self._IsAlive

    Returns:
      bool: True if alive, otherwise False
    """
    return not self._IsAlive

  def Inspect(self):
    """
    Prints animal's ID, Age, Lifespan, and probability of death of other causes
    """
    print("  ID", self._ID, "", end = "")
    print("Age", self._Age, "", end = "")
    print("LS", self._NaturalLifespan, "", end = "")
    print("Pr dth", round(self._ProbabilityOfDeathOtherCauses, 2), "", end = "")

  def CheckIfKilledByOtherFactor(self):
    """
    Kills animals based on chance, using self._ProbabilityOfDeathOtherCauses

    Returns:
      bool: True if killed, otherwise False
    """
    if random.randint(0, 100) < self._ProbabilityOfDeathOtherCauses * 100:
      self._IsAlive = False
      return True
    else:
      return False

  def _CalculateRandomValue(self, BaseValue, Variability):
    """
    Calculates a pseudo-random value for Variability

    Args:
      BaseValue (int): ???
      Variability (int): Something to do with chance/randomness in Warrens
    
    Returns:
      int: random value based on BaseValue and Variability
    """
    return BaseValue - (BaseValue * Variability / 100) + (BaseValue * random.randint(0, Variability * 2) / 100)

class Fox(Animal):
  def __init__(self, Variability):
    """
    Fox is an Animal with some funky extras

    Args:
        Variability (int): Something to do with chance/randomness in Warrens

    Attributes:
        __DEFAULT_LIFE_SPAN (int): Constant that sets lifespan
        __DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES (float): Constant for Animal's probability of death by other causes (non-fox)
        __FoodUnitsNeeded (int): Random number defining how many food units are required to stay alive
        __FoodUnitsConsumedThisPeriod (int): Counter for food units consumed
    """
    self.__DEFAULT_LIFE_SPAN = 7
    self.__DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES = 0.1
    super(Fox, self).__init__(self.__DEFAULT_LIFE_SPAN, self.__DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES, Variability)
    self.__FoodUnitsNeeded = int(10 * self._CalculateRandomValue(100, Variability) / 100)
    self.__FoodUnitsConsumedThisPeriod  = 0

  def AdvanceGeneration(self, ShowDetail):
    """
    Advances foxes by, um, killing them (if they haven't eaten)
    """
    if self.__FoodUnitsConsumedThisPeriod == 0:
      self._IsAlive = False
      if ShowDetail:
        print("  Fox dies as has eaten no food this period.")
    else:
      if self.CheckIfKilledByOtherFactor():
        self._IsAlive = False
        if ShowDetail:
          print("  Fox killed by other factor.")
      else:
        if self.__FoodUnitsConsumedThisPeriod < self.__FoodUnitsNeeded:
          self.CalculateNewAge()
          if ShowDetail:
            print("  Fox ages further due to lack of food.")
        self.CalculateNewAge()
        if not self._IsAlive:
          if ShowDetail:
            print("  Fox has died of old age.")

  def ResetFoodConsumed(self):
    """
    (Re)Setter for self.__FoodUnitsConsumedThisPeriod
    """
    self.__FoodUnitsConsumedThisPeriod = 0

  def ReproduceThisPeriod(self): 
    """
    Advises on whether Foxes should reproduce based on probability constant

    Notes:
      Could move the attribute to the Animal or Fox class as a parameter, so you could vary the reproduction rate?

    Attributes:
      REPRODUCTION_PROBABILITY (float): probability of love-making ;)

    Returns:
      bool: True if period should feature reproduction, otherwise False
    """
    REPRODUCTION_PROBABILITY  = 0.25
    if random.randint(0, 100) < REPRODUCTION_PROBABILITY * 100:
      return True
    else:
      return False

  def GiveFood(self, FoodUnits):
    """
    Adds specified number of units to self.__FoodUnitsConsumedThis period, in effect "eating"

    Args:
      FoodUnits (int): Number of units to "consume"
    """
    self.__FoodUnitsConsumedThisPeriod = self.__FoodUnitsConsumedThisPeriod + FoodUnits
  
  def Inspect(self):
    """Overrides Animal.Inspect(), also printing the food the fox needs and how many units it has eaten"""
    super(Fox, self).Inspect()
    print("Food needed", self.__FoodUnitsNeeded, "", end = "")
    print("Food eaten", self.__FoodUnitsConsumedThisPeriod, "", end = "")
    print()

class Genders(enum.Enum):
  """
  Only two genders?????????

  Notes:
    You may be asked to expand this to include more genders or add properties for genders?
  Attributes:
    Male (enum): Wow.
    Female (enum): Seriously not funny, AQA
  """
  Male = 1
  Female = 2
    
class Rabbit(Animal):
  def __init__(self, Variability, ParentsReproductionRate = 1.2):
    """
    Rabbit is an Animal with some funky extras (but spoiler, they're weak AF)

    Args:
        Variability (int): Something to do with chance/randomness in Warrens
        ParentsReproductionRate (float, optional): Reproduction rate of Rabbit's parents

    Attributes:
        __DEFAULT_LIFE_SPAN (int): Constant that sets lifespan
        __DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES (float): Constant for Animal's probability of death by other causes (non-fox)
        __Gender (enum): Instance of Gender class
    """
    self.__DEFAULT_LIFE_SPAN = 4
    self.__DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES  = 0.05
    super(Rabbit, self).__init__(self.__DEFAULT_LIFE_SPAN, self.__DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES, Variability)
    self.__ReproductionRate = ParentsReproductionRate * self._CalculateRandomValue(100, Variability) / 100
    if random.randint(0, 100) < 50:
      self.__Gender = Genders.Male
    else:
      self.__Gender = Genders.Female

  def Inspect(self):
    """Overrides Animal.Inspect(), also printing the food the reproduction rate and the gender of the rabbit"""
    super(Rabbit, self).Inspect()
    print("Rep rate", round(self.__ReproductionRate, 1), "", end = "")
    if self.__Gender == Genders.Female:
      print("Gender Female")
    else:
      print("Gender Male")
    
  def IsFemale(self):
    """
    Checks if self.__Gender is Female
    
    Returns:
      bool: True if Rabbit is female, otherwise False
    """
    if self.__Gender == Genders.Female:
      return True
    else:
      return False
    
  def GetReproductionRate(self):
    """Getter for self.__ReproductionRate""" 
    return self.__ReproductionRate

def Main():
  """
  Starts simulation with defined (or inputted) settings

  Attributes:
    MenuOption (int): Choice, overriden by inputted Choice
    LandscapeSize (int)
    InitialWarrenCount (int)
    InitialFoxCount (int)
    Variability (int)
    FixedInitialLocations (bool)
  """
  MenuOption = 0
  while MenuOption != 3:
    print("Predator Prey Simulation Main Menu")
    print()
    print("1. Run simulation with default settings")
    print("2. Run simulation with custom settings")
    print("3. Exit")
    print()
    MenuOption = int(input("Select option: "))
    if MenuOption == 1 or MenuOption == 2:
      if MenuOption == 1:
        LandscapeSize = 15
        InitialWarrenCount = 5
        InitialFoxCount = 5
        Variability = 0
        FixedInitialLocations = True
      else:
        LandscapeSize = int(input("Landscape Size: "))
        InitialWarrenCount = int(input("Initial number of warrens: "))
        InitialFoxCount = int(input("Initial number of foxes: "))
        Variability = int(input("Randomness variability (percent): "))
        FixedInitialLocations = False
      Sim = Simulation(LandscapeSize, InitialWarrenCount, InitialFoxCount, Variability, FixedInitialLocations)
  input()

if __name__ == "__main__":
  Main()
