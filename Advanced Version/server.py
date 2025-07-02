# Start a simple Flask server for webhook handling
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import time
import json
from urllib.parse import unquote

app = Flask(__name__)

def parse_webhook_data(request_obj):
    """Parse and format webhook data from either GET or POST request"""
    data = {}
    
    # Get data from either form (POST) or args (GET)
    if request_obj.method == 'POST':
        form_data = request_obj.form
    else:  # GET request
        form_data = request_obj.args
    
    # Common Twilio parameters
    common_params = {
        'AccountSid': 'Account SID',
        'CallSid': 'Call SID',
        'CallStatus': 'Call Status',
        'From': 'From Number',
        'To': 'To Number',
        'Caller': 'Caller Number',
        'Called': 'Called Number',
        'Direction': 'Call Direction',
        'ApiVersion': 'API Version',
        'CallDuration': 'Call Duration',
        'Duration': 'Duration (seconds)',
        'RecordingUrl': 'Recording URL',
        'SipResponseCode': 'SIP Response Code',
    }
    
    # AMD-specific parameters
    amd_params = {
        'AnsweredBy': 'AMD Result',
        'AnsweringMachineDetection': 'AMD Detection',
        'MachineDetectionDuration': 'AMD Duration (ms)',
        'MachineDetectionSilenceTimeout': 'AMD Silence Timeout (ms)',
        'MachineDetectionSpeechThreshold': 'AMD Speech Threshold (ms)',
        'MachineDetectionSpeechEndThreshold': 'AMD Speech End Threshold (ms)',
        'MachineDetectionTimeout': 'AMD Timeout (s)',
    }
    
    # Status callback parameters
    status_params = {
        'CallbackSource': 'Callback Source',
        'SequenceNumber': 'Sequence Number',
        'Timestamp': 'Timestamp',
    }
    
    # Geographic parameters
    geo_params = {
        'FromCountry': 'From Country',
        'FromState': 'From State', 
        'FromCity': 'From City',
        'FromZip': 'From ZIP',
        'ToCountry': 'To Country',
        'ToState': 'To State',
        'ToCity': 'To City',
        'ToZip': 'To ZIP',
        'CallerCountry': 'Caller Country',
        'CallerState': 'Caller State',
        'CallerCity': 'Caller City',
        'CallerZip': 'Caller ZIP',
        'CalledCountry': 'Called Country',
        'CalledState': 'Called State',
        'CalledCity': 'Called City',
        'CalledZip': 'Called ZIP',
    }
    
    # Parse all parameters
    all_params = {**common_params, **amd_params, **status_params, **geo_params}
    
    for key, value in form_data.items():
        # URL decode the value
        decoded_value = unquote(str(value))
        
        if key in all_params:
            data[all_params[key]] = decoded_value
        else:
            data[key] = decoded_value
    
    return data

def get_webhook_type(request_obj):
    """Determine the type of webhook based on the data"""
    # Get data from either form (POST) or args (GET)
    if request_obj.method == 'POST':
        form_data = request_obj.form
    else:
        form_data = request_obj.args
        
    if form_data.get('AnsweredBy') or form_data.get('AnsweringMachineDetection'):
        return "AMD_RESULT"
    elif form_data.get('CallStatus'):
        return "STATUS_CALLBACK"
    elif form_data.get('RecordingUrl'):
        return "RECORDING_CALLBACK"
    else:
        return "UNKNOWN"

@app.route("/webhook", methods=['GET', 'POST'])
def handle_webhook():
    """Handle Twilio webhooks for AMD status updates - caller stays silent"""
    webhook_type = get_webhook_type(request)
    parsed_data = parse_webhook_data(request)
    
    print("\n" + "="*70)
    print(f"--- AMD WEBHOOK RECEIVED ({webhook_type}) [{request.method}] ---")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Display key information prominently
    key_info = []
    if 'Call SID' in parsed_data:
        key_info.append(f"Call SID: {parsed_data['Call SID']}")
    if 'Call Status' in parsed_data:
        key_info.append(f"Status: {parsed_data['Call Status']}")
    if 'AMD Result' in parsed_data:
        key_info.append(f"AMD Result: {parsed_data['AMD Result']}")
        
        # Show AMD result interpretation
        amd_result = parsed_data['AMD Result'].lower()
        if amd_result == 'human':
            key_info.append("   ✅ Human detected - real person answered")
        elif amd_result in ['machine_start', 'machine_end_beep', 'machine_end_silence', 'machine_end_other', 'machine']:
            key_info.append("   🤖 Machine detected - answering machine/voicemail")
        elif amd_result == 'fax':
            key_info.append("   📠 Fax machine detected")
        elif amd_result == 'unknown':
            key_info.append("   ❓ Unknown - could not determine human vs machine")
        else:
            key_info.append(f"   ❓ Unrecognized AMD result: {amd_result}")
    
    if 'AMD Duration (ms)' in parsed_data:
        duration = parsed_data['AMD Duration (ms)']
        key_info.append(f"AMD Duration: {duration}ms ({float(duration)/1000:.2f}s)")
    
    if 'Sequence Number' in parsed_data:
        key_info.append(f"Sequence: {parsed_data['Sequence Number']}")
    if 'Callback Source' in parsed_data:
        key_info.append(f"Source: {parsed_data['Callback Source']}")
    
    for info in key_info:
        print(f">> {info}")
    
    print("\n" + "-"*50)
    print("DETAILED WEBHOOK DATA:")
    print("-"*50)
    
    # Group data by category
    categories = {
        'Call Information': ['Call SID', 'Call Status', 'From Number', 'To Number', 'Caller Number', 'Called Number', 'Call Direction', 'Duration (seconds)', 'Call Duration', 'SIP Response Code'],
        'AMD Results': ['AMD Result', 'AMD Detection', 'AMD Duration (ms)', 'AMD Timeout (s)', 'AMD Silence Timeout (ms)', 'AMD Speech Threshold (ms)', 'AMD Speech End Threshold (ms)'],
        'Callback Information': ['Callback Source', 'Sequence Number', 'Timestamp', 'API Version'],
        'Geographic Information': ['From Country', 'From State', 'From City', 'From ZIP', 'To Country', 'To State', 'To City', 'To ZIP', 'Caller Country', 'Caller State', 'Caller City', 'Caller ZIP', 'Called Country', 'Called State', 'Called City', 'Called ZIP'],
        'Other': []
    }
    
    # Categorize data
    categorized_data = {cat: {} for cat in categories}
    for key, value in parsed_data.items():
        categorized = False
        for category, fields in categories.items():
            if key in fields:
                categorized_data[category][key] = value
                categorized = True
                break
        if not categorized:
            categorized_data['Other'][key] = value
    
    # Display categorized data
    for category, data in categorized_data.items():
        if data:  # Only show categories with data
            print(f"\n[{category}]:")
            for key, value in data.items():
                # Don't show empty values
                if value and value.strip():
                    print(f"   {key}: {value}")
    
    # Show test scenario context
    print(f"\n[TEST SCENARIO CONTEXT]:")
    print(f"   Caller: Twilio number with AMD enabled (stays silent)")
    print(f"   Callee: Twilio number with Studio flow (simulates scenarios)")
    print(f"   AMD Purpose: Detect if Studio flow simulates human or machine")
    print(f"   No Messages: Caller doesn't play messages - Studio handles everything")
    
    print("="*70 + "\n")
    
    # Return empty TwiML response - caller stays silent
    response = VoiceResponse()
    return str(response)

@app.route("/silent", methods=['GET', 'POST'])
def handle_silent():
    """Keep caller silent to allow AMD detection of callee's Studio flow"""
    print("\n" + "="*50)
    print("--- SILENT ENDPOINT CALLED ---")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    print(">> Action: Keeping caller silent for AMD detection")
    print(">> Duration: 60 seconds (allows AMD to analyze callee)")
    print(">> Callee: Studio flow will simulate human/machine scenarios")
    print(">> Caller: Stays silent - no messages played")
    print("="*50 + "\n")
    
    response = VoiceResponse()
    # Keep caller silent for 60 seconds to allow AMD detection
    response.pause(length=60)
    return str(response)

@app.route("/status", methods=['GET'])
def status():
    """Simple status endpoint"""
    return {
        "status": "running",
        "server": "Twilio AMD Testing Server",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "purpose": "AMD testing with caller staying silent",
        "endpoints": ["/webhook", "/silent", "/status"],
        "test_setup": {
            "caller": "Twilio number with AMD enabled (stays silent)",
            "callee": "Twilio number with Studio flow (simulates scenarios)",
            "amd_purpose": "Detect if Studio flow simulates human or machine"
        },
        "accepts": "GET and POST requests"
    }

@app.route("/", methods=['GET'])
def home():
    """Home page with server info"""
    return """
    <h1>Twilio AMD Testing Server</h1>
    <p><strong>Purpose:</strong> AMD testing where caller stays silent and callee Studio flow simulates scenarios</p>
    
    <h2>Test Setup</h2>
    <ul>
        <li><strong>Caller:</strong> Twilio number with AMD enabled (stays silent)</li>
        <li><strong>Callee:</strong> Twilio number with Studio flow (simulates human/machine scenarios)</li>
        <li><strong>AMD Purpose:</strong> Detect if Studio flow simulates human or machine</li>
    </ul>
    
    <h2>Endpoints</h2>
    <ul>
        <li><strong>/webhook</strong> - AMD callback endpoint (GET/POST) - logs AMD results</li>
        <li><strong>/silent</strong> - TwiML endpoint (GET/POST) - keeps caller silent for 60s</li>
        <li><strong>/status</strong> - Server status (JSON)</li>
    </ul>
    
    <h2>How It Works</h2>
    <ol>
        <li>Caller (Twilio number) calls callee (Twilio number) with AMD enabled</li>
        <li>Caller gets TwiML from /silent endpoint - stays quiet for 60 seconds</li>
        <li>Callee Studio flow simulates different answering scenarios (human/machine)</li>
        <li>AMD analyzes callee's response and sends results to /webhook</li>
        <li>Server logs AMD results for analysis and fine-tuning</li>
    </ol>
    
    <p><strong>No messages are played by the caller</strong> - this is pure AMD detection testing!</p>
    <p>Check the console for webhook logs and AMD results.</p>
    """

if __name__ == "__main__":
    PORT = 5000
    print("Starting Twilio AMD Testing Server...")
    print(f"Server will run on port {PORT}")
    print(f"Purpose: AMD testing with caller staying silent")
    print(f"\nTest Setup:")
    print(f"   Caller: Twilio number with AMD enabled (stays silent)")
    print(f"   Callee: Twilio number with Studio flow (simulates scenarios)")
    print(f"   AMD Purpose: Detect if Studio flow simulates human or machine")
    print(f"\nEndpoints:")
    print(f"   - /webhook (AMD callbacks)")
    print(f"   - /silent (keeps caller silent)")
    print(f"   - /status (server info)")
    print("\n" + "="*60)
    print("To start ngrok in another terminal:")
    print("   ngrok http 5000 --domain=owlbank.ngrok.io")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=PORT, debug=True)