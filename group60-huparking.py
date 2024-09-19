import math
import pygame


#defines the parking lot
#defines the areas for closest parking
def initialise_system():
  global parking_lot
  global cars_entered
  global parking_dict
  global area_dict
  parking_lot = [["Not Taken" for j in range(8)] for i in range(8)]
  cars_entered = []
  parking_dict = {}
  for i in range(8):
    for j in range(8):
      parking_dict[(i, j)] = parking_lot[i][j]

  area_dict= {}
  print("Hard set the four areas of interests A, B, C, D. ")
  for i in range(4):
    print(f"Please define area {chr(65+i)}")
    areaname = input("Enter the name of the area: ")
    x_cord = int(input("Enter the x coordinate of the area: "))
    while x_cord < 0 or x_cord > 7:
      print("Please enter a valid x coordinate.")
      x_cord = int(input("Enter the x coordinate of the area: "))
    y_cord = int(input("Enter the y coordinate of the area: "))
    while y_cord < 0 or y_cord > 7:
      print("Please enter a valid y coordinate.")
      y_cord = int(input("Enter the y coordinate of the area: "))
    area_dict[chr(65+i)] = [areaname, (x_cord, y_cord)]
#-----------------------------------------------------------------------------------

#checks the parking lot for free spaces
#prints free spaces if there are any otherwise prints "No parking spaces available"
#returns True if parking available and vice versa
def parking_full():
  free_space_counter = 0
  for i in range(len(parking_lot)):
    for j in range(len(parking_lot[0])):
      if parking_lot[i][j] == "Not Taken":
        free_space_counter += 1
  if free_space_counter == 0:
    print("Parking is full, Sorry!")
    return True
  else:
    print("There are", free_space_counter, "free spaces")
    return False
#-----------------------------------------------------------------------------------
def display_choose():
  free_slots = []
  for i in range(len(parking_lot)):
    print()
    for j in range(len(parking_lot[0])):
      if parking_lot[i][j] == "Not Taken":
        print("Free Spot", (i, j), end=" | ")
        free_slots.append((i, j))
      else:
        print("     Taken      ", end=" | ")
    print("")
    print()

  print("Enter the coordinates of the parking spot you want: ")
  spot_choosen = (int(input("Enter the row number ")), int(input("Enter the column number ")))
  while spot_choosen not in free_slots:
    print("Please enter a valid spot.")
    spot_choosen = (int(input("Enter the row number ")), int(input("Enter the column number ")))
  parking_lot[spot_choosen[0]][spot_choosen[1]] = user_num_plate
  parking_dict[spot_choosen] = user_num_plate
  cars_entered.append(user_num_plate)
  print("Your car has been parked succesfully in row", spot_choosen[0], "and column", spot_choosen[1])

  print_parking(spot_choosen[0], spot_choosen[1])


#-----------------------------------------------------------------------------------

#assigns the first free parking slot to the user
def random_park():
  global user_num_plate
  found = False
  row = 0
  col = 0
  while row  < len(parking_lot) and not found:
      while not found and col < len(parking_lot[0]):
          if parking_lot[row][col] == "Not Taken":
              parking_lot[row][col] = user_num_plate
              cars_entered.append(user_num_plate)
              parking_dict[(row, col)] = user_num_plate
              found = True
              print("Your car has been parked succesfully in row", row, "and column", col)

          col +=1
      row += 1

  print_parking(row-1, col-1)    
#-----------------------------------------------------------------------------------

#main parking function
#only works if parking available
#takes number plate input
#asks users which parking they would prefer and calls seperate functions to park car
#num plate has to be of this format:
#7 characters: first 3 alphabets, remaining 4 numbers
def enter_parking_lot():
  global user_num_plate
  if not parking_full():
    user_num_plate = input("Please enter your vehicle's number plate (3 alphabets followed by 4 numbers): ")
    while not user_num_plate[0:3].isalpha() or not user_num_plate[3:].isdigit() or len(user_num_plate) > 7 or user_num_plate in cars_entered:
      if user_num_plate in cars_entered:
        print("The entered number plate isnt unique please try again")
        user_num_plate = input("Please enter your vehicle's number plate: ")
      else:
        print("Invalid Number Plate Entered, Please try again.")
        print("the format for the number plate is: 3 alphabets followed by 4 numbers")
        user_num_plate = input("Please enter your vehicle's number plate: ")

    print("How would you like to park?")
    print("1. Do you want to pick your own spot?")
    print("2. Do you want to get assigned a random spot?")
    print("3. Do you want to park close to a specific area")
    park_option = int(input("Please enter your choice: "))
    while park_option < 1 or park_option > 3:
      print("Please enter a valid option")
      park_option = int(input("Please enter your choice: "))
    if park_option == 1:
      display_choose()
    elif park_option == 2:
      random_park()
    elif park_option == 3:
      global area_choice
      for k, v in area_dict.items():
        print(k,":",v[0], v[1])

      area_choice = input(("Please enter the area you would like to park in (Choose between A-D): "))
      area_choice = area_choice.upper()
      while area_choice not in ["A", "B", "C", "D"]:
        print("Please enter a valid area")
        area_choice = input(("Please enter the area you would like to park in (A, B, C, D): "))
      closest_parking(area_choice)
#-----------------------------------------------------------------------------------

#removes car from the parking lot
#removes car from the cars_entered list
#sets the dictionary value to "Not Taken"
def exit_parking():
  
  numberplate = input("Enter your plate number: ")
  while numberplate not in cars_entered:
    print("Incorrect plate number entered")
    numberplate = input("Enter your plate number: ")
  found = False
  row = 0
  col = 0

  for k, v in parking_dict.items():
    if v == numberplate:
      parking_lot[k[0]][k[1]] = "Not Taken"
      cars_entered.remove(numberplate)
      parking_dict[k] = "Not Taken"
      print("Your car has been removed successfully!")
      break

#-----------------------------------------------------------------------------------

#asks user to enter their number plate and prints the coordinates of their parking
def find_my_car():
  numberplate = input("Enter your plate number: ")
  while numberplate not in cars_entered:
    print("Incorrect plate number entered")
    numberplate = input("Enter your plate number.")
  for k, v in parking_dict.items():
    if v == numberplate:
      print("Your car is parked at:", k)
      y = k[0]
      x = k[1]
      break
  print_parking(y, x)



#------------------------------------------------------------------------------------
def print_parking(y, x):


  pygame.init()

  width = 390
  height = 710
  w,h = 0,0
  screen =   pygame.display.set_mode((width, height))


  run = True
  while run:

    for i in range(len(parking_lot)): 
        w = 0
        for j in range(len(parking_lot[0])):
          spot = pygame.Rect(w, h, 40, 80)
          if parking_lot[i][j] == "Not Taken":
            pygame.draw.rect(screen, (0,255,0), spot)
          elif i == y and j == x:
            pygame.draw.rect(screen, (0,0,255), spot)
          else:
            pygame.draw.rect(screen, (255,0,0), spot)
          w += 50
        h += 90

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          run = False

    pygame.display.update()
  pygame.quit()


#--------------------------------------------------------------------------------------

def closest_parking(area_choice):
  tuple = area_dict[area_choice][1]
  min = 10000
  x = tuple[0]
  y = tuple[1]
  print(tuple)
  x_pos = 0
  y_pos = 0
  col = 0
  row = 0
  found = False
  if parking_lot[x][y] == "Not Taken":
        parking_lot[x][y] = user_num_plate
        cars_entered.append(user_num_plate)
        parking_dict[(x, y)] = user_num_plate
        print("Your car has been parked in row", x, "and column", y)
  else:

    while col < len(parking_lot):
      row = 0
      while row < len(parking_lot[0]):
        if parking_lot[row][col] == "Not Taken":
          dist = math.sqrt((x - (row))**2 + (y - (col))**2)
          if min > dist:
             min = dist
             y_pos = row
             x_pos = col


        row += 1
      col += 1
    parking_lot[y_pos][x_pos] = user_num_plate
    cars_entered.append(user_num_plate)
    parking_dict[y_pos, x_pos] = user_num_plate
    print("Your car has been parked in row", y_pos, "and column", x_pos)

    print_parking(y_pos, x_pos)

#-----------------------------------------------------------------------------------

#the main domain options: park or remove or find your car
#the Mainmenu keeps printing and calling functions until the system is switched off using '-1'
def Mainmenu():
  choice = 0
  while choice != -1:
    print("Welcome to HU Parking! \nThe column and row numbers of this parking lot range from 0 - 7.  \n1:Enter a new vehicle \n2:Remove your vehicle \n3:Find my car \n-1: Exit code")
    try:
      choice = int(input("Please enter the number corresponding to what you want to do: "))
      while (choice < -1 or choice > 3):
        choice = int(input("Please ensure your number choice is one from the options: "))
      if choice == 1:
        enter_parking_lot()
      elif choice == 2 and len(cars_entered) > 0:
        exit_parking()
      elif choice == 3 and len(cars_entered) > 0:
        find_my_car()
      elif choice == -1:
        print("Thank you for using the HU parking app <3")
      elif (choice ==2 or choice == 3) and len(cars_entered) == 0:
        print("Please enter a car first")
    except:
      TypeError


initialise_system()
Mainmenu()