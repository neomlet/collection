import java.util.*;

public class PasswordGenerator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Length (min 4): ");
        int length = Math.max(4, scanner.nextInt());
        
        System.out.print("Use special chars? (y/n): ");
        boolean useSpecial = scanner.next().toLowerCase().equals("y");
        
        String lower = "abcdefghijklmnopqrstuvwxyz";
        String upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        String digits = "0123456789";
        String special = "!@#$%^&*()_+-=";
        
        List<Character> password = new ArrayList<>();
        password.add(lower.charAt((int)(Math.random() * lower.length())));
        password.add(upper.charAt((int)(Math.random() * upper.length())));
        password.add(digits.charAt((int)(Math.random() * digits.length())));
        
        if (useSpecial) {
            password.add(special.charAt((int)(Math.random() * special.length())));
        }
        
        String all = lower + upper + digits + (useSpecial ? special : "");
        while (password.size() < length) {
            password.add(all.charAt((int)(Math.random() * all.length())));
        }
        
        Collections.shuffle(password);
        System.out.println("Password: " + password.stream().collect(StringBuilder::new, StringBuilder::append, StringBuilder::append).toString());
    }
}