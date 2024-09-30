#add new element at the beginning of the linked-list

class Student:
    def __init__(self, student_id=0):
        self.id = student_id
        self.next = None

class StudentList:
    def __init__(self):
        self.head = None
        self.current = None
        self.tail = None
        
    def add_student(self, student_id):
        new_student = Student(student_id)
        if self.current is None:
            self.head = new_student
            self.current = new_student
            self.tail = new_student
        else: 
            self.current.next = new_student
            self.current = new_student
            self.tail = new_student
            
    def insert_beginning(self, student_id):
        new_student = Student(student_id)
        new_student.next = self.head
        self.head = new_student
        if self.current is None:
            self.current = new_student
        if self.tail is None:
            self.tail = new_student
            
    def print_list(self):
        temp = self.head
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
