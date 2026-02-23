import requests
from datetime import datetime
from PIL import Image

# =====================================
# CONFIG — EDIT ONLY IF USERNAMES CHANGE
# =====================================
GITHUB_USERNAME = "phoenix2429"
LEETCODE_USERNAME = "canarycode"
BIRTHDATE = datetime(2005, 8, 24)

IMAGE_PATH = "assets/profile.jpg"
ASCII_WIDTH = 70

ASCII_CHARS = "@%#*+=-:. "

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
# IMAGE → ASCII
# =====================================
def image_to_ascii(path, width=70):
    try:
        img = Image.open(path).convert("L")

        # maintain aspect ratio
        aspect_ratio = img.height / img.width
        height = int(width * aspect_ratio * 0.55)

        img = img.resize((width, height))

        pixels = img.getdata()
        chars = "".join(
            ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
            for pixel in pixels
        )

        ascii_image = "\n".join(
            chars[i:i + width] for i in range(0, len(chars), width)
        )

        return ascii_image
    except Exception as e:
        return f"ASCII generation failed: {e}"

# =====================================
# README GENERATOR
# =====================================
def generate_readme():
    age = calculate_age()
    gh = get_github_stats()
    lc = get_leetcode_stats()
    ascii_art = image_to_ascii(IMAGE_PATH, ASCII_WIDTH)
    last_updated = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    content = f"""# LOGHAMITHRA N

<pre>
{ascii_art}
</pre>

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

## Contacts

- Email: ......loghamithra345@gmail.com
- LinkedIn: ......https://linkedin.com/in/loghamithra240825
- GitHub: ......https://github.com/{GITHUB_USERNAME}

---

## Live Stats

- GitHub Followers: ......{gh['followers']}
- GitHub Following: ......{gh['following']}
- GitHub Public Repos: ......{gh['repos']}
- LeetCode Solves: ......{lc}
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
    print("✅ README generated with ASCII art.")