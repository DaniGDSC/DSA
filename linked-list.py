#add new element at the beginning of the linked-list

class Student:
    def __init__(self, student_id=0):
        self.id = student_id
        self.next = None

class StudentList:
    def __init__(self):
        self.Head = Student()
        self.Current = None
        self.Tail = None
        
    def add_student(self, student_id):
        new_student = Student(student_id)
        if self.Current is None:
            self.Head.next = new_student
            self.Current = new_student
            self.Tail = new_student
        else: 
            self.Current.next = new_student
            self.Current = new_student
            self.Tail = new_student
            
    def insert_beginning(self, student_id):
        new_student = Student(student_id)
        new_student.next = self.Head.next
        self.Head.next = new_student
        if self.Current is None:
            self.Current = new_student
        if self.Tail is None:
            self.Tail = new_student
            
    def print_list(self):
        temp = self.Head.next
        while temp is not None:
            print(temp.id, end=' ')
            temp = temp.next    
        print()

if __name__ == "__main__":
    sl = StudentList()
    sl.add_student(56)
    sl.add_student(78)
    sl.add_student(12)
    sl.insert_beginning(99)
    sl.print_list()
