import Foundation

func generatePassword() -> String {
    print("Length (min 4): ", terminator: "")
    let length = max(Int(readLine()!) ?? 0, 4)
    
    print("Use special chars? (y/n): ", terminator: "")
    let useSpecial = readLine()!.lowercased() == "y"
    
    let lower = "abcdefghijklmnopqrstuvwxyz"
    let upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    let digits = "0123456789"
    let special = "!@#$%^&*()_+-="
    
    var password: [Character] = [
        lower.randomElement()!,
        upper.randomElement()!,
        digits.randomElement()!
    ]
    
    if useSpecial {
        password.append(special.randomElement()!)
    }
    
    let all = lower + upper + digits + (useSpecial ? special : "")
    while password.count < length {
        password.append(all.randomElement()!)
    }
    
    return String(password.shuffled())
}

print("Password: \(generatePassword())")