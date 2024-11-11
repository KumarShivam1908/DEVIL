# main.py
from WrapperClass.LLMS.Florence2b import Florence2Detector
from WrapperClass.LLMS.webAuto import WebDevAutomator
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def computer_vision_menu():
    """Handle Computer Vision tasks."""
    detector = Florence2Detector()
    
    while True:
        clear_screen()
        print("\nComputer Vision Tasks:")
        print("1. Object Detection")
        print("2. Segmentation")
        print("3. Back to Main Menu")
        
        task = input("\nEnter choice (1-3): ")
        
        if task == '3':
            break
            
        if task in ['1', '2']:
            print("\nProcess Type:")
            print("1. Image")
            print("2. Video")
            process_type = input("\nEnter type (1-2): ")
            
            if task == '1':  # Object Detection
                if process_type == '1':
                    image_path = input("\nEnter image path: ")
                    detector.process_image_detection(image_path)
                elif process_type == '2':
                    video_path = input("\nEnter video path: ")
                    detector.process_video_detection(video_path, frame_step=5)
                    
            elif task == '2':  # Segmentation
                text_input = input("\nEnter text to segment (e.g., 'a person'): ")
                if process_type == '1':
                    image_path = input("\nEnter image path: ")
                    detector.process_image_segmentation(image_path, text_input)
                elif process_type == '2':
                    video_path = input("\nEnter video path: ")
                    detector.process_video_segmentation(video_path, text_input, frame_step=5)
        
        input("\nPress Enter to continue...")

def web_development_menu():
    """Handle Web Development tasks."""
    automator = WebDevAutomator()
    
    while True:
        clear_screen()
        print("\nWeb Development Tasks:")
        print("1. Create HTML/CSS/JS Project")
        print("2. Create React Project")
        print("3. Back to Main Menu")
        
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            
            if choice == 3:
                break
                
            if choice in [1, 2]:
                instructions = input("Enter project instructions: ")
                if choice == 1:
                    automator.create_html_project(instructions)
                else:
                    automator.create_react_project(instructions)
                    
            input("\nPress Enter to continue...")
                
        except ValueError:
            print("Please enter a valid number!")
            input("\nPress Enter to continue...")

def main():
    while True:
        clear_screen()
        print("\n=== AI Task Automation System ===")
        print("\nMain Menu:")
        print("1. Computer Vision Tasks")
        print("2. Web Development Tasks")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            computer_vision_menu()
        elif choice == '2':
            web_development_menu()
        elif choice == '3':
            print("\nThank you for using the system!")
            break
        else:
            print("\nInvalid choice! Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()