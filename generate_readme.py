# generate_readme.py

import requests
from datetime import datetime, timezone, timedelta
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

ASCII_CHARS = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|)(1}{][?-_+~><i!lI;:,",^`'. """

# =====================================
# IMAGE → COLORED ASCII PNG
# =====================================
def generate_ascii_image():
    try:
        img = Image.open(IMAGE_PATH).convert("RGB")
    except Exception as e:
        print(f"❌ Failed to open image: {e}")
        return

    # maintain aspect ratio (terminal correction)
    new_height = int(ASCII_WIDTH * img.height / img.width * 0.55)
    img = img.resize((ASCII_WIDTH, new_height))

    width, height = img.size

    font_size = 10
    font = ImageFont.load_default()

    output_img = Image.new(
        "RGB",
        (width * font_size, height * font_size),
        "black",
    )
    draw = ImageDraw.Draw(output_img)

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            char = ASCII_CHARS[gray * (len(ASCII_CHARS) - 1) // 255]

            draw.text(
                (x * font_size, y * font_size),
                char,
                fill=(r, g, b),
                font=font,
            )

    output_img.save(OUTPUT_IMAGE)
    print("✅ ASCII image generated.")


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
            "following": user.get("following", 0),
        }
    except Exception:
        return {"repos": "N/A", "followers": "N/A", "following": "N/A"}


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
            timeout=15,
        )

        data = response.json()
        return sum(
            x["count"]
            for x in data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
        )
    except Exception:
        return "N/A"


# =====================================
# README GENERATOR (COMPACT STYLE)
# =====================================
def generate_readme():
    age = calculate_age()
    gh = get_github_stats()
    lc = get_leetcode_stats()

    ist = timezone(timedelta(hours=5, minutes=30))
    last_updated = datetime.now(ist).strftime("%d-%m-%Y %I:%M:%S %p")

    return f"""
<table>
<tr>
<td width="340">

<img src="assets/ascii.png" width="320"/>

</td>
<td>

### LOGHAMITHRA N

```bash
OS: Linux
Age: {age}
IDE: Visual Studio Code

GitHub Followers: {gh['followers']}
GitHub Repos: {gh['repos']}
LeetCode Solved: {lc}

Last Updated: {last_updated}

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