import datetime
import webbrowser
import os
def greet():
    print("👋 Hi, I’m your assistant bot. How can I help you  today?")
def show_time():
    now = datetime.datetime.now()
    print(f"⏰ Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
def open_google():
    webbrowser.open("https://www.google.com")

# requires security update risk of shell injection 
def run_command():
    cmd = input("Enter the shell command to run: ") 
    os.system(cmd)
def main():
    greet()
    while True:
       print("\n1. Show time\n2. Open Google\n3. Run command\n4. Exit")
       choice = input("Enter your choice: ")
       if choice == '1':
            show_time()
       elif choice == '2':
            open_google()
       elif choice == '3':
            run_command()
       elif choice == '4': 
            print("👋 Bye!")
            break
       else: 
            print("❗ Invalid option, try again.")


if __name__ == "__main__":
     main()
