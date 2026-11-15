# Override Methods in Python and Dunder Methods / Exploring dunder methods
class Employee:
    def __init__(self,name,employee_id,salary):
        self.name=name
        self.employee_id=employee_id
        self.salary=salary
    
    def __str__(self):
        return f"Employee: {self.name} - Employee ID: {self.employee_id}"   

    def __repr__(self):
        return f"""Employee: {self.name}- Employee ID:{self.employee_id},
         Salary:{self.salary})"""

    def __eq__(self,other):
        return self.employee_id==other.employee_id
    
    def __lt__(self,other):
        return self.salary<other.salary




class Manager(Employee):
    def __init__(self,name,employee_id,salary,team_size):
        super().__init__(name,employee_id,salary)
        self.team_size=team_size

    def __str__(self):
        base_str=super().__str__()
        return f"{base_str} - Managing a team of {self.team_size} employees"

mgr1=Manager("Mike",'M123',100000,10)


emp1=Employee("Alice",'E123',75000)
emp2=Employee("Bob",'E124',80000)
emp3=Employee("Charlie",'E123',90000)

#print(f"Are emp1 and emp2 equal? {emp1==emp2}")
# print(f"Are emp1 and emp3 equal? {emp1==emp3}")
#print()
staff=[emp1,emp2,emp3]

print("\nSorted staff by salary:")

for employee in staff:
    print(employee)
# outputs: Employee: Alice - Employee ID: E123
# outputs: Employee: Bob - Employee ID: E124
# outputs: Employee: Charlie - Employee ID: E123
# outputs: Manager: Bob - Manager ID: M456 - Managing a team of 10 employees