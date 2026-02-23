import requests
from datetime import datetime
from bs4 import BeautifulSoup

# =====================================
# CONFIG — EDIT ONLY IF USERNAMES CHANGE
# =====================================
GITHUB_USERNAME = "phoenix2429"
LEETCODE_USERNAME = "canarycode"
GFG_USERNAME = "loghamitowyq"
BIRTHDATE = datetime(2005, 8, 24)

# =====================================
# AGE CALCULATION
# =====================================
def calculate_age():
    today = datetime.now()
    age = today.year - BIRTHDATE.year - (
        (today.month, today.day) < (BIRTHDATE.month, BIRTHDATE.day)
    )
    return age

# =====================================
# GITHUB DATA
# =====================================
def get_github_stats():
    try:
        user = requests.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}",
            timeout=10,
        ).json()

        return {
            "repos": user.get("public_repos", 0),
            "followers": user.get("followers", 0),
            "following": user.get("following", 0),
        }
    except Exception:
        return {"repos": "N/A", "followers": "N/A", "following": "N/A"}

# =====================================
# LEETCODE DATA
# =====================================
def get_leetcode_stats():
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """

    try:
        response = requests.post(
            "https://leetcode.com/graphql",
            json={"query": query, "variables": {"username": LEETCODE_USERNAME}},
            timeout=15,
        )

        data = response.json()
        submissions = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
        total_solved = sum(item["count"] for item in submissions)
        return total_solved
    except Exception:
        return "N/A"

# =====================================
# GEEKSFORGEEKS DATA (SCRAPING)
# =====================================
def get_gfg_stats():
    try:
        url = f"https://www.geeksforgeeks.org/user/{GFG_USERNAME}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        solved = soup.find("div", class_="score_card_value")
        if not solved:
            solved = soup.find("span", class_="score_card_value")
        if not solved:
            solved = soup.find("div", class_="problemNavbarHead_profile_score")
            
        if solved:
            return solved.text.strip()
        return "N/A"
    except Exception:
        return "N/A"

# =====================================
# README GENERATOR
# =====================================
def generate_readme():
    age = calculate_age()
    gh = get_github_stats()
    lc = get_leetcode_stats()
    gfg = get_gfg_stats()
    last_updated = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    content = f"""<img src="assets/profile.jpg" width="150px" align="left">

# LOGHAMITHRA N

- OS: ......Debian 12, Android, Linux
- Age: ......{age} years
- IDE: ......Visual Studio Code

- Languages.Programming: ......Python, C, Java, Go
- Languages.Web: ......HTML, CSS, JavaScript, React
- Languages.Real: ......English, Kannada, Hindi, Tamil

- Networking: ......TCP/IP, DNS, DHCP, VLAN
- Security: ......TLS, VPN, IPsec
- Tools: ......Git, VS Code, Wireshark

---

Contacts

- Email: ......loghamithra345@gmail.com
- LinkedIn: ......https://linkedin.com/in/loghamithra240825
- GitHub: ......https://github.com/phoenix2429

---

Live Stats

- GitHub Followers: ......{gh['followers']}
- GitHub Following: ......{gh['following']}
- GitHub Public Repos: ......{gh['repos']}
- LeetCode Solves: ......{lc}
- GeeksforGeeks Score: ......{gfg}
- Last Updated: ......{last_updated}

"""
    return content

# =====================================
# MAIN EXECUTION
# =====================================
if __name__ == "__main__":
    content = generate_readme()
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ README generated successfully.")