import json
from datetime import datetime

# 這裡示範「每天從預設題庫中挑選」或「串接 AI 生成」的邏輯
# 若要完全自動，強烈建議在這裡使用 OpenAI API (ChatGPT) 來生成學測級別的文章

def generate_daily_article():
    # 模擬今天產生的文章資料
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    new_article = {
        "date": today_str,
        "title": "New Discoveries in Space Exploration",
        "content": "Space exploration has always fascinated humanity. Recently, astronomers discovered a new exoplanet that closely resembles Earth. This discovery has sparked debates about the possibility of extraterrestrial life.\n\nScientists plan to send probes to gather more data in the coming decades.",
        "vocabulary": [
            {"word": "fascinate", "part_of_speech": "v.", "meaning": "使著迷"},
            {"word": "exoplanet", "part_of_speech": "n.", "meaning": "系外行星"},
            {"word": "extraterrestrial", "part_of_speech": "adj.", "meaning": "地球外的；外星的"}
        ]
    }
    return new_article

def main():
    article_data = generate_daily_article()
    
    # 覆寫原本的 article.json
    with open('article.json', 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)
    print(f"[{article_data['date']}] 文章已成功更新！")

if __name__ == "__main__":
    main()