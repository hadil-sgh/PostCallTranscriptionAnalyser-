from flask import Flask, request, jsonify
from TranscriptAnalyzer import analyze_transcript

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/score', methods=['POST'])
def score():
    data = request.get_json()
    transcript_id = data.get('transcript_id')

    if not transcript_id:
        return jsonify({'error': 'Missing transcript_id'}), 400

    transcript = get_transcript_from_db(transcript_id)
    if not transcript:
        return jsonify({'error': 'Transcript not found'}), 404

    result = analyze_transcript(transcript)
    return jsonify(result), 200

def get_transcript_from_db(transcript_id):
    # Simulated mock database of transcripts (speaker tags removed)
    mock_db = {
        "1": (
            "Hello, how can I help you?\n"
            "My internet has been down since yesterday afternoon.\n"
            "Did you try restarting it?\n"
            "Yes, several times. Nothing works.\n"
            "Hm okay. Well, maybe it's a local outage. I’m not sure.\n"
            "Can you check?\n"
            "I mean… I guess I can look it up, hold on.\n"
            "(waits for 2 minutes)\n"
            "Yeah, there's no info here. Probably just your device.\n"
            "It’s not just my device. I called yesterday too.\n"
            "Oh, then I don’t really know what else to say.\n"
            "Can I speak to a supervisor?\n"
            "They're not here right now. Try calling back later.\n"
            "This is very unhelpful.\n"
            "Well I can’t fix it if I don’t know what’s wrong, can I?\n"
            "I’m really frustrated.\n"
            "Yeah okay, well, sorry or whatever. Call again tomorrow.\n"
        ),
        "2": (
            "Good morning.\n"
            "I want to cancel my subscription.\n"
            "Okay... why?\n"
            "I’m not happy with the service.\n"
            "Huh. You sure? It’s a pretty good deal.\n"
            "I’ve had multiple issues and no resolution.\n"
            "I guess I can cancel it. Hold on. *long pause*\n"
            "Are you still there?\n"
            "Yeah. Just canceling it... wait.\n"
            "Okay.\n"
            "Actually, I can’t cancel right now, system's slow. Try online maybe.\n"
            "What?\n"
            "Yeah, just go on the website. It's faster.\n"
            "I tried, it told me to call.\n"
            "Well I can’t help if the system isn’t working. Bye.\n"
        )
    }

    return mock_db.get(transcript_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
