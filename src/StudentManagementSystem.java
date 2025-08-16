import java.util.*;

public class StudentManagementSystem {
    public static void main(String[] args) {
        List<Student> students = new ArrayList<>();

        Student student1 = new Student(1630, "Rihan", "EEE");
        Student student2 = new Student(1654, "Akhar", "CSE");
        Student student3 = new Student(1693, "Rifat", "ME");
        Student student4 = new Student(1612, "Irfan", "CE");
        Student student5 = new Student(1607, "Pranto", "SWE");

        students.add(student1);
        students.add(student2);
        students.add(student3);
        students.add(student4);
        students.add(student5);

        System.out.println("All Students:");
        for (Student student : students) {
            System.out.println(student);
        }

        Student newStudent = new Student(1613, "Asim", "CSE");
        students.add(2,newStudent);
        System.out.println("\nAfter adding a new student at index 2:");
        for (Student student : students) {
            System.out.println(student);
        }

        students.remove(1);
        System.out.println("\nAfter removing the student at index 1:");
        for (Student student : students) {
            System.out.println(student);
        }

        students.remove(student4);
        System.out.println("\nAfter removing student4 by object:");
        for (Student student : students) {
            System.out.println(student);
        }

        Set<Student> courseEnrollment= new HashSet<>();
        courseEnrollment.add(student1);
        courseEnrollment.add(student3);
        courseEnrollment.add(student5);

        System.out.println("\nCourse Enrollment:");
        for (Student student : courseEnrollment) {
            System.out.println(student);
        }

        System.out.println("\nAdding a student to the course enrollment set again:");
        boolean wasAdded = courseEnrollment.add(student1);
        System.out.println("Was he added?" + wasAdded);

        System.out.println("Checking if a student is enrolled in the course:");
        boolean isEnrolled = courseEnrollment.contains(student2);
        System.out.println("Is student2 enrolled? " + isEnrolled);

        Map<Integer, Student> studentMap = new HashMap<>();
        for (Student student : students) {
            studentMap.put(student.getStudentId(), student);
        }
        for (Map.Entry<Integer, Student> entry : studentMap.entrySet()) {
            System.out.println("ID: " + entry.getKey() + ":- " + entry.getValue());

        }
        System.out.println("Quickly retrieving a student by ID:");
        int searchId = 1630;
        Student foundStudent = studentMap.get(searchId);
        if (foundStudent != null) {
            System.out.println("Found Student: " + foundStudent);
        } else {
            System.out.println("No student found with ID: " + searchId);

        }
        searchId = 1654;
        foundStudent = studentMap.get(searchId);
        if (foundStudent != null) {
            System.out.println("Found Student: "+ searchId + foundStudent);
        }
        else {
            System.out.println("No student found with ID: " + searchId);
        }


    }
}
