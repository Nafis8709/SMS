import java.util.Objects;
public class Student {
    private int studentId;
    private String name;
    private String major;

    public Student(int studentId, String name, String major) {
        this.studentId = studentId;
        this.name = name;
        this.major = major;
    }
    public int getStudentId() {
        return studentId;
    }
    public String getName() {
        return name;
    }
    public String getMajor() {
        return major;
    }
    @Override
    public String toString() {
        return "Student{" +
                "studentId=" + studentId +
                ", name='" + name + '\'' +
                ", major='" + major + '\'' +
                '}';
    }
    @Override
    public boolean equals(Object o) {
        if(this == o) return true;
        if(o == null || getClass() != o.getClass()) return false;
        Student student = (Student) o;
        return studentId == student.studentId;

    }

    @Override
    public int hashCode() {
        return Objects.hash(studentId);
    }
}
