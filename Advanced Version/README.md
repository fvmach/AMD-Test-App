# Advanced AMD Testing Suite

This advanced version provides automated batch testing of multiple AMD configurations with comprehensive logging and analysis capabilities.

## What This Does

- **Batch Tests** all 6 pre-configured AMD scenarios automatically
- **Real-time Monitoring** of call progress and AMD results
- **Comprehensive Logging** via webhook server with detailed AMD analysis
- **Automated ngrok Setup** for seamless webhook exposure
- **Interactive Menu** for testing individual configurations

## Quick Start

### 1. Setup Environment

```bash
# From the Advanced Version directory
cd "Advanced Version"

# Install dependencies (if not already done)
pip install twilio flask python-dotenv pyngrok

# Ensure your .env file is configured (in parent directory)
```

### 2. Start the Notebook

```bash
jupyter notebook amd_test_notebook.ipynb
```

### 3. Run Batch Test

Execute the cells in order, then use:

```python
# Test all configurations automatically
batch_test_all_configurations()
```

## Pre-configured AMD Scenarios

| Configuration | Timeout | Speech Threshold | Use Case |
|---------------|---------|------------------|----------|
| `residential_fast` | 15s | 1800ms | Personal phones with short greetings |
| `business_standard` | 20s | 2400ms | Business phones with longer greetings |
| `voicemail_drop` | 45s | 3000ms | Message delivery (DetectMessageEnd) |
| `conservative` | 25s | 2400ms | High accuracy, fewer unknowns |
| `aggressive` | 8s | 1500ms | Fast detection, more unknowns |
| `custom_tuning` | 20s | 2000ms | Template for custom parameters |

## Key Features

### Automated Batch Testing

```python
# Tests all 6 configurations in sequence
batch_test_all_configurations()

# Results in:
# - 6 simultaneous calls with different AMD settings
# - Real-time webhook logging
# - Comprehensive result summary
```

### Custom Configuration Creation

```python
# Create custom AMD parameters
config_key = create_custom_config(
    name="My Custom Test",
    description="Optimized for my use case",
    timeout=18,
    speech_threshold=2200,
    speech_end_threshold=1100,
    silence_timeout=3500
)

# Test the custom configuration
make_amd_call(config_key)
```

### Real-time Call Monitoring

```python
# Monitor call progress and AMD results
monitor_call_with_amd_results('CAxxxxxxxxxx', max_wait_time=60)
```

## 📡 Webhook Server Features

The advanced server provides:

- **Detailed AMD Analysis** with result interpretation
- **Categorized Logging** (Call Info, AMD Results, Geographic Data)
- **Real-time Status Updates** with emoji indicators
- **Test Scenario Context** explaining the setup

### AMD Result Interpretation

```
 Human detected - real person answered
 Machine detected - answering machine/voicemail  
 Fax machine detected
 Unknown - could not determine human vs machine
```

## Interactive Menu

The notebook includes a comprehensive menu system:

```
1. Interactive AMD Testing
2. Batch Test All Configurations  
3. Quick Test Single Configuration
4. Make AMD Call
5. Fetch Call AMD Results
6. Monitor Call with AMD Results
0. Exit
```

## Batch Test Process

1. **Configuration Display** - Shows all 6 test scenarios
2. **Confirmation Prompt** - Confirms before making multiple calls
3. **Sequential Execution** - Makes calls with 1-second intervals
4. **Real-time Logging** - Each call logs to webhook immediately
5. **Summary Report** - Shows all Call SIDs and results

### Sample Batch Output

```
[1/6] Testing: Residential/Mobile - Fast Detection
SUCCESS - Call SID: CA2d5c16203f0b0587a6e1f91d79a8ab05

[2/6] Testing: Business - Standard Detection  
SUCCESS - Call SID: CAe6ccecabb40a66ab9e7bfd8222e627bb

...

BATCH TEST COMPLETED
Successful calls: 6
Failed calls: 0
```

## Advanced Analysis

### Call Result Fetching

```python
# Get detailed AMD results for any call
fetch_call_amd_results('CAxxxxxxxxxx')

# Shows:
# - Call status and duration
# - AMD detection results
# - All AMD parameters used
# - Timing information
```

### Recent Calls Analysis

```python
# View recent calls with AMD results
calls = client.calls.list(limit=10)
# Displays formatted table with SIDs, status, and results
```

## Configuration Customization

### Modifying Existing Configurations

```python
# Adjust existing configuration
AMD_CONFIGURATIONS['residential_fast']['params']['machine_detection_timeout'] = 12

# Test the modified configuration
make_amd_call('residential_fast')
```

### Adding New Scenarios

```python
# Add a new test scenario
AMD_CONFIGURATIONS['my_scenario'] = {
    "name": "My Custom Scenario",
    "description": "Tailored for my specific use case",
    "params": {
        "machine_detection": "Enable",
        "machine_detection_timeout": 16,
        # ... other parameters
    }
}
```

## Understanding Results

### Webhook Data Categories

1. **Call Information** - SID, status, numbers, duration
2. **AMD Results** - Detection result, duration, thresholds
3. **Callback Information** - Source, sequence, timestamps
4. **Geographic Information** - Location data for numbers

### Performance Metrics

- **Detection Speed** - How quickly AMD determined the result
- **Accuracy Rate** - Percentage of correct human/machine detection
- **Unknown Rate** - Percentage of indeterminate results
- **Configuration Comparison** - Side-by-side performance analysis

## Best Practices

1. **Test with Real Scenarios** - Use actual phone numbers and voicemails
2. **Analyze Patterns** - Look for consistent results across configurations
3. **Adjust Gradually** - Make small parameter changes and test
4. **Monitor Webhooks** - Watch real-time logs for insights
5. **Document Results** - Keep track of what works for your use case

## Troubleshooting

### No Webhook Callbacks

```bash
# Check ngrok status
curl https://your-domain.ngrok.io/status

# Verify webhook URL in configuration
echo $WEBHOOK_BASE_URL
```

### Calls Not Connecting

```python
# Verify phone numbers
print(f"From: {FROM_NUMBER}")
print(f"To: {TO_NUMBER}")

# Check Twilio account balance and phone number capabilities
```

### AMD Always Returns 'Unknown'

- Increase `machine_detection_timeout`
- Lower `machine_detection_speech_threshold`
- Test with known human/machine scenarios

## Files Overview

- **`amd_test_notebook.ipynb`** - Main testing interface with all functions
- **`server.py`** - Advanced webhook server with detailed logging
- **Configuration sections** - Pre-built AMD scenarios for different use cases

This advanced version is perfect for comprehensive AMD testing and fine-tuning across multiple scenarios simultaneously.