import json

with open("youtube_cookies.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("cookies.txt", "w", encoding="utf-8") as f:
    f.write("# Netscape HTTP Cookie File\n\n")
    for cookie in data:
        domain = cookie.get("domain", ".youtube.com")
        flag = "TRUE" if not cookie.get("hostOnly", False) else "FALSE"
        path = cookie.get("path", "/")
        secure = "TRUE" if cookie.get("secure", False) else "FALSE"
        expiration = int(cookie.get("expirationDate", 0))
        name = cookie["name"]
        value = cookie["value"]

        line = f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n"
        f.write(line)

print("✅ 已成功轉換成 cookies.txt，交給 yt-dlp 使用。")
