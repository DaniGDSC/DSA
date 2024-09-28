#include <iostream>
using namespace std;

class student {
public: 
    int ID; // Member variable to store the student ID
    student *next; // Pointer to the next student in the list
    student() {
        ID = 0; // Initialize the ID to 0 and set next pointer to NULL
        next = NULL;
    }

    void setstudent(int id) {
        this->ID = id; // Set the student ID
        this->next = NULL; // Set the next pointer to NULL
    }

    int getstudent() {
        return this->ID; // Return the student ID
    }

    void nextelement(student *ns) {
        this->next = ns; // Set the next pointer to the given student pointer
    }

    student* getnextstudent() {
        return next; // Return the next student pointer
    }
};

class StudentList {
private: 
    student *HeadStudent, *CurrentStudent;
public:
    StudentList() : HeadStudent(NULL), CurrentStudent(NULL) {} // Initialize head and current pointers to NULL

    void Add_Student(int studentid) {
        student *NewStudent = new student(); // Create a new student node
        NewStudent->setstudent(studentid); // Set the new student ID
        if (HeadStudent == NULL) { // If the list is empty, set the head to the new student
            HeadStudent = NewStudent;
            CurrentStudent = NewStudent;
        } else { // Otherwise, add the new student after the current student
            CurrentStudent->nextelement(NewStudent);
            CurrentStudent = NewStudent; // Update the current student pointer to the new student
        }
        cout << "Student ID: " << CurrentStudent->getstudent() << endl;
    }
};

int main() {
    StudentList sl;
    sl.Add_Student(56);
    sl.Add_Student(78);
    sl.Add_Student(12);
    return 0;
}
