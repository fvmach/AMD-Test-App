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
        'MachineDetectionDuration': 'AMD Duration',
        'MachineDetectionSilenceTimeout': 'AMD Silence Timeout',
        'MachineDetectionSpeechThreshold': 'AMD Speech Threshold',
        'MachineDetectionSpeechEndThreshold': 'AMD Speech End Threshold',
        'MachineDetectionTimeout': 'AMD Timeout',
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
    """Handle Twilio webhooks for call status updates"""
    webhook_type = get_webhook_type(request)
    parsed_data = parse_webhook_data(request)
    
    print("\n" + "="*60)
    print(f"--- WEBHOOK RECEIVED ({webhook_type}) [{request.method}] ---")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Display key information prominently
    key_info = []
    if 'Call SID' in parsed_data:
        key_info.append(f"Call SID: {parsed_data['Call SID']}")
    if 'Call Status' in parsed_data:
        key_info.append(f"Status: {parsed_data['Call Status']}")
    if 'AMD Result' in parsed_data:
        key_info.append(f"AMD Result: {parsed_data['AMD Result']}")
    if 'AMD Detection' in parsed_data:
        key_info.append(f"AMD Detection: {parsed_data['AMD Detection']}")
    if 'Sequence Number' in parsed_data:
        key_info.append(f"Sequence: {parsed_data['Sequence Number']}")
    if 'Callback Source' in parsed_data:
        key_info.append(f"Source: {parsed_data['Callback Source']}")
    
    for info in key_info:
        print(f">> {info}")
    
    print("\n" + "-"*40)
    print("PARSED WEBHOOK DATA:")
    print("-"*40)
    
    # Group data by category
    categories = {
        'Call Information': ['Call SID', 'Call Status', 'From Number', 'To Number', 'Caller Number', 'Called Number', 'Call Direction', 'Duration (seconds)', 'Call Duration', 'SIP Response Code'],
        'AMD Information': ['AMD Result', 'AMD Detection', 'AMD Duration', 'AMD Timeout', 'AMD Silence Timeout', 'AMD Speech Threshold', 'AMD Speech End Threshold'],
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
    
    print("="*60 + "\n")
    
    response = VoiceResponse()
    return str(response)

@app.route("/handle_amd", methods=['GET', 'POST'])
def handle_amd():
    """Handle AMD results with TwiML response"""
    webhook_type = get_webhook_type(request)
    parsed_data = parse_webhook_data(request)
    
    print("\n" + "="*60)
    print(f"--- AMD TwiML HANDLER ({webhook_type}) [{request.method}] ---")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Get AMD result from different possible parameter names
    form_data = request.form if request.method == 'POST' else request.args
    answered_by = (form_data.get('AnsweredBy') or 
                   form_data.get('AnsweringMachineDetection') or 
                   'unknown').lower()
    
    call_sid = form_data.get('CallSid', 'N/A')
    call_status = form_data.get('CallStatus', 'N/A')
    
    print(f">> Call SID: {call_sid}")
    print(f">> Call Status: {call_status}")
    print(f">> AMD Result: {answered_by}")
    
    # Show additional AMD details if available
    amd_details = {}
    amd_fields = ['MachineDetectionDuration', 'MachineDetectionSilenceTimeout', 
                  'MachineDetectionSpeechThreshold', 'MachineDetectionSpeechEndThreshold']
    
    for field in amd_fields:
        if form_data.get(field):
            amd_details[field] = form_data.get(field)
    
    if amd_details:
        print(f"\n[AMD Details]:")
        for field, value in amd_details.items():
            print(f"   {field}: {value}")
    
    print("-"*60)
    
    response = VoiceResponse()
    
    # Handle different AMD results
    if answered_by in ['machine_start', 'machine_end_beep', 'machine_end_silence', 'machine_end_other', 'machine']:
        message = "This is a message for your answering machine. Have a great day!"
        print(f">> Action: Playing message for answering machine")
        print(f">> Message: {message}")
        response.say(message, voice='alice')
        response.hangup()
        
    elif answered_by == 'human':
        message = "Hello! A human answered. This is a test call from Twilio's AMD demo."
        print(f">> Action: Speaking to human")
        print(f">> Message: {message}")
        response.say(message, voice='alice')
        
    elif answered_by == 'fax':
        message = "Fax machine detected. Hanging up."
        print(f">> Action: Fax detected - hanging up")
        print(f">> Message: {message}")
        response.say(message, voice='alice')
        response.hangup()
        
    else:
        message = "Could not determine if human or machine answered. This is a test call."
        print(f">> Action: Unknown AMD result - playing generic message")
        print(f">> Message: {message}")
        response.say(message, voice='alice')
    
    print("="*60 + "\n")
    
    return str(response)

@app.route("/status", methods=['GET'])
def status():
    """Simple status endpoint"""
    return {
        "status": "running",
        "server": "Twilio AMD Demo Server",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "endpoints": ["/webhook", "/handle_amd", "/status"],
        "accepts": "GET and POST requests"
    }

@app.route("/", methods=['GET'])
def home():
    """Home page with server info"""
    return """
    <h1>Twilio AMD Demo Server</h1>
    <p>Server is running and ready to receive webhooks!</p>
    <ul>
        <li><strong>/webhook</strong> - Main webhook endpoint for AMD callbacks (GET/POST)</li>
        <li><strong>/handle_amd</strong> - TwiML handler for AMD results (GET/POST)</li>
        <li><strong>/status</strong> - Server status (JSON)</li>
    </ul>
    <p>Check the console for webhook logs.</p>
    <p><em>Note: This server accepts both GET and POST requests to handle different webhook configurations.</em></p>
    """

if __name__ == "__main__":
    PORT = 5000
    print("Starting Twilio AMD Demo Server...")
    print(f"Server will run on port {PORT}")
    print(f"Public URL: https://owlbank.ngrok.io (when ngrok is running)")
    print(f"Webhook endpoints:")
    print(f"   - https://owlbank.ngrok.io/webhook (GET/POST)")
    print(f"   - https://owlbank.ngrok.io/handle_amd (GET/POST)")
    print("\n" + "="*60)
    print("To start ngrok in another terminal:")
    print("   ngrok http 5000 --domain=owlbank.ngrok.io")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=PORT, debug=True)