import os
from flask import Flask, render_template, jsonify
import logging
from dotenv import load_dotenv
import pickle
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")


@app.route('/')
def index():
    """Home page for the RPG bot dashboard."""
    return render_template('index.html', title="Mortem House Stat - RPG Bot Dashboard")


@app.route('/api/stats')
def stats():
    """API endpoint to get bot statistics."""
    try:
        # Load the database
        db_path = Path("rpg_database.pkl")
        if not db_path.exists():
            return jsonify({
                'users': 0,
                'items': 0,
                'commands_used': 0
            })

        with open(db_path, 'rb') as f:
            data = pickle.load(f)

        return jsonify({
            'users': len(data.get('users', {})),
            'items': sum(len(inventory) for inventory in data.get('inventories', {}).values()),
            'commands_used': len(data.get('cooldowns', {}))
        })
    except Exception as e:
        logger.error(f"Error loading stats: {e}")
        return jsonify({'error': 'Failed to load stats'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)