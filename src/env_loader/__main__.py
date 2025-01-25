from pathlib import Path
import os
from dotenv import load_dotenv

class EnvLoader:
    def __init__(self, project_name, required_vars):
        self.project_name = project_name
        self.required_vars = required_vars
        self.get_env_file_path()
        self.check_or_create_env()

    def get_env_file_path(self):
        if os.name == "nt":  # Windows
            self.config_dir = Path(os.getenv("APPDATA", "C:\\Users\\Default\\AppData\\Roaming")) / self.project_name
        else:  # Linux/macOS
            self.config_dir = Path(os.getenv("XDG_CONFIG_HOME", "~/.config")).expanduser() / self.project_name

        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_custom_env(self):
        # Load the .env file from the custom location
        self.env_file = self.config_dir / ".env"
        if self.env_file.exists():
            load_dotenv(self.env_file)  # Explicitly pass the path to the .env file
            print(f"✅ Loaded environment variables from {self.config_dir}")
            return True
        else:
            print(f"⚠️  No .env file found at {self.config_dir}. Please create one.")
            return False

    def check_or_create_env(self):
        if not self.load_custom_env():
            user_input = input("Would you like to create one now? (y/n): ").strip().lower()

            if user_input == "y":
                # Open the .env file for writing
                with open(self.env_file, "w") as env_file:
                    print(f"✅ .env file created at {os.path.abspath(self.config_dir)}")

                    # Prompt the user for each variable
                    for var_name, default_value in self.required_vars:
                        user_value = input(
                            f"Please set the value for {var_name} (default: {default_value}): "
                        ).strip()

                        # Use the default if the user provides no input
                        if not user_value:
                            user_value = default_value

                        # Write the variable to the .env file
                        env_file.write(f"{var_name}={user_value}\n")
                        print(f"✅ {var_name} set.")

                    print("All variables have been set.")
                print("Edit this file with your configuration.")
                self.load_custom_env()
            else:
                print("❌ Running in offline mode. Use command `connect` to go to online mode with database")
                exit(1)  # Exit if the user does not want to create the file


