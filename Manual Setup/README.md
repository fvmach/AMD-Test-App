# Manual AMD Testing Setup

This manual setup provides step-by-step interactive testing of Twilio's Answering Machine Detection with detailed explanations and educational examples.

## What This Does

- **Interactive Learning** - Step-by-step AMD exploration
- **Educational Examples** - Detailed explanations of each AMD parameter
- **Hands-on Testing** - Manual control over each test call
- **TwiML Demonstrations** - Shows how to handle different AMD results
- **Real-time Analysis** - Monitor and analyze call results as they happen

## Getting Started

### 1. Basic Setup

```bash
# From Manual Setup directory
cd "Manual Setup"

# Start the webhook server (in separate terminal)
python server.py

# In another terminal, start ngrok
ngrok http 5000 --domain=your-domain.ngrok.io
```

### 2. Open the Notebook

```bash
jupyter notebook amd_demo_notebook.ipynb
```

### 3. Follow the Guided Steps

Execute each cell in order to learn about AMD concepts and test different scenarios.

## Learning Path

### Step 1: Understanding AMD Basics

The notebook starts with fundamental concepts:

- What is Answering Machine Detection?
- How does AMD work with Twilio?
- When should you use AMD?
- AMD parameter explanations

### Step 2: AMD Configuration

Learn about the key parameters:

```python
# Example AMD configuration
{
    "machine_detection": "Enable",           # Enable AMD
    "machine_detection_timeout": 10,         # 10 seconds max
    "machine_detection_speech_threshold": 2400,  # 2.4s speech = machine
    "machine_detection_speech_end_threshold": 1200,  # 1.2s silence = end
    "machine_detection_silence_timeout": 5000    # 5s silence = unknown
}
```

### Step 3: Use Case Scenarios

Pre-built scenarios for different situations:

| Scenario | Description | Best For |
|----------|-------------|----------|
| **Machine Detected** | Standard AMD with default sensitivity | General purpose testing |
| **Human Detected** | Higher sensitivity for human detection | Customer service calls |
| **Long Message** | Optimized for lengthy voicemail greetings | Business voicemails |
| **Short Message** | Quick detection for brief greetings | Mobile voicemails |
| **Message Handling** | Advanced TwiML for different results | Production implementations |

## Interactive Features

### Manual Call Control

```python
# Make a test call with specific configuration
call = make_amd_call(
    from_number="+15551234567",
    to_number="+15557654321", 
    use_case_id="1"  # Machine detection scenario
)
```

### Real-time Monitoring

```python
# Watch call progress live
monitor_call_status(call.sid, max_wait_time=60)

# Output:
# 14:32:15 - Status: queued
# 14:32:16 - Status: ringing  
# 14:32:20 - Status: in-progress
# AMD Result: machine
# 14:32:25 - Status: completed
```

### Result Analysis

```python
# Analyze recent calls and their AMD results
analyze_recent_calls(limit=10)

# Shows:
# - Call SIDs and statuses
# - AMD detection results
# - Success/failure statistics
```

## 🛠️ TwiML Examples

### Basic AMD Handler

```xml
<!-- For human detection -->
<Response>
    <Say voice="alice">
        Hello! Thank you for answering. This is a test call 
        demonstrating Answering Machine Detection.
    </Say>
</Response>
```

### Advanced AMD Handler

```python
@app.route("/handle_amd", methods=['POST'])
def handle_amd():
    amd_result = request.form.get('AnsweringMachineDetection')
    response = VoiceResponse()
    
    if amd_result == 'machine':
        response.pause(length=1)  # Wait for beep
        response.say("This is a message for your voicemail...")
    elif amd_result == 'human':
        response.say("Hello! A human answered the phone.")
    
    return str(response)
```

## Educational Examples

### Parameter Impact Demonstration

```python
# Show how different parameters affect detection
configs = {
    "sensitive": {"speech_threshold": 1500},    # Detects machines faster
    "conservative": {"speech_threshold": 3000}, # More careful detection
    "quick": {"timeout": 5},                   # Fast timeout
    "patient": {"timeout": 20}                 # Longer detection window
}
```

### Scenario Comparisons

Test the same phone number with different configurations:

1. **Quick Detection** (8s timeout) vs **Patient Detection** (20s timeout)
2. **Sensitive** (1500ms threshold) vs **Conservative** (3000ms threshold)
3. **Standard AMD** vs **DetectMessageEnd** mode

## Learning Objectives

By working through this manual setup, you'll understand:

1. **AMD Parameter Effects** - How each setting impacts detection
2. **Use Case Matching** - Which configurations work for different scenarios  
3. **Result Handling** - How to process different AMD outcomes
4. **Performance Tuning** - Optimizing parameters for your use case
5. **Production Implementation** - Best practices for real applications

## 📋 Step-by-Step Workflow

### 1. Environment Setup
- Configure Twilio credentials
- Start webhook server
- Test basic connectivity

### 2. Basic AMD Test
- Make your first AMD-enabled call
- Observe webhook callbacks
- Understand the detection process

### 3. Parameter Exploration
- Test different timeout values
- Adjust speech thresholds
- Compare detection accuracy

### 4. Scenario Testing
- Test with known voicemails
- Try different phone types
- Document what works best

### 5. TwiML Integration
- Build response handlers
- Implement different actions per result
- Test complete call flows

## 🔧 Webhook Server Features

The manual setup server provides:

### Detailed Logging
```
--- AMD TwiML HANDLER (AMD_RESULT) [POST] ---
>> Call SID: CAxxxxxxxxxx
>> Call Status: in-progress
>> AMD Result: human
>> Action: Speaking to human
>> Message: Hello! A human answered...
```

### Parameter Display
```
[AMD Details]:
   MachineDetectionDuration: 3500
   MachineDetectionTimeout: 10
   MachineDetectionSpeechThreshold: 2400
```

### Multiple Endpoints
- `/webhook` - Basic AMD callback logging
- `/handle_amd` - TwiML response generator
- `/status` - Server health check

## Common Learning Points

### False Positives/Negatives

**Human detected as machine:**
- Speech threshold too low
- Person spoke immediately without pause
- Long greeting mistaken for voicemail

**Machine detected as human:**
- Speech threshold too high  
- Very short voicemail greeting
- Background noise interference

### Optimization Strategies

1. **Start Conservative** - Use longer timeouts initially
2. **Test Real Scenarios** - Use actual target phone numbers
3. **Measure Results** - Track accuracy over time
4. **Adjust Gradually** - Make small parameter changes
5. **Document Findings** - Keep notes on what works

## Files Overview

- **`amd_demo_notebook.ipynb`** - Interactive learning notebook
- **`server.py`** - Educational webhook server with detailed explanations

This manual setup is perfect for learning AMD concepts, understanding parameter effects, and building confidence before implementing production solutions.