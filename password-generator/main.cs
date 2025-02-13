using System;
using System.Linq;
using System.Collections.Generic;

class Program {
    static void Main() {
        Console.Write("Length (min 4): ");
        int length = Math.Max(4, int.Parse(Console.ReadLine()));
        
        Console.Write("Use special chars? (y/n): ");
        bool useSpecial = Console.ReadLine().ToLower() == "y";
        
        var random = new Random();
        var password = new List<char> {
            "abcdefghijklmnopqrstuvwxyz"[random.Next(26)],
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random.Next(26)],
            "0123456789"[random.Next(10)]
        };
        
        if (useSpecial) password.Add("!@#$%^&*()_+-="[random.Next(14)]);
        
        string all = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" 
                    + (useSpecial ? "!@#$%^&*()_+-=" : "");
        
        while (password.Count < length) {
            password.Add(all[random.Next(all.Length)]);
        }
        
        Console.WriteLine("Password: " + new string(password.OrderBy(x => random.Next()).ToArray()));
    }
}