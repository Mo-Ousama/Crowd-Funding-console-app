import re
from datetime import datetime

# قائمة لتخزين بيانات المستخدمين والمشاريع
users = []
projects = []

# دالة لتسجيل مستخدم جديد
def register_user():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")
    phone = input("Enter mobile phone number (Egyptian format): ")

    # التأكد من تطابق الباسورد
    if password != confirm_password:
        print("Passwords do not match!")
        return

    # التحقق من رقم الهاتف المصري
    phone_regex = r'^01[0-2,5]{1}[0-9]{8}$'
    if not re.match(phone_regex, phone):
        print("Invalid phone number!")
        return

    # تخزين بيانات المستخدم
    users.append({
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone": phone
    })
    print("User registered successfully!")

# دالة لتسجيل الدخول
def login_user():
    email = input("Enter email: ")
    password = input("Enter password: ")
    
    for user in users:
        if user['email'] == email and user['password'] == password:
            print(f"Welcome back, {user['first_name']}!")
            return user
    print("Invalid email or password.")
    return None

# فئة تمثل مشروع
class Project:
    def __init__(self, title, details, target, start_date, end_date, owner):
        self.title = title
        self.details = details
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.owner = owner

# دالة لإنشاء مشروع جديد
def create_project(user):
    title = input("Enter project title: ")
    details = input("Enter project details: ")
    target = float(input("Enter target amount (EGP): "))
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    # التحقق من صحة التواريخ
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        if start_date >= end_date:
            print("End date must be after start date!")
            return
    except ValueError:
        print("Invalid date format!")
        return

    # إنشاء وتخزين المشروع
    project = Project(title, details, target, start_date, end_date, user)
    projects.append(project)
    print("Project created successfully!")

# دالة لعرض جميع المشاريع
def view_projects():
    if not projects:
        print("No projects available.")
        return
    for project in projects:
        print(f"Title: {project.title}, Target: {project.target} EGP, Start: {project.start_date}, End: {project.end_date}, Owner: {project.owner['first_name']} {project.owner['last_name']}")

# دالة لتعديل مشروع
def edit_project(user):
    project_title = input("Enter the title of the project you want to edit: ")
    for project in projects:
        if project.title == project_title and project.owner == user:
            project.details = input("Enter new details: ")
            print("Project updated successfully!")
            return
    print("Project not found or you don't have permission to edit it.")

# دالة لحذف مشروع
def delete_project(user):
    project_title = input("Enter the title of the project you want to delete: ")
    for project in projects:
        if project.title == project_title and project.owner == user:
            projects.remove(project)
            print("Project deleted successfully!")
            return
    print("Project not found or you don't have permission to delete it.")

# دالة للبحث عن المشاريع بالتاريخ
def search_projects_by_date():
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format!")
        return

    found_projects = [project for project in projects if start_date <= project.start_date <= end_date]
    if not found_projects:
        print("No projects found in this date range.")
        return
    for project in found_projects:
        print(f"Title: {project.title}, Target: {project.target} EGP, Start: {project.start_date}, End: {project.end_date}")

# الدالة الرئيسية لتشغيل التطبيق
def main():
    logged_in_user = None  # حالة المستخدم الغير مسجل الدخول
    while True:
        print("\n1. Register User")
        print("2. Login User")
        if logged_in_user:  # إظهار خيارات المشاريع فقط عند تسجيل الدخول
            print("3. Create Project")
            print("4. View Projects")
            print("5. Edit Project")
            print("6. Delete Project")
            print("7. Search Projects by Date")
        print("8. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            logged_in_user = login_user()
        elif logged_in_user and choice == '3':
            create_project(logged_in_user)
        elif logged_in_user and choice == '4':
            view_projects()
        elif logged_in_user and choice == '5':
            edit_project(logged_in_user)
        elif logged_in_user and choice == '6':
            delete_project(logged_in_user)
        elif logged_in_user and choice == '7':
            search_projects_by_date()
        elif choice == '8':
            print("Exiting the application.")
            break
        else:
            if not logged_in_user:
                print("You need to login first to manage projects.")
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()