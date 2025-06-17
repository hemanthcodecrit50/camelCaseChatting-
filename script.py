from pynput import keyboard
import subprocess
import time

# Flag to avoid infinite loop
is_processing = False

def to_camel_case(text):
    words = text.split()
    if not words:
        return ""
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

def get_clipboard():
    # Get clipboard content using xclip
    process = subprocess.Popen(
        ['xclip', '-selection', 'clipboard', '-o'],
        stdout=subprocess.PIPE
    )
    output, _ = process.communicate()
    return output.decode('utf-8')

def set_clipboard(text):
    # Set clipboard content using xclip
    process = subprocess.Popen(
        ['xclip', '-selection', 'clipboard'],
        stdin=subprocess.PIPE
    )
    process.communicate(input=text.encode('utf-8'))

def on_enter(key):
    global is_processing

    # Check if the pressed key is the Enter key
    if key == keyboard.Key.enter:
        # Prevent repeated triggering (set flag to True to indicate processing)
        if is_processing:
            return  # Skip processing if it's already in process

        is_processing = True  # Set flag to True to prevent re-entry

        time.sleep(0.1)  # Small delay to capture typed text

        # Simulate Ctrl+A to select all text
        controller = keyboard.Controller()
        controller.press(keyboard.Key.ctrl)
        controller.press('a')
        controller.release('a')
        controller.release(keyboard.Key.ctrl)

        time.sleep(0.1)  # Wait for selection
        # Simulate Ctrl+C to copy the selected text
        controller.press(keyboard.Key.ctrl)
        controller.press('c')
        controller.release('c')
        controller.release(keyboard.Key.ctrl)

        time.sleep(0.1)  # Wait for clipboard update
        text = get_clipboard()
        
        camel_case_text = to_camel_case(text)
        
        print(camel_case_text)

        if text.strip():  # If there's text, replace it with camelCase
            set_clipboard(camel_case_text)
            # Simulate Ctrl+V to paste the camelCase text
            controller.press(keyboard.Key.ctrl)
            controller.press('v')
            controller.release('v')
            controller.release(keyboard.Key.ctrl)

            # Simulate pressing Enter to send the message
            controller.press(keyboard.Key.enter)
            controller.release(keyboard.Key.enter)

        is_processing = False  # Reset flag after processing

# Start listening for keyboard events
with keyboard.Listener(on_press=on_enter) as listener:
    print("🔥 WhatsApp Auto camelCase is running... Press ESC to exit.")

    # Keep the script running until ESC is pressed
    listener.join()
