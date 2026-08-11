from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# GET /events - Retrieve all events (helpful for testing)
@app.route('/events', methods=['GET'])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# POST /events - Create a new event from JSON input
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()

    # Validate that JSON was provided and contains a 'title'
    if not data or 'title' not in data:
        return jsonify({"error": "Missing 'title' in JSON body"}), 400

    # Generate a new ID (find max existing ID and add 1)
    new_id = max([e.id for e in events], default=0) + 1

    # Create event object and append to our list
    new_event = Event(new_id, data['title'])
    events.append(new_event)

    # Return 201 Created status with the new event data
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<id> - Update the title of an event
@app.route('/events/<int:id>', methods=['PATCH'])
def update_event(id):
    data = request.get_json()

    # Validate JSON input
    if not data or 'title' not in data:
        return jsonify({"error": "Missing 'title' in JSON body"}), 400

    # Search for the event by ID
    for event in events:
        if event.id == id:
            # Update the title and return 200 OK
            event.title = data['title']
            return jsonify(event.to_dict()), 200

    # If loop finishes without returning, the ID was not found
    return jsonify({"error": "Event not found"}), 404

# DELETE /events/<id> - Remove an event from the list
@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    # Search for the event by ID using enumerate to get the index
    for index, event in enumerate(events):
        if event.id == id:
            # Remove from list and return 204 No Content (empty body)
            del events[index]
            return '', 204

    # Return 404 Not Found if ID does not exist
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)