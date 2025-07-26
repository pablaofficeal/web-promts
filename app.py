from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prompts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# === Загрузка конфигураций ===
def load_json(filename, folder='config'):
    path = os.path.join(folder, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_tech_by_id(tech_id):
    techs = load_json('technologies.json')
    return next((t for t in techs if t['id'] == tech_id), None)

# === ORM ===
class PromptGeneration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    technology = db.Column(db.String(50), nullable=False)
    framework = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'technology': self.technology,
            'framework': self.framework,
            'language': self.language,
            'prompt': self.prompt,
            'timestamp': self.timestamp.isoformat()
        }

# === API ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/technologies', methods=['GET'])
def get_technologies():
    techs = load_json('technologies.json')
    return jsonify([{'id': t['id'], 'name': t['name']} for t in techs])

@app.route('/api/frameworks/<tech_id>', methods=['GET'])
def get_frameworks(tech_id):
    frameworks = load_json('frameworks.json').get(tech_id, [])
    return jsonify(frameworks)

@app.route('/api/languages/<tech_id>/<framework_id>', methods=['GET'])
def get_languages(tech_id, framework_id):
    frameworks = load_json('frameworks.json').get(tech_id, [])
    framework = next((f for f in frameworks if f['id'] == framework_id), None)
    if framework:
        return jsonify(framework.get('languages', []))
    return jsonify([])

@app.route('/api/prompts', methods=['GET'])
def get_all_prompts():
    # Загружаем все промпты из папки prompts
    prompts = {}
    prompts_dir = os.path.join('config', 'prompts')
    if os.path.exists(prompts_dir):
        for filename in os.listdir(prompts_dir):
            if filename.endswith('.json'):
                tech_id = filename.replace('.json', '')
                prompts[tech_id] = load_json(f'prompts/{filename}')
    return jsonify(prompts)

@app.route('/api/generate', methods=['POST'])
def generate_prompt():
    data = request.get_json()
    tech_id = data.get('technology')
    framework_id = data.get('framework')

    if not tech_id or not framework_id:
        return jsonify({'error': 'Технология и фреймворк обязательны'}), 400

    # Загружаем данные
    tech = get_tech_by_id(tech_id)
    if not tech:
        return jsonify({'error': 'Технология не найдена'}), 404

    frameworks = load_json('frameworks.json').get(tech_id, [])
    framework = next((f for f in frameworks if f['id'] == framework_id), None)
    if not framework:
        return jsonify({'error': 'Фреймворк не найден'}), 404

    # Получаем язык из запроса или используем первый доступный
    language = data.get('language')
    if not language:
        available_languages = framework.get('languages', [])
        language = available_languages[0] if available_languages else 'unknown'

    # Пытаемся найти готовый промпт для конкретного языка
    try:
        prompts = load_json(f'prompts/{tech_id}.json')
        framework_prompts = prompts.get(framework_id, {})
        prompt = framework_prompts.get(language)
    except:
        prompt = None
    
    # Если готового промпта нет, используем шаблон
    if not prompt:
        rules = load_json('prompt_rules.json')
        template = rules.get(tech_id)
        if not template:
            return jsonify({'error': 'Шаблон промта не найден'}), 500

        try:
            prompt = template.format(
                framework_name=framework['name'],
                language=language
            )
        except Exception as e:
            return jsonify({'error': 'Ошибка генерации промта'}), 500

    # Логируем
    try:
        log_entry = PromptGeneration(
            technology=tech_id,
            framework=framework_id,
            language=language,
            prompt=prompt
        )
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Логирование не удалось: {e}")

    return jsonify({'prompt': prompt})

# === Запуск ===
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Запускаем в production режиме для Docker
    app.run(host='0.0.0.0', port=5045, debug=False)