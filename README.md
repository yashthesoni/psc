### Project Title
**Python Password Strength Checker**

A password is **immediately rejected** if it fails any of the following checks:

| # | Error Condition | Rationale / Cybersecurity Threat | Action |
|---|---|---|---|
| 1 | **Username Inside Password** | Passwords containing the username (case-insensitive) are susceptible to simple dictionary & credential stuffing attacks. | Rebuilt |
| 2 | **Leaked in > 300 Data Breaches** | High breach counts indicate the password is in publicly available hacker wordlists (e.g. RockYou). | Rebuilt |
| 3 | **Empty Password Input** | Blank strings provide zero protection. | Rebuilt |

---

If a password triggers any warning, it is **rejected unless the user explicitly inputs `y`**:

| # | Warning Condition | Rationale / Cybersecurity Threat |
|---|---|---|
| 1 | **Leaked in 1 to 300 Breaches** | Password has appeared in real-world leaks, but at lower frequency. |
| 2 | **Fewer than 4 Numbers & Special Characters** | Fewer than 4 numbers and special characters combined lowers entropy against dictionary and brute-force attacks. |
| 3 | **No Uppercase Letter** | Reduces overall character search space (pool size). |
| 4 | **No Special Character** | At least one non-alphanumeric character (`@`, `#`, `$`, etc.) is mandatory. |
| 5 | **Potential Birth Year (1950–2026)** | Detects 4-digit blocks containing years between 1950 and 2026. Prevents predictable personal dates. |

---

### HaveIBeenPwned API via k-Anonymity

To check breaches without compromising user privacy:
1. The password is hashed using **SHA-1**.
2. Only the **first 5 characters (prefix)** of the hash are sent to `api.pwnedpasswords.com`.
3. The API returns candidate hashes.
4. Python locally matches the remaining **35 characters (suffix)** to determine the exact leak count.