import os

# יצירת תמונות SVG דמה לכל המילים במשחק (מורחב ל-48 מילים)
images_dir = "static/images"
os.makedirs(images_dir, exist_ok=True)

# רשימת כל התמונות הנדרשות עם אמוג'י מתאים (מורחב)
images_data = {
    # חיות (12 מילים)
    "dog": "🐕",
    "cat": "🐱", 
    "bird": "🐦",
    "fish": "🐟",
    "cow": "🐄",
    "horse": "🐎",
    "mouse": "🐭",
    "lion": "🦁",
    "elephant": "🐘",
    "monkey": "🐵",
    "bear": "🐻",
    "wolf": "🐺",
    
    # צבעים (12 מילים)
    "red": "🔴",
    "blue": "🔵", 
    "yellow": "🟡",
    "green": "🟢",
    "purple": "🟣",
    "orange": "🟠",
    "pink": "🩷",
    "black": "⚫",
    "white": "⚪",
    "brown": "🟤",
    "gray": "🔘",
    "gold": "🟡",
    
    # אוכל (12 מילים)
    "apple": "🍎",
    "banana": "🍌",
    "bread": "🍞", 
    "water": "💧",
    "milk": "🥛",
    "cake": "🎂",
    "pizza": "🍕",
    "ice_cream": "🍦",
    "egg": "🥚",
    "cheese": "🧀",
    "fish_food": "🐟",
    "meat": "🥩",
    
    # משפחה (12 מילים)
    "father": "👨",
    "mother": "👩",
    "brother": "👦",
    "sister": "👧",
    "grandfather": "👴",
    "grandmother": "👵",
    "cousin": "👪",
    "baby": "👶",
    "uncle": "👨‍🦳",
    "aunt": "👩‍🦳", 
    "son": "👦",
    "daughter": "👧",
    
    # פעלים (12 מילים)
    "go": "🚶‍♂️",
    "come": "🏃‍♂️",
    "eat": "🍽️",
    "drink": "🥤",
    "sleep": "😴",
    "run": "🏃‍♂️",
    "play": "🎮",
    "read": "📖",
    "write": "✍️",
    "see": "👁️",
    "hear": "👂",
    "speak": "🗣️"
}

# פונקציה ליצירת SVG עם אמוג'י ורקע צבעוני (משופרת)
def create_svg_image(name, emoji):
    # צבעי רקע שונים לכל קטגוריה - משופרים
    colors = {
        # חיות - גוונים חמים וטבעיים
        'dog': '#D2691E', 'cat': '#FF69B4', 'bird': '#87CEEB', 'fish': '#00CED1',
        'cow': '#000000', 'horse': '#8B4513', 'mouse': '#808080', 'lion': '#DAA520',
        'elephant': '#696969', 'monkey': '#CD853F', 'bear': '#8B4513', 'wolf': '#708090',
        
        # צבעים - צבעים אמיתיים
        'red': '#FF0000', 'blue': '#0000FF', 'yellow': '#FFFF00', 'green': '#008000',
        'purple': '#800080', 'orange': '#FFA500', 'pink': '#FFC0CB', 'black': '#000000',
        'white': '#FFFFFF', 'brown': '#8B4513', 'gray': '#808080', 'gold': '#FFD700',
        
        # אוכל - צבעי אוכל אמיתיים
        'apple': '#FF0000', 'banana': '#FFFF00', 'bread': '#DEB887', 'water': '#87CEEB',
        'milk': '#FFFFFF', 'cake': '#FFB6C1', 'pizza': '#FF6347', 'ice_cream': '#FFF8DC',
        'egg': '#FFFACD', 'cheese': '#FFD700', 'fish_food': '#20B2AA', 'meat': '#8B0000',
        
        # משפחה - צבעים מגדריים וגיליים
        'father': '#4169E1', 'mother': '#FF69B4', 'brother': '#32CD32', 'sister': '#FF1493',
        'grandfather': '#708090', 'grandmother': '#DDA0DD', 'cousin': '#FFA500', 'baby': '#FFB6C1',
        'uncle': '#2E8B57', 'aunt': '#DC143C', 'son': '#00CED1', 'daughter': '#DA70D6',
        
        # פעלים - גוונים אנרגטיים ודינמיים
        'go': '#228B22', 'come': '#FF4500', 'eat': '#DC143C', 'drink': '#1E90FF',
        'sleep': '#9370DB', 'run': '#FF6347', 'play': '#32CD32', 'read': '#4682B4',
        'write': '#B8860B', 'see': '#FF1493', 'hear': '#20B2AA', 'speak': '#FF8C00'
    }
    
    bg_color = colors.get(name, '#f7fafc')
    
    # SVG משופר עם עיצוב יפה יותר
    svg_content = f'''<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{bg_color}AA;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="#00000030"/>
    </filter>
  </defs>
  <rect width="200" height="200" fill="url(#bg_{name})" stroke="#444444" stroke-width="3" rx="20"/>
  <circle cx="100" cy="100" r="60" fill="rgba(255,255,255,0.2)" filter="url(#shadow)"/>
  <text x="100" y="100" font-family="Arial, sans-serif" font-size="60" text-anchor="middle" dy="0.3em" filter="url(#shadow)">{emoji}</text>
  <rect x="10" y="170" width="180" height="25" fill="rgba(255,255,255,0.9)" stroke="#333" stroke-width="1" rx="12"/>
  <text x="100" y="184" font-family="Arial, sans-serif" font-size="12" fill="#2d3748" text-anchor="middle" font-weight="bold">{name.replace('_', ' ').replace('food', '').strip().title()}</text>
</svg>'''
    
    return svg_content

# יצירת כל התמונות
print("🎨 יוצר תמונות חדשות למשחק (48 תמונות)...")
created_count = 0

for name, emoji in images_data.items():
    file_path = os.path.join(images_dir, f"{name}.jpg")
    svg_content = create_svg_image(name, emoji)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    created_count += 1
    print(f"✅ {created_count}/48: {file_path}")

print(f"\n🎉 נוצרו {len(images_data)} תמונות בהצלחה!")
print("📊 פילוח תמונות:")
print("   🐾 חיות: 12 תמונות")
print("   🎨 צבעים: 12 תמונות") 
print("   🍕 אוכל: 12 תמונות")
print("   👨‍👩‍👧‍👦 משפחה: 12 תמונות")
print("המשחק עם 10 רמות לכל קטגוריה מוכן לפעולה! 🎮")