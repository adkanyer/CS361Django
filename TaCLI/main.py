from TaCLI import UI, Environment, TextFileInterface

# create an instance of the UI
environment = Environment.Environment(TextFileInterface.TextFileInterface(), DEBUG=True)
ui = UI.UI(environment)

# TextFileInterface.TextFileInterface().create_account("tyler", "a", "supervisor")
# create a user to determine if someone is logged onto the system
# if CurrentUser is none: no one is logged on
# if CurrentUser is not None, someone is logged on.

# set application to running
running = True
while running:
    s = input("Enter a command: ")

    # stop and quit application
    if s == "q":
        running = False
    else:
        # take input and attempt to change into a command
        response = ui.command(s)
        print(response)

print("Program has been terminated.")

