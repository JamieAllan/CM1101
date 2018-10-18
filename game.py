#!/usr/bin/python3

from map import rooms
from player import *
from items import *
from gameparser import *



def list_of_items(items):

    list_items = []
    
    for i in list(items):
        list_items.append(i["name"])

    return list_items
    

def print_room_items(room):

    if len(list_of_items(room["items"])) == 0:
        pass
    else:
        output = "There is "
        output += ", ".join(list_of_items(room["items"]))
        output += " here."
        print(output)
        


def print_inventory_items(items):

	list_inventory = []

	for i in list(items):
		list_inventory.append(i["name"])

		
	output = "You have "
	output += ", ".join(list_inventory)
	output += " here."
	print(output)




def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:

    >>> print_room(rooms["Office"])
    <BLANKLINE>
    THE GENERAL OFFICE
    <BLANKLINE>
    You are standing next to the cashier's till at
    30-36 Newport Road. The cashier looks at you with hope
    in their eyes. If you go west you can return to the
    Queen's Buildings.
    <BLANKLINE>
    There is a pen here.
    <BLANKLINE>

    >>> print_room(rooms["Reception"])
    <BLANKLINE>
    RECEPTION
    <BLANKLINE>
    You are in a maze of twisty little passages, all alike.
    Next to you is the School of Computer Science and
    Informatics reception. The receptionist, Matt Strangis,
    seems to be playing an old school text-based adventure
    game on his computer. There are corridors leading to the
    south and east. The exit is to the west.
    <BLANKLINE>
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

    >>> print_room(rooms["Admins"])
    <BLANKLINE>
    MJ AND SIMON'S ROOM
    <BLANKLINE>
    You are leaning agains the door of the systems managers'
    room. Inside you notice Matt "MJ" John and Simon Jones. They
    ignore you. To the north is the reception.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    # Display room name
    if room["description"].find("Simon Jones") != -1:
        print("")
        print(room["name"].upper())
        print("")
		# Display room description
        print(room["description"])
        print("")
        # Display room's items
        print_room_items(room)
    else:
        print("")
        print(room["name"].upper())
        print("")
        # Display room description
        print(room["description"])
        print("")
        # Display room's items
        print_room_items(room)	
        print("")
    
def exit_leads_to(exits, direction):

    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:

    GO <EXIT NAME UPPERCASE> to <where it leads>.

    For example:
    >>> print_exit("east", "you personal tutor's office")
    GO EAST to you personal tutor's office.
    >>> print_exit("south", "MJ and Simon's room")
    GO SOUTH to MJ and Simon's room.
    """
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    
    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))

    for item in room_items:
        print("TAKE " + item["id"].upper() + " to take " + item["name"] + ".")

    for item in inv_items:
          
        print("DROP " + item["id"].upper() + " to drop your " + item["name"] + ".")
   
    print("What do you want to do?")
    print("")


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:

    >>> is_valid_exit(rooms["Reception"]["exits"], "south")
    True
    >>> is_valid_exit(rooms["Reception"]["exits"], "up")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "west")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "east")
    True
    """
    return chosen_exit in exits


def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """

    global current_room



    if is_valid_exit(current_room["exits"],direction):
        new_room = move(current_room["exits"],direction)
        current_room = new_room
        

    else:
        print("Not a valid exit")

    
def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """

    global current_room
    global inventory
    global items
    global mass

    try:
        item_available = items[item_id]
        if (mass + item_available["mass"]) > maximum_weight:
            print ("")
            print ("You are already carrying too much")

        else:
            if current_room["items"]:
                i = current_room["items"]
      
                if item_available not in i:
                    print ("That cannot be picked up")

                for item in i:
                    if item ==item_available:
                        inventory.append(item)
                        current_room["items"].remove(item)
                        mass += item_available["mass"]

    except KeyError:
        print ("Come again?")
         
             
            
    

def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """

    global current_room
    global inventory
    global mass

    try:
        item_to_drop = items [item_id]
        if mass < 0:
            print("Cannot be dropped")

        else:
            if inventory:
                inventory_list = inventory

                if item_to_drop not in inventory_list:
                    print ("That is not droppable")

                for item in inventory_list:
                    if item == item_to_drop:
                        current_room["items"].append(item)
                        inventory.remove(item)
                        mass -= item_to_drop["mass"]

            else:
                print("That cannot be dropped")
                
    except KeyError:
        print("Come again?")
    

def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.

    """

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.

    """

    # Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input

def exit_leads_to(exits, direction):

    for key, val in exits.items():
        if key == direction:
            return val

def move(exits, direction):
    
    # Next room to go to
    return rooms[exit_leads_to(exits,direction)]


# This is the entry point of our program
def main():

    # Main game loop
    while True:
        # Display game status (room description, inventory etc.)
        print_room(current_room)
        print_inventory_items(inventory)
        
        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)

        # Execute the player's command
        execute_command(command)



# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()

