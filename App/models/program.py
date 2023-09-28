class Program:
    id = 1

    def __init__(self, file_path):

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.name = lines[0].strip()  # First line is the program name
                self.course_codes = [code.strip() for code in lines[1:]]  # Subsequent lines are course codes
                self.id = Program.latest_programmeID  # Assign the latest ID
                Program.id += 1  # Increment the latest ID for the next instance

        except FileNotFoundError:
            print("File not found.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_json(self):
        return{
            'Program ID:': self.id,
            'Program Name: ': self.name,
            'Program Courses: ': self.course_codes
        }
       