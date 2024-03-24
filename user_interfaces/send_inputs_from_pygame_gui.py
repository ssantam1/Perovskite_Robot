import gui_test  # Import the other Python file

# Inside the event handling part
if event.key == pygame.K_RETURN:
    # Pass the text to a function in the other file for processing
    gui_test.process_input(text)
    text = ''
