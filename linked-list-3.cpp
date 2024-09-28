#include <iostream>
using namespace std;

class student {
public:
    int ID; // Student ID
    student *next; // Pointer to the next student in the list

    student(int id = 0) : ID(id), next(NULL) {} // Constructs a new student with the given ID.
};

class StudentList {
private:
    student *HeadStudent; // Pointer to the head of the list
    student *CurrentStudent; // Pointer to the current student in the list

public:
    StudentList() : HeadStudent(new student()), CurrentStudent(NULL) {} // Constructs a new empty StudentList.

    // Adds a new student with the given ID to the end of the list.
    void Add_Student(int studentid) {
        student *NewStudent = new student(studentid);
        if (CurrentStudent == NULL) {
            HeadStudent->next = NewStudent;
            CurrentStudent = NewStudent;
        } else {
            CurrentStudent->next = NewStudent;
            CurrentStudent = NewStudent;
        }
    }

    // Inserts a new student with the given ID at the beginning of the list.
    void InsertBeginning(int studentid) {
        student *NewStudent = new student(studentid);
        NewStudent->next = HeadStudent->next;
        HeadStudent->next = NewStudent;
        if (CurrentStudent == NULL) {
            CurrentStudent = NewStudent;
        }
    }

    // Deletes all elements containing the given value
    void DeleteElement(int value) {
        student *current = HeadStudent;
        student *prev = NULL;
        
        while (current != NULL) {
            if (current->ID == value) {
                if (prev == NULL) {
                    // Deleting the first element
                    HeadStudent = current->next;
                } else {
                    prev->next = current->next;
                }
                
                if (current == CurrentStudent) {
                    CurrentStudent = prev;
                }
                
                student *temp = current;
                current = current->next;
                delete temp;
            } else {
                prev = current;
                current = current->next;
            }
        }
    }

    void PrintList() {
        student *temp = HeadStudent->next; // Start from the first actual student
        while (temp != NULL) {
            cout << temp->ID << " ";
            temp = temp->next;
        }
        cout << endl;
    }

    ~StudentList() {
        student *current = HeadStudent;
        while (current != NULL) {
            student *next = current->next;
            delete current;
            current = next;
        }
    }
};

int main() {
    StudentList sl;
    sl.Add_Student(56);
    sl.Add_Student(78);
    sl.Add_Student(12);
    sl.Add_Student(78);
    sl.InsertBeginning(99);
    
    cout << "Original list: ";
    sl.PrintList();
    
    sl.DeleteElement(56);
    sl.PrintList();
      
    return 0;
}