# Answering Machine Simulator with Twilio Studio

This component uses Twilio Studio flows to simulate different answering scenarios, providing controlled and repeatable AMD testing environments.

## What This Does

- **Simulates Human Responses** - Studio flows that mimic real person behavior
- **Creates Machine Scenarios** - Voicemail greeting simulations
- **Provides Consistent Testing** - Repeatable scenarios for AMD tuning
- **Enables A/B Testing** - Compare AMD configurations against known scenarios
- **Supports Edge Cases** - Test unusual situations like long greetings, silence, etc.

## How It Works

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   AMD Caller    │───▶│ Twilio Voice │───▶│ Studio Flow     │
│ (Your Script)   │    │     API      │    │ (Simulates      │
│                 │    │              │    │  Response)      │
└─────────────────┘    └──────────────┘    └─────────────────┘
         │                                          │
         ▼                                          ▼
┌─────────────────┐                      ┌─────────────────┐
│ AMD Results     │                      │ Controlled      │
│ (Human/Machine) │                      │ Behavior        │
└─────────────────┘                      └─────────────────┘
```

## Scenario Types

### 1. Human Response Scenarios

**Quick Human Answer**
```
Flow: Answer immediately → Say "Hello?" → Wait for response
AMD Expected: human
Use Case: Testing fast human detection
```

**Hesitant Human Answer**  
```
Flow: Pause 2s → Say "Hello... who is this?" → Wait
AMD Expected: human  
Use Case: Testing detection with initial silence
```

**Chatty Human Answer**
```
Flow: Say "Hi there! Thanks for calling, how can I help you today?"
AMD Expected: human (might be detected as machine if threshold too low)
Use Case: Testing long human greetings
```

### 2. Machine Response Scenarios

**Standard Voicemail**
```
Flow: Pause 1s → Play voicemail greeting → Play beep tone
AMD Expected: machine_end_beep
Use Case: Typical answering machine detection
```

**Long Business Voicemail**
```
Flow: Play 15-second business greeting → Beep
AMD Expected: machine_end_beep  
Use Case: Testing timeout and speech threshold limits
```

**Voicemail with Music**
```
Flow: Play hold music → Voicemail greeting → Beep
AMD Expected: machine_end_beep
Use Case: Testing detection with background audio
```

### 3. Edge Case Scenarios

**Silent Pickup**
```
Flow: Answer → Silence for 10 seconds → Hangup
AMD Expected: unknown
Use Case: Testing silence timeout
```

**Fax Machine**
```
Flow: Play fax tones
AMD Expected: fax
Use Case: Testing fax detection
```

**Call Screening**
```
Flow: "Please hold while we connect..." → Transfer to voicemail
AMD Expected: machine (might be detected as human initially)
Use Case: Testing complex call flows
```


## Phone Number Configuration

### Setup Process

1. **Get Twilio Phone Numbers**
   - Caller number (for your AMD script)
   - Callee number (for Studio flow)

2. **Configure Studio Flow**
   ```bash
   # Create new Studio flow
   # Copy JSON configuration
   # Assign to phone number webhook
   ```

3. **Set Webhook URL**
   ```
   Phone Number → Voice Configuration → Webhook
   https://webhooks.twilio.com/v1/Accounts/{AccountSid}/Flows/{FlowSid}
   ```

### Testing Setup

```python
# Configure your AMD test
FROM_NUMBER = "+15551234567"  # Your Twilio number
TO_NUMBER = "+15557654321"    # Number with Studio flow

# Make AMD call to Studio flow
call = make_amd_call('residential_fast')
```

## Test Scenarios

### A/B Testing Different Flows

Create multiple Studio flows for comparison:

```python
# Test numbers with different Studio flows
HUMAN_SIMULATION = "+15551111111"    # Quick human response
MACHINE_SIMULATION = "+15552222222"  # Standard voicemail  
EDGE_CASE_SIMULATION = "+15553333333" # Silent pickup

# Test same AMD config against different scenarios
results = {}
for name, number in scenarios.items():
    call = make_amd_call('business_standard', to_number=number)
    results[name] = monitor_call_results(call.sid)
```

### Parameter Optimization

Use Studio flows to test AMD parameter effects:

```python
# Test different speech thresholds against same Studio flow
configs = [
    {"name": "sensitive", "speech_threshold": 1500},
    {"name": "standard", "speech_threshold": 2400}, 
    {"name": "conservative", "speech_threshold": 3500}
]

for config in configs:
    # Test against voicemail simulation
    call = make_amd_call_with_params(
        to_number=MACHINE_SIMULATION,
        **config
    )
```


## Performance Analysis

### Measuring AMD Accuracy

```python
# Track accuracy across different scenarios
test_results = {
    "human_scenarios": {
        "total_tests": 50,
        "correct_detections": 47,
        "accuracy": 94.0
    },
    "machine_scenarios": {
        "total_tests": 50, 
        "correct_detections": 49,
        "accuracy": 98.0
    }
}
```

### Configuration Optimization

Use Studio flows to find optimal parameters:

1. **Create baseline flows** for human/machine scenarios
2. **Test multiple AMD configurations** against each flow
3. **Measure accuracy and speed** for each combination
4. **Optimize parameters** based on your use case priorities

## Implementation Tips

### Best Practices

1. **Start Simple** - Begin with basic human/machine flows
2. **Add Complexity Gradually** - Introduce edge cases as you tune
3. **Use Real Audio** - Record actual voicemail greetings when possible
4. **Test Edge Cases** - Silent pickups, long greetings, background noise
5. **Document Results** - Track which flows work best with which configurations

### Common Gotchas

- **Studio flow delays** - Account for flow processing time
- **Audio quality** - Use clear, realistic audio samples
- **Timing variations** - Test flows at different times
- **Network conditions** - Consider call quality impacts

## Files Overview

- **`studio-flow-example.json`** - Template flows for different scenarios
- **Flow library** - Collection of pre-built simulation flows
- **Documentation** - Detailed setup and configuration guides

This Studio-based approach provides the most realistic and controlled AMD testing environment, allowing you to perfect your configurations before deploying to production.