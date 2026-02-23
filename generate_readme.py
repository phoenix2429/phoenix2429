import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =====================================
# CONFIG
# =====================================
GITHUB_USERNAME = "phoenix2429"
LEETCODE_USERNAME = "canarycode"
BIRTHDATE = datetime(2005, 8, 24)

IMAGE_PATH = "assets/profile.jpg"
OUTPUT_IMAGE = "assets/ascii.png"

ASCII_WIDTH = 80
ASCII_CHARS = "@%#*+=-:. "

# =====================================
# IMAGE → COLORED ASCII PNG
# =====================================
def generate_ascii_image():
    img = Image.open(IMAGE_PATH)
    img = img.resize((ASCII_WIDTH, int(ASCII_WIDTH * img.height / img.width * 0.55)))

    width, height = img.size
    pixels = img.load()

    font_size = 10
    font = ImageFont.load_default()

    output_img = Image.new("RGB", (width * font_size, height * font_size), "black")
    draw = ImageDraw.Draw(output_img)

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            gray = int((r + g + b) / 3)
            char = ASCII_CHARS[gray * len(ASCII_CHARS) // 256]
            draw.text((x * font_size, y * font_size), char, fill=(r, g, b), font=font)

    output_img.save(OUTPUT_IMAGE)

# =====================================
# AGE
# =====================================
def calculate_age():
    today = datetime.now()
    return today.year - BIRTHDATE.year - (
        (today.month, today.day) < (BIRTHDATE.month, BIRTHDATE.day)
    )

# =====================================
# GITHUB
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
        }
    except:
        return {"repos": "N/A", "followers": "N/A"}

# =====================================
# LEETCODE
# =====================================
def get_leetcode_stats():
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        submitStats: submitStatsGlobal {
          acSubmissionNum {
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
        )
        data = response.json()
        return sum(x["count"] for x in data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"])
    except:
        return "N/A"

# =====================================
# README
# =====================================
def generate_readme():
    age = calculate_age()
    gh = get_github_stats()
    lc = get_leetcode_stats()
    last_updated = datetime.now().strftime("%d-%m-%Y")

    return f"""
<table>
<tr>
<td>

<img src="assets/ascii.png" width="320"/>

</td>
<td>

### LOGHAMITHRA N

- Age: {age}
- OS: Debian 12 / Linux
- IDE: VS Code  

---

**GitHub**
- Followers: {gh['followers']}
- Repos: {gh['repos']}

**LeetCode**
- Solved: {lc}

_Last updated: {last_updated}_

</td>
</tr>
</table>
"""

# =====================================
# MAIN
# =====================================
if __name__ == "__main__":
    generate_ascii_image()
    readme = generate_readme()

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ Colored ASCII profile generated.")