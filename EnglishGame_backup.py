from flask import Flask, render_template, request, jsonify, session
import random
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'english_game_secret_key_2025'

# קובץ שמירת נתוני השחקנים
PLAYERS_DATA_FILE = 'players_data.json'

# מאגר מילים עברית-אנגלית עם תמונות
WORDS_DATABASE = {
    'animals': {
        'name': 'חיות',
        'words': [
            {'hebrew': 'כלב', 'english': 'dog', 'image': 'dog.jpg'},
            {'hebrew': 'חתול', 'english': 'cat', 'image': 'cat.jpg'},
            {'hebrew': 'ציפור', 'english': 'bird', 'image': 'bird.jpg'},
            {'hebrew': 'דג', 'english': 'fish', 'image': 'fish.jpg'},
            {'hebrew': 'פרה', 'english': 'cow', 'image': 'cow.jpg'},
            {'hebrew': 'סוס', 'english': 'horse', 'image': 'horse.jpg'},
            {'hebrew': 'עכבר', 'english': 'mouse', 'image': 'mouse.jpg'},
            {'hebrew': 'אריה', 'english': 'lion', 'image': 'lion.jpg'},
            {'hebrew': 'פיל', 'english': 'elephant', 'image': 'elephant.jpg'},
            {'hebrew': 'קוף', 'english': 'monkey', 'image': 'monkey.jpg'},
            {'hebrew': 'דוב', 'english': 'bear', 'image': 'bear.jpg'},
            {'hebrew': 'זאב', 'english': 'wolf', 'image': 'wolf.jpg'},
        ]
    },
    'colors': {
        'name': 'צבעים',
        'words': [
            {'hebrew': 'אדום', 'english': 'red', 'image': 'red.jpg'},
            {'hebrew': 'כחול', 'english': 'blue', 'image': 'blue.jpg'},
            {'hebrew': 'צהוב', 'english': 'yellow', 'image': 'yellow.jpg'},
            {'hebrew': 'ירוק', 'english': 'green', 'image': 'green.jpg'},
            {'hebrew': 'סגול', 'english': 'purple', 'image': 'purple.jpg'},
            {'hebrew': 'כתום', 'english': 'orange', 'image': 'orange.jpg'},
            {'hebrew': 'ורוד', 'english': 'pink', 'image': 'pink.jpg'},
            {'hebrew': 'שחור', 'english': 'black', 'image': 'black.jpg'},
            {'hebrew': 'לבן', 'english': 'white', 'image': 'white.jpg'},
            {'hebrew': 'חום', 'english': 'brown', 'image': 'brown.jpg'},
            {'hebrew': 'אפור', 'english': 'gray', 'image': 'gray.jpg'},
            {'hebrew': 'זהב', 'english': 'gold', 'image': 'gold.jpg'},
        ]
    },
    'food': {
        'name': 'אוכל',
        'words': [
            {'hebrew': 'תפוח', 'english': 'apple', 'image': 'apple.jpg'},
            {'hebrew': 'בננה', 'english': 'banana', 'image': 'banana.jpg'},
            {'hebrew': 'לחם', 'english': 'bread', 'image': 'bread.jpg'},
            {'hebrew': 'מים', 'english': 'water', 'image': 'water.jpg'},
            {'hebrew': 'חלב', 'english': 'milk', 'image': 'milk.jpg'},
            {'hebrew': 'עוגה', 'english': 'cake', 'image': 'cake.jpg'},
            {'hebrew': 'פיצה', 'english': 'pizza', 'image': 'pizza.jpg'},
            {'hebrew': 'גלידה', 'english': 'ice cream', 'image': 'ice_cream.jpg'},
            {'hebrew': 'ביצה', 'english': 'egg', 'image': 'egg.jpg'},
            {'hebrew': 'גבינה', 'english': 'cheese', 'image': 'cheese.jpg'},
            {'hebrew': 'דג', 'english': 'fish', 'image': 'fish_food.jpg'},
            {'hebrew': 'בשר', 'english': 'meat', 'image': 'meat.jpg'},
        ]
    },
    'family': {
        'name': 'משפחה',
        'words': [
            {'hebrew': 'אבא', 'english': 'father', 'image': 'father.jpg'},
            {'hebrew': 'אמא', 'english': 'mother', 'image': 'mother.jpg'},
            {'hebrew': 'אח', 'english': 'brother', 'image': 'brother.jpg'},
            {'hebrew': 'אחות', 'english': 'sister', 'image': 'sister.jpg'},
            {'hebrew': 'סבא', 'english': 'grandfather', 'image': 'grandfather.jpg'},
            {'hebrew': 'סבתא', 'english': 'grandmother', 'image': 'grandmother.jpg'},
            {'hebrew': 'בן דוד', 'english': 'cousin', 'image': 'cousin.jpg'},
            {'hebrew': 'תינוק', 'english': 'baby', 'image': 'baby.jpg'},
            {'hebrew': 'דוד', 'english': 'uncle', 'image': 'uncle.jpg'},
            {'hebrew': 'דודה', 'english': 'aunt', 'image': 'aunt.jpg'},
            {'hebrew': 'בן', 'english': 'son', 'image': 'son.jpg'},
            {'hebrew': 'בת', 'english': 'daughter', 'image': 'daughter.jpg'},
        ]
    }
}

# מערכת רמות - 10 רמות לכל נושא
LEVELS_SYSTEM = {
    'animals': [
        {'level': 1, 'name': 'גורי חיות', 'words': ['dog', 'cat', 'bird', 'fish', 'cow'], 'unlock_score': 0},
        {'level': 2, 'name': 'חיות הבית', 'words': ['horse', 'mouse', 'dog', 'cat', 'bird'], 'unlock_score': 25},
        {'level': 3, 'name': 'חיות הבר', 'words': ['lion', 'elephant', 'monkey', 'bear', 'wolf'], 'unlock_score': 50},
        {'level': 4, 'name': 'ספארי 1', 'words': ['elephant', 'lion', 'monkey', 'horse', 'cow'], 'unlock_score': 75},
        {'level': 5, 'name': 'ספארי 2', 'words': ['bear', 'wolf', 'lion', 'elephant', 'monkey'], 'unlock_score': 100},
        {'level': 6, 'name': 'חיות מעורב 1', 'words': ['dog', 'lion', 'fish', 'elephant', 'bird'], 'unlock_score': 125},
        {'level': 7, 'name': 'חיות מעורב 2', 'words': ['cat', 'bear', 'horse', 'wolf', 'mouse'], 'unlock_score': 150},
        {'level': 8, 'name': 'מומחה חיות 1', 'words': ['monkey', 'cow', 'lion', 'dog', 'elephant'], 'unlock_score': 175},
        {'level': 9, 'name': 'מומחה חיות 2', 'words': ['wolf', 'bear', 'cat', 'horse', 'bird'], 'unlock_score': 200},
        {'level': 10, 'name': 'מלך החיות', 'words': ['elephant', 'lion', 'wolf', 'bear', 'monkey'], 'unlock_score': 225},
    ],
    'colors': [
        {'level': 1, 'name': 'צבעים בסיסיים', 'words': ['red', 'blue', 'yellow', 'green', 'black'], 'unlock_score': 0},
        {'level': 2, 'name': 'עוד צבעים', 'words': ['purple', 'orange', 'pink', 'white', 'brown'], 'unlock_score': 25},
        {'level': 3, 'name': 'צבעי רקב', 'words': ['gray', 'gold', 'red', 'blue', 'yellow'], 'unlock_score': 50},
        {'level': 4, 'name': 'מיקס צבעים 1', 'words': ['green', 'purple', 'orange', 'pink', 'black'], 'unlock_score': 75},
        {'level': 5, 'name': 'מיקס צבעים 2', 'words': ['white', 'brown', 'gray', 'gold', 'red'], 'unlock_score': 100},
        {'level': 6, 'name': 'צבעים חמים', 'words': ['red', 'orange', 'yellow', 'pink', 'gold'], 'unlock_score': 125},
        {'level': 7, 'name': 'צבעים קרים', 'words': ['blue', 'green', 'purple', 'gray', 'black'], 'unlock_score': 150},
        {'level': 8, 'name': 'מומחה צבעים 1', 'words': ['gold', 'brown', 'white', 'purple', 'orange'], 'unlock_score': 175},
        {'level': 9, 'name': 'מומחה צבעים 2', 'words': ['pink', 'gray', 'yellow', 'green', 'blue'], 'unlock_score': 200},
        {'level': 10, 'name': 'מלך הצבעים', 'words': ['gold', 'purple', 'orange', 'green', 'red'], 'unlock_score': 225},
    ],
    'food': [
        {'level': 1, 'name': 'אוכל בסיסי', 'words': ['apple', 'banana', 'bread', 'water', 'milk'], 'unlock_score': 0},
        {'level': 2, 'name': 'מתוקים', 'words': ['cake', 'ice cream', 'apple', 'banana', 'bread'], 'unlock_score': 25},
        {'level': 3, 'name': 'חלבונים', 'words': ['egg', 'cheese', 'fish', 'meat', 'milk'], 'unlock_score': 50},
        {'level': 4, 'name': 'ארוחת בוקר', 'words': ['egg', 'bread', 'milk', 'cheese', 'apple'], 'unlock_score': 75},
        {'level': 5, 'name': 'ארוחת ערב', 'words': ['pizza', 'fish', 'meat', 'bread', 'water'], 'unlock_score': 100},
        {'level': 6, 'name': 'מזון מעורב 1', 'words': ['cake', 'pizza', 'apple', 'egg', 'cheese'], 'unlock_score': 125},
        {'level': 7, 'name': 'מזון מעורב 2', 'words': ['ice cream', 'fish', 'banana', 'meat', 'milk'], 'unlock_score': 150},
        {'level': 8, 'name': 'מומחה אוכל 1', 'words': ['pizza', 'cake', 'fish', 'egg', 'apple'], 'unlock_score': 175},
        {'level': 9, 'name': 'מומחה אוכל 2', 'words': ['meat', 'cheese', 'ice cream', 'banana', 'bread'], 'unlock_score': 200},
        {'level': 10, 'name': 'שף מומחה', 'words': ['pizza', 'cake', 'ice cream', 'fish', 'meat'], 'unlock_score': 225},
    ],
    'family': [
        {'level': 1, 'name': 'המשפחה הקרובה', 'words': ['father', 'mother', 'brother', 'sister', 'baby'], 'unlock_score': 0},
        {'level': 2, 'name': 'סבא וסבתא', 'words': ['grandfather', 'grandmother', 'father', 'mother', 'cousin'], 'unlock_score': 25},
        {'level': 3, 'name': 'משפחה מורחבת', 'words': ['uncle', 'aunt', 'cousin', 'son', 'daughter'], 'unlock_score': 50},
        {'level': 4, 'name': 'הדור הצעיר', 'words': ['son', 'daughter', 'baby', 'cousin', 'brother'], 'unlock_score': 75},
        {'level': 5, 'name': 'הדור הבוגר', 'words': ['father', 'mother', 'uncle', 'aunt', 'grandfather'], 'unlock_score': 100},
        {'level': 6, 'name': 'כל המשפחה 1', 'words': ['grandmother', 'sister', 'cousin', 'son', 'father'], 'unlock_score': 125},
        {'level': 7, 'name': 'כל המשפחה 2', 'words': ['mother', 'uncle', 'daughter', 'baby', 'brother'], 'unlock_score': 150},
        {'level': 8, 'name': 'מומחה משפחה 1', 'words': ['aunt', 'grandfather', 'sister', 'cousin', 'son'], 'unlock_score': 175},
        {'level': 9, 'name': 'מומחה משפחה 2', 'words': ['grandmother', 'uncle', 'daughter', 'father', 'mother'], 'unlock_score': 200},
        {'level': 10, 'name': 'מומחה משפחה', 'words': ['grandfather', 'grandmother', 'uncle', 'aunt', 'cousin'], 'unlock_score': 225},
    ]
}

def load_players_data():
    """טעינת נתוני השחקנים מקובץ"""
    try:
        if os.path.exists(PLAYERS_DATA_FILE):
            with open(PLAYERS_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"שגיאה בטעינת נתוני שחקנים: {e}")
    return {}

def save_players_data(players_data):
    """שמירת נתוני השחקנים לקובץ"""
    try:
        with open(PLAYERS_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(players_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"שגיאה בשמירת נתוני שחקנים: {e}")

def create_new_player(name):
    """יצירת שחקן חדש"""
    return {
        'name': name,
        'created_date': datetime.now().isoformat(),
        'last_played': datetime.now().isoformat(),
        'total_score': 0,
        'games_played': 0,
        'levels_progress': {
            'animals': {'current_level': 1, 'completed_levels': [], 'score': 0},
            'colors': {'current_level': 1, 'completed_levels': [], 'score': 0},
            'food': {'current_level': 1, 'completed_levels': [], 'score': 0},
            'family': {'current_level': 1, 'completed_levels': [], 'score': 0}
        }
    }

def init_session():
    """אתחול מפגש משחק"""
    pass  # פונקציה זו מוחלפת במערכת הפרופילים החדשה

def get_available_categories():
    """מחזיר רשימת קטגוריות זמינות"""
    return list(WORDS_DATABASE.keys())

def get_random_words(category, count):
    """מחזיר מילים אקראיות מקטגוריה"""
    if category not in WORDS_DATABASE:
        return []
    
    words = WORDS_DATABASE[category]['words']
    if len(words) < count:
        return words
    
    return random.sample(words, count)

# נתיבים ראשיים
@app.route('/')
def index():
    """מסך בחירת/יצירת שחקן"""
    print("📱 נטען מסך הבית - בחירת שחקן")
    players_data = load_players_data()
    return render_template('index.html', 
                         players=list(players_data.keys()),
                         categories=WORDS_DATABASE)

@app.route('/api/players', methods=['GET'])
def get_players():
    """קבלת רשימת השחקנים"""
    players_data = load_players_data()
    players_list = []
    for name, data in players_data.items():
        players_list.append({
            'name': name,
            'total_score': data.get('total_score', 0),
            'games_played': data.get('games_played', 0),
            'last_played': data.get('last_played', 'מעולם לא')
        })
    return jsonify({'success': True, 'players': players_list})

@app.route('/api/create_player', methods=['POST'])
def create_player():
    """יצירת שחקן חדש"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'success': False, 'error': 'חובה להזין שם'}), 400
        
        players_data = load_players_data()
        
        if name in players_data:
            return jsonify({'success': False, 'error': 'השם כבר קיים'}), 400
        
        # יצירת שחקן חדש
        players_data[name] = create_new_player(name)
        save_players_data(players_data)
        
        print(f"✅ שחקן חדש נוצר: {name}")
        return jsonify({'success': True, 'message': f'שחקן {name} נוצר בהצלחה!'})
        
    except Exception as e:
        print(f"❌ שגיאה ביצירת שחקן: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/select_player', methods=['POST'])
def select_player():
    """בחירת שחקן"""
    try:
        data = request.json
        player_name = data.get('name', '').strip()
        
        players_data = load_players_data()
        
        if player_name not in players_data:
            return jsonify({'success': False, 'error': 'שחקן לא נמצא'}), 400
        
        # עדכון זמן משחק אחרון
        players_data[player_name]['last_played'] = datetime.now().isoformat()
        save_players_data(players_data)
        
        # שמירת השחקן הנוכחי בסשן
        session['current_player'] = player_name
        
        print(f"👤 נבחר שחקן: {player_name}")
        return jsonify({'success': True, 'player': players_data[player_name]})
        
    except Exception as e:
        print(f"❌ שגיאה בבחירת שחקן: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/player_progress', methods=['GET'])
def get_player_progress():
    """קבלת התקדמות השחקן"""
    try:
        player_name = session.get('current_player')
        if not player_name:
            return jsonify({'success': False, 'error': 'לא נבחר שחקן'}), 400
        
        players_data = load_players_data()
        if player_name not in players_data:
            return jsonify({'success': False, 'error': 'שחקן לא נמצא'}), 400
        
        player = players_data[player_name]
        
        # חישוב רמות זמינות לכל קטגוריה
        progress = {}
        for category in WORDS_DATABASE:
            category_progress = player['levels_progress'][category]
            category_score = category_progress['score']
            current_level = category_progress['current_level']
            
            # רמות זמינות
            available_levels = []
            for level_data in LEVELS_SYSTEM[category]:
                if category_score >= level_data['unlock_score']:
                    available_levels.append(level_data)
            
            progress[category] = {
                'current_level': current_level,
                'score': category_score,
                'completed_levels': category_progress['completed_levels'],
                'available_levels': available_levels,
                'total_levels': len(LEVELS_SYSTEM[category])
            }
        
        return jsonify({
            'success': True, 
            'progress': progress,
            'player_info': {
                'name': player['name'],
                'total_score': player['total_score'],
                'games_played': player['games_played']
            }
        })
        
    except Exception as e:
        print(f"❌ שגיאה בקבלת התקדמות: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/start_game', methods=['POST'])
def start_game():
    """התחלת משחק חדש"""
    try:
        data = request.json
        category = data.get('category')
        level = data.get('level', 1)
        
        player_name = session.get('current_player')
        if not player_name:
            return jsonify({'success': False, 'error': 'לא נבחר שחקן'}), 400
        
        print(f"🎮 {player_name} מתחיל משחק - קטגוריה: {category}, רמה: {level}")
        
        if category not in WORDS_DATABASE:
            return jsonify({'success': False, 'error': 'קטגוריה לא קיימת'}), 400
        
        # קבלת מידע הרמה
        level_info = None
        for level_data in LEVELS_SYSTEM[category]:
            if level_data['level'] == level:
                level_info = level_data
                break
        
        if not level_info:
            return jsonify({'success': False, 'error': 'רמה לא קיימת'}), 400
        
        # בחירת מילים לרמה
        level_words = []
        for word_data in WORDS_DATABASE[category]['words']:
            if word_data['english'] in level_info['words']:
                level_words.append(word_data)
        
        if not level_words:
            return jsonify({'success': False, 'error': 'לא נמצאו מילים לרמה זו'}), 400
        
        # הכנת נתוני המשחק
        session['game_data'] = {
            'player_name': player_name,
            'category': category,
            'level': level,
            'level_name': level_info['name'],
            'questions_pool': level_words.copy(),
            'questions_answered': 0,
            'correct_answers': 0,
            'score': 0,
            'current_question': None,
            'total_questions': len(level_words)
        }
        
        print(f"✅ משחק הוכן עם {len(level_words)} מילים ברמה: {level_info['name']}")
        return jsonify({
            'success': True, 
            'total_questions': len(level_words),
            'level_info': level_info
        })
        
    except Exception as e:
        print(f"❌ שגיאה בהתחלת משחק: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/next_question', methods=['GET'])
def next_question():
    """קבלת השאלה הבאה"""
    try:
        game_data = session.get('game_data')
        if not game_data or not game_data.get('questions_pool'):
            print("❌ אין נתוני משחק או שהמשחק הסתיים")
            return jsonify({'success': False, 'error': 'אין משחק פעיל'}), 400
        
        # בחירת שאלה אקראית מהרשימה
        current_word = random.choice(game_data['questions_pool'])
        
        # יצירת תשובות אפשריות
        category = game_data['category']
        all_words = WORDS_DATABASE[category]['words']
        
        # בחירת 3 תשובות שגויות
        wrong_answers = []
        for word in all_words:
            if word['english'] != current_word['english'] and len(wrong_answers) < 3:
                wrong_answers.append(word['english'])
        
        # ערבוב התשובות
        answers = wrong_answers + [current_word['english']]
        random.shuffle(answers)
        
        game_data['current_question'] = current_word
        session['game_data'] = game_data
        
        print(f"❓ נוצרה שאלה חדשה: {current_word['hebrew']} -> {current_word['english']}")
        
        return jsonify({
            'success': True,
            'question': current_word,
            'answers': answers,
            'game_progress': {
                'answered': game_data['questions_answered'],
                'total': game_data['total_questions'],
                'score': game_data['score'],
                'level': game_data['level'],
                'level_name': game_data['level_name']
            }
        })
        
    except Exception as e:
        print(f"❌ שגיאה ביצירת שאלה: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/submit_answer', methods=['POST'])
def submit_answer():
    """בדיקת תשובה ועדכון התקדמות"""
    try:
        data = request.json
        user_answer = data.get('answer', '').strip().lower()
        
        game_data = session.get('game_data')
        if not game_data or not game_data.get('current_question'):
            return jsonify({'success': False, 'error': 'אין שאלה פעילה'}), 400
        
        current_question = game_data['current_question']
        correct_answer = current_question['english'].lower()
        is_correct = user_answer == correct_answer
        
        # עדכון סטטיסטיקות המשחק
        game_data['questions_answered'] += 1
        points_earned = 0
        
        if is_correct:
            game_data['correct_answers'] += 1
            points_earned = 5  # נקודות קבועות לתשובה נכונה
            game_data['score'] += points_earned
            print(f"✅ תשובה נכונה! נקודות: +{points_earned}")
        else:
            print(f"❌ תשובה שגויה. נכון: {correct_answer}, תשובה: {user_answer}")
        
        # הסרת השאלה הנוכחית מהרשימה
        if current_question in game_data['questions_pool']:
            game_data['questions_pool'].remove(current_question)
        
        # בדיקה אם המשחק הסתיים
        game_finished = len(game_data['questions_pool']) == 0
        level_completed = False
        level_up = False
        
        if game_finished:
            print(f"🏁 המשחק הסתיים! ציון: {game_data['score']}")
            
            # עדכון נתוני השחקן
            success_rate = (game_data['correct_answers'] / game_data['total_questions']) * 100
            if success_rate >= 70:  # 70% הצלחה מזכה בהשלמת רמה
                level_completed = True
                level_up = True
                print(f"🎉 רמה הושלמה עם {success_rate:.1f}% הצלחה!")
            
            # שמירת התקדמות השחקן
            save_game_progress(game_data, level_completed)
        
        session['game_data'] = game_data
        
        return jsonify({
            'success': True,
            'is_correct': is_correct,
            'correct_answer': current_question['english'],
            'points_earned': points_earned,
            'game_progress': {
                'answered': game_data['questions_answered'],
                'total': game_data['total_questions'],
                'score': game_data['score'],
                'level': game_data['level'],
                'level_name': game_data['level_name']
            },
            'game_finished': game_finished,
            'level_completed': level_completed,
            'level_up': level_up
        })
        
    except Exception as e:
        print(f"❌ שגיאה בבדיקת תשובה: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def save_game_progress(game_data, level_completed):
    """שמירת התקדמות השחקן"""
    try:
        player_name = game_data['player_name']
        category = game_data['category']
        level = game_data['level']
        score = game_data['score']
        
        players_data = load_players_data()
        if player_name not in players_data:
            return
        
        player = players_data[player_name]
        
        # עדכון נתונים כלליים
        player['total_score'] += score
        player['games_played'] += 1
        player['last_played'] = datetime.now().isoformat()
        
        # עדכון התקדמות בקטגוריה
        category_progress = player['levels_progress'][category]
        category_progress['score'] += score
        
        if level_completed:
            if level not in category_progress['completed_levels']:
                category_progress['completed_levels'].append(level)
            
            # עליה לרמה הבאה
            if level == category_progress['current_level'] and level < 10:
                category_progress['current_level'] = level + 1
        
        save_players_data(players_data)
        print(f"💾 התקדמות נשמרה עבור {player_name}")
        
    except Exception as e:
        print(f"❌ שגיאה בשמירת התקדמות: {e}")

@app.route('/api/exit_game', methods=['POST'])
def exit_game():
    """יציאה מהמשחק ושמירת התקדמות"""
    try:
        game_data = session.get('game_data')
        if game_data:
            # שמירת התקדמות חלקית
            save_game_progress(game_data, False)
        
        # איפוס נתוני המשחק
        session.pop('game_data', None)
        
        return jsonify({'success': True, 'message': 'יצאת מהמשחק בהצלחה'})
        
    except Exception as e:
        print(f"❌ שגיאה ביציאה מהמשחק: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_levels/<category>', methods=['GET'])
def get_levels(category):
    """קבלת רמות עבור קטגוריה מסוימת"""
    try:
        player_name = session.get('current_player')
        if not player_name:
            return jsonify({'success': False, 'error': 'לא נבחר שחקן'}), 400
        
        if category not in WORDS_DATABASE:
            return jsonify({'success': False, 'error': 'קטגוריה לא קיימת'}), 400
        
        players_data = load_players_data()
        if player_name not in players_data:
            return jsonify({'success': False, 'error': 'שחקן לא נמצא'}), 400
        
        player = players_data[player_name]
        category_progress = player['levels_progress'][category]
        category_score = category_progress['score']
        
        # רשימת רמות עם מידע זמינות
        levels_info = []
        for level_data in LEVELS_SYSTEM[category]:
            is_unlocked = category_score >= level_data['unlock_score']
            is_completed = level_data['level'] in category_progress['completed_levels']
            
            levels_info.append({
                'level': level_data['level'],
                'name': level_data['name'],
                'unlock_score': level_data['unlock_score'],
                'is_unlocked': is_unlocked,
                'is_completed': is_completed,
                'words_count': len(level_data['words'])
            })
        
        return jsonify({
            'success': True,
            'category': category,
            'category_name': WORDS_DATABASE[category]['name'],
            'levels': levels_info,
            'player_score': category_score,
            'current_level': category_progress['current_level']
        })
        
    except Exception as e:
        print(f"❌ שגיאה בקבלת רמות: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# פונקציות עזר ישנות (נשמרות לתאימות)
@app.route('/set_name', methods=['POST'])
def set_name():
    """קביעת שם השחקן - פונקציה ישנה לתאימות"""
    return jsonify({'success': False, 'error': 'השתמש במערכת הפרופילים החדשה'}), 400

@app.route('/get_question', methods=['GET'])
def get_question():
    """קבלת השאלה הבאה - פונקציה ישנה"""
    return jsonify({'error': 'השתמש ב-API החדש: /api/next_question'}), 400

@app.route('/submit_answer', methods=['POST'])
def submit_old_answer():
    """בדיקת תשובה - פונקציה ישנה"""
    return jsonify({'error': 'השתמש ב-API החדש: /api/submit_answer'}), 400

@app.route('/get_stats', methods=['GET'])
def get_stats():
    """קבלת סטטיסטיקות השחקן - פונקציה ישנה"""
    return jsonify({'error': 'השתמש ב-API החדש: /api/player_progress'}), 400

if __name__ == '__main__':
    # יצירת תיקיות נדרשות
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("🎮 משחק לימוד אנגלית של עידן - גרסה 2.0 🎮")
    print("✨ עם מערכת פרופילים ו-10 רמות לכל קטגוריה! ✨")
    print("השרת מתחיל...")
    print("גש לכתובת: http://localhost:5000")
    print("או מהטלפון: http://[כתובת-ה-IP-שלך]:5000")
    print("נתוני השחקנים נשמרים ב: players_data.json")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
