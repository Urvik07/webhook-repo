from flask import Blueprint, request, jsonify, render_template
from app import mongo
from datetime import datetime
import pytz

webhook = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    """
    Endpoint to receive and process GitHub webhook events.
    It handles 'push' and 'pull_request' events and stores them in the MongoDB.
    """
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        # Process push event
        event = {
            '_id': f"{data['after']}_PUSH",
            'request_id': data['after'],
            'author': data['pusher']['name'],
            'action': 'PUSH',
            'from_branch': data['ref'].split('/')[-1],
            'to_branch': data['ref'].split('/')[-1],
            'timestamp': datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        mongo.db.events.insert_one(event)

    elif event_type == 'pull_request':
        # Process pull request event
        pull_request_action = data['action']
        action = 'PULL_REQUEST'
        # For Merge event
        if pull_request_action == 'closed' and data['pull_request']['merged']: 
            action = 'MERGE'
        print(action)
        event = {
            '_id': f"{data['pull_request']['id']}_{action}",
            'request_id': str(data['pull_request']['id']),
            'author': data['pull_request']['user']['login'],
            'action': action,
            'from_branch': data['pull_request']['head']['ref'],
            'to_branch': data['pull_request']['base']['ref'],
            'timestamp': datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        mongo.db.events.insert_one(event)

    return jsonify({'status': 'success'}), 200

@webhook.route('/events', methods=['GET'])
def get_events():
    """
    Endpoint to fetch the latest 10 events from the MongoDB.
    The events are sorted by timestamp in descending order.
    """
    events = list(mongo.db.events.find({}, {'_id': 0}).sort('timestamp', -1).limit(10))
    return jsonify(events)

@webhook.route('/', methods=['GET'])
def index():
    """
    Render the index.html template.
    """
    return render_template('index.html')
