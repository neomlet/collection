import kotlin.random.Random

fun main() {
    print("Length (min 4): ")
    val length = maxOf(readLine()!!.toIntOrNull() ?: 0, 4)
    
    print("Use special chars? (y/n): ")
    val useSpecial = readLine()!!.trim().equals("y", ignoreCase = true)
    
    val lower = "abcdefghijklmnopqrstuvwxyz"
    val upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    val digits = "0123456789"
    val special = "!@#$%^&*()_+-="
    
    val password = mutableListOf(
        lower[Random.nextInt(lower.length)],
        upper[Random.nextInt(upper.length)],
        digits[Random.nextInt(digits.length)]
    )
    
    if (useSpecial) password.add(special[Random.nextInt(special.length)])
    
    val all = lower + upper + digits + if (useSpecial) special else ""
    while (password.size < length) {
        password.add(all[Random.nextInt(all.length)])
    }
    
    println("Password: ${password.shuffled().joinToString("")}")
}