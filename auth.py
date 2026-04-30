# auth.py — In-Memory Authentication Manager

class AuthManager:
    def __init__(self):
        self.users = {
            "superadmin": {
                "password":   "superadmin123",
                "role":       "Super Admin",
                "first_name": "Super",
                "last_name":  "Admin",
            },
            "admin": {
                "password":   "admin123",
                "role":       "Admin",
                "first_name": "Christian Joseph",
                "last_name":  "Aquino",
            },
            "teacher": {
                "password":   "teacher123",
                "role":       "Teacher",
                "first_name": "Demo",
                "last_name":  "Teacher",
            },
        }
        self.current_user = None

    def login(self, username, password):
        username = username.strip()
        password = password.strip()
        if not username:
            return False, None, "Username is required."
        if not password:
            return False, None, "Password is required."
        if username not in self.users:
            return False, None, f'Username "{username}" not found.'
        if self.users[username]["password"] != password:
            return False, None, "Incorrect password. Please try again."
        self.current_user = username
        return True, self.users[username]["role"], "OK"

    def register(self, first_name, last_name, username, password, confirm):
        first_name = first_name.strip()
        last_name  = last_name.strip()
        username   = username.strip()
        password   = password.strip()
        confirm    = confirm.strip()
        if not all([first_name, last_name, username, password, confirm]):
            return False, "Please fill in all fields."
        if password != confirm:
            return False, "Passwords do not match."
        if username in self.users:
            return False, "Username already exists."
        self.users[username] = {
            "password":   password,
            "role":       "Staff",
            "first_name": first_name,
            "last_name":  last_name,
        }
        return True, "Account created successfully!"

    def register_admin(self, first_name, last_name, username, password, confirm,
                       middle_name="", birth_date="", age="", gender="",
                       mobile="", email="", barangay="", address=""):
        first_name = first_name.strip()
        last_name  = last_name.strip()
        username   = username.strip()
        if not first_name or not last_name:
            return False, "First Name and Surname are required."
        if not password:
            return False, "Password is required."
        if password != confirm:
            return False, "Passwords do not match."
        if not username:
            import random, string
            username = (first_name[:2] + last_name[:3]).lower() + \
                       ''.join(random.choices(string.digits, k=3))
        if username in self.users:
            return False, f'Username "{username}" already exists.'
        self.users[username] = {
            "password":    password,
            "role":        "Admin",
            "first_name":  first_name,
            "last_name":   last_name,
            "middle_name": middle_name,
            "birth_date":  birth_date,
            "age":         age,
            "gender":      gender,
            "mobile":      mobile,
            "email":       email,
            "barangay":    barangay,
            "address":     address,
        }
        return True, f"Admin '{username}' registered successfully!"

    def logout(self):
      self.current_user = None

    def get_counts(self):
        admins   = sum(1 for u in self.users.values() if u["role"] == "Admin")
        teachers = sum(1 for u in self.users.values() if u["role"] == "Teacher")
        staff    = sum(1 for u in self.users.values() if u["role"] == "Staff")
        return admins, teachers, staff