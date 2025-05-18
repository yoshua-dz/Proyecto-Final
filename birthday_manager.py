import csv
from datetime import datetime 
import os

class Birthday:
    def __init__(self, name, birthdate, email, message=None):
        self.name = name
        self.birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        self.email = email
        self.message = message 
    
    def to_list(self):
        return [self.name, self.birthdate.strftime("%Y-%m-%d"), self.email, self.message or ""]

    def days_until_birthday(self):
        today = datetime.today()
        next_birthday = self.birthdate.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1) #si ya pasó, toma el siguiente
        return (next_birthday - today).days

class BirthdayManager:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_birthdays(self):
        birthdays = []
        if not os.path.exists(self.filepath):
            return birthdays
        with open(self.filepath, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                msg = row.get("message", "")
                birthdays.append(Birthday(row["name"], row["birthdate"], row["email"], msg))
        return birthdays

    def save_birthday(self, birthday):
        birthdays = self.load_birthdays()
        updated = False
        for i, b in enumerate(birthdays):
            if b.email == birthday.email:
                birthdays[i] = birthday
                updated = True
                break
        if not updated:
            birthdays.append(birthday)

        with open(self.filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "birthdate", "email", "message"])
            for b in birthdays:
                writer.writerow(b.to_list())

    def delete_birthday(self, email_to_delete):
        birthdays = self.load_birthdays()
        birthdays = [b for b in birthdays if b.email != email_to_delete]
        with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'birthdate', 'email'])  # Encabezado
            for b in birthdays:
                writer.writerow([b.name, b.birthdate.strftime("%Y-%m-%d"), b.email])

