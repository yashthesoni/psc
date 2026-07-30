import hashlib
import urllib.request
import urllib.error

def check_pwned_api(password: str) -> int:
    try:
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Python-Password-Checker'})
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            for line in content.splitlines():
                h, count = line.split(':')
                if h == suffix:
                    return int(count)
    except Exception:
        pass
    return 0

def check_errors(username: str, password: str, pwned_count: int) -> list:
    errors = []

    # Username check
    if username.strip() and username.lower() in password.lower():
        errors.append("Password contains username")

    # Breach check (> 300)
    if pwned_count > 300:
        errors.append(f"Password leaked in {pwned_count} data breaches")

    return errors

def check_warnings(password: str, pwned_count: int) -> list:
    warnings = []

    # Breach warning (1 to 300)
    if 1 <= pwned_count <= 300:
        warnings.append(f"Password leaked in {pwned_count} data breaches")

    # Digits count (< 4)
    digit_count = sum(1 for c in password if c.isdigit())
    if digit_count < 4:
        warnings.append(f"Fewer than 4 digits ({digit_count} found)")

    # Uppercase check
    if not any(c.isupper() for c in password):
        warnings.append("No uppercase letter")

    # Special character check
    if not any(not c.isalnum() for c in password):
        warnings.append("No special character")

    # Birth year check (1970 - 2015)
    n = len(password)
    i = 0
    has_birthyear = False

    while i < n:
        if password[i].isdigit():
            start = i
            while i < n and password[i].isdigit():
                i += 1
            end = i
            
            digit_block = password[start:end]
            
            if len(digit_block) >= 4:
                char_before_is_letter = (start > 0) and password[start - 1].isalpha()
                char_after_is_letter = (end < n) and password[end].isalpha()
                
                if not char_before_is_letter and not char_after_is_letter:
                    for j in range(len(digit_block) - 3):
                        sub_year = int(digit_block[j:j+4])
                        if 1970 <= sub_year <= 2015:
                            has_birthyear = True
                            break
        else:
            i += 1

    if has_birthyear:
        warnings.append("Potential birth year detected (1970-2015)")

    return warnings

def indent_block(text: str, indent: str = "    ") -> str:
    """Indents every line of a multi-line string block."""
    return "\n".join(indent + line if line.strip() else line for line in text.splitlines())

def main():
    username = input("Username: ").strip()

    while True:
        password = input("Password: ")

        if not password:
            print("\n    Password cannot be empty.\n")
            continue

        pwned_count = check_pwned_api(password)

        errors = check_errors(username, password, pwned_count)
        warnings = check_warnings(password, pwned_count)

        output_blocks = []

        if errors:
            err_lines = ["Errors:"] + [f"- {err}" for err in errors]
            output_blocks.append("\n".join(err_lines))

        if warnings:
            warn_lines = ["Warnings:"] + [f"- {w}" for w in warnings]
            output_blocks.append("\n".join(warn_lines))

        if errors:
            output_blocks.append("Password rejected.")
            message_text = "\n\n".join(output_blocks)
            print("\n" + indent_block(message_text) + "\n")
            continue

        if warnings:
            message_text = "\n\n".join(output_blocks)
            print("\n" + indent_block(message_text) + "\n")
            choice = input("    Ignore warnings? (y/n): ").strip().lower()
            if choice != 'y':
                print("\n    Password rejected.\n")
                continue

        print("\n    Password accepted.\n")
        break

if __name__ == "__main__":
    main()
