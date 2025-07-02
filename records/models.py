from django.db import models

# Many-to-one: A company can have many employees
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Employee model: Belongs to one company

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    join_date = models.DateField()
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employees'
    )

    def __str__(self):
        return f"{self.name} - {self.email}"


# One-to-one: Each employee has one profile
class Profile(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    bio = models.TextField()
    linkedin = models.URLField()

    def __str__(self):
        return f"{self.employee.name}'s Profile"

# Many-to-many: Projects can have many employees, and vice versa
class Project(models.Model):
    name = models.CharField(max_length=100)
    employees = models.ManyToManyField(Employee, related_name='projects')

    def __str__(self):
        return self.name
    
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField()

    def __str__(self):
        return self.title

