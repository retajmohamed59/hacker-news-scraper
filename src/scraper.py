import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# -----------------------------
# Step 1: Request the page
# -----------------------------
url = "https://news.ycombinator.com/"
response = requests.get(url)
response.raise_for_status()  # ensures request worked

# -----------------------------
# Step 2: Parse HTML
# -----------------------------
soup = BeautifulSoup(response.text, "html.parser")

posts = soup.select(".athing")
subtexts = soup.select(".subtext")

data = []

# -----------------------------
# Step 3: Extract Top 20 posts
# -----------------------------
for post, sub in list(zip(posts, subtexts))[:20]:
    # title & link
    title_tag = post.select_one(".titleline a")
    title = title_tag.text.strip()
    link = title_tag["href"]

    # score
    score_tag = sub.select_one(".score")
    if score_tag:
        score = int(score_tag.text.replace(" points", "").replace(" point", ""))
    else:
        score = 0

    # comments
    comments_tag = sub.select("a")[-1].text
    if "comment" in comments_tag:
        comments = comments_tag.split()[0]
        comments = 0 if comments == "discuss" else int(comments)
    else:
        comments = 0

    # time
    time_tag = sub.select_one(".age")
    time_posted = time_tag.text if time_tag else "N/A"

    data.append({
        "title": title,
        "link": link,
        "score": score,
        "comments": comments,
        "time_posted": time_posted
    })

# -----------------------------
# Step 4: Create DataFrame
# -----------------------------
df = pd.DataFrame(data)

# -----------------------------
# Step 5: Ensure data folder exists
# -----------------------------
os.makedirs("data", exist_ok=True)

# -----------------------------
# Step 6: Save CSV
# -----------------------------
output_path = "data/hacker_news_posts.csv"
df.to_csv(output_path, index=False)

print("✅ Top 20 posts scraped and saved successfully!")