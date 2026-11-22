"""
Exercice: Modify the code so this prints "In class D"

original code for clase E:
class E(B,C,D):   #
  def do_action(self):
    super().do_action()

"""

class A:
  def do_action(self):
   print("In class A")

class B(A):
  def do_action(self):
   print("In class B")

class C(A):
   def do_action(self):
    print("In class C")

class D(A):
    def do_action(self):
      print("In class D")

class E(D,B,C):   # 
  def do_action(self):
    super().do_action()

r=E()
r.do_action() 
