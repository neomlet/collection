package main

import (
    "fmt"
    "math/rand"
    "time"
    "strings"
)

func main() {
    rand.Seed(time.Now().UnixNano())
    
    var length int
    fmt.Print("Length (min 4): ")
    fmt.Scan(&length)
    if length < 4 { length = 4 }
    
    var useSpecial string
    fmt.Print("Use special chars? (y/n): ")
    fmt.Scan(&useSpecial)
    
    lower := "abcdefghijklmnopqrstuvwxyz"
    upper := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits := "0123456789"
    special := "!@#$%^&*()_+-="
    
    password := []byte{
        lower[rand.Intn(len(lower))],
        upper[rand.Intn(len(upper))],
        digits[rand.Intn(len(digits))],
    }
    
    if strings.ToLower(useSpecial) == "y" {
        password = append(password, special[rand.Intn(len(special))])
    }
    
    all := lower + upper + digits
    if useSpecial == "y" { all += special }
    
    for len(password) < length {
        password = append(password, all[rand.Intn(len(all))])
    }
    
    rand.Shuffle(len(password), func(i, j int) {
        password[i], password[j] = password[j], password[i]
    })
    
    fmt.Println("Password:", string(password))
}