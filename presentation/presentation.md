# Presentation: Password Strength Checker

## Slide 1: Title Slide
- **Title:** Password Strength Checker
- **Subtitle:** A privacy-focused password evaluation tool powered by k-Anonymity & security heuristics.
- **Presenter:** Project Maintainer

---

## Slide 2: Problem & Solution
- **Problem:**
  - Users select weak, predictable passwords containing personal information (usernames, birth years).
  - Users frequently reuse passwords that have already been exposed in security breaches.
- **Privacy Challenge:**
  - Conventional online breach checkers require sending passwords to a third-party server, introducing a security risk.
- **Solution:**
  - Hybrid heuristic evaluation (local rules) combined with zero-knowledge breach lookups using HaveIBeenPwned's **k-Anonymity model**.

---

## Slide 3: Evaluation Criteria & Security Architecture
- **Immediate Rejections (Errors):**
  - Password contains the username (case-insensitive).
  - Leaked in > 300 data breaches.
  - Empty input.
- **Interactive Warnings (Requires Explicit Approval `y`):**
  - Leaked in 1–300 breaches.
  - Fewer than 4 numbers & special characters combined (at least 1 special char mandatory).
  - Missing uppercase character.
  - Potential birth year detected (1950–2026).

---

## Slide 4: Privacy via k-Anonymity
- **How k-Anonymity Works:**
  1. Hash the password locally using **SHA-1**.
  2. Send only the **first 5 hex characters** (hash prefix) to `api.pwnedpasswords.com`.
  3. The API returns thousands of hash suffixes sharing that prefix.
  4. Perform local comparison of the remaining **35 characters** (hash suffix) on the client.
- **Result:** Neither HaveIBeenPwned nor any middleman ever receives the full hash or plain text password.

---

## Slide 5: Delivery & Deployment
- **Python CLI Tool (`psc.py`):**
  - Native Python 3 implementation with standard libraries (`hashlib`, `urllib.request`).
- **Web Interface (`index.html`):**
  - Fully responsive, dark-mode client-side application utilizing Web Crypto API (`crypto.subtle`).
- **GitHub Pages Deployment:**
  - Accessible directly at `https://yashthesoni.github.io/psc/`.
