# Twilio Voice API – Answering Machine Detection (AMD) Demo

A comprehensive demonstration project showcasing Twilio's Answering Machine Detection (AMD) capabilities with multiple testing scenarios, configurations, and Studio flow simulations.

## Project Overview

This project provides three different approaches to test and fine-tune Twilio's AMD functionality:

1. **Advanced Version** - Automated batch testing with multiple AMD configurations
2. **Manual Setup** - Interactive testing with step-by-step control
3. **Answering Machine Simulator** - Studio flow examples for simulating different scenarios

## Repository Structure

```
twilio-amd-demo/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── Advanced Version/                   # Automated AMD testing suite
│   ├── README.md                      # Advanced setup guide
│   ├── amd_test_notebook.ipynb        # Jupyter notebook with batch testing
│   └── server.py                      # Flask webhook server
├── Manual Setup/                       # Interactive AMD testing
│   ├── README.md                      # Manual setup guide
│   ├── amd_demo_notebook.ipynb        # Step-by-step testing notebook
│   └── server.py                      # Basic webhook server
└── Answering Machine Simulator/        # Studio flow examples
    ├── README.md                      # Studio setup guide
    └── studio-flow-example.json       # Example flows for testing
```

## Quick Start

### Prerequisites

- **Twilio Account** with Voice API capabilities
- **Two Twilio Phone Numbers** (caller and callee. Callee can be replaced by another PSTN phone number)
- **Python 3.7+** with pip
- **ngrok** (for webhook exposure)

### Basic Setup

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd twilio-amd-demo
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Twilio credentials
   ```

3. **Set up ngrok:**
   ```bash
   ngrok http 5000 --domain=your-domain.ngrok.io
   ```

4. **Choose your testing approach:**
   - **Quick Start**: Use [Advanced Version](Advanced%20Version/README.md) for automated batch testing
   - **Learn Step-by-Step**: Use [Manual Setup](Manual%20Setup/README.md) for interactive testing
   - **Simulate Scenarios**: Use [Answering Machine Simulator](Answering%20Machine%20Simulator/README.md) with Studio flows

## Environment Configuration

Create a `.env` file with your Twilio credentials:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15551234567
INCOMING_PHONE_NUMBER=+15557654321
NGROK_DOMAIN=your-domain.ngrok.io
```

## AMD Testing Scenarios

This project includes pre-configured AMD scenarios:

| Configuration | Use Case | Timeout | Speech Threshold | Best For |
|---------------|----------|---------|------------------|----------|
| **Residential Fast** | Personal phones | 15s | 1800ms | Mobile/home phones |
| **Business Standard** | Business lines | 20s | 2400ms | Corporate systems |
| **Voicemail Drop** | Message delivery | 45s | 3000ms | Voicemail detection |
| **Conservative** | High accuracy | 25s | 2400ms | Fewer false positives |
| **Aggressive** | Fast response | 8s | 1500ms | Quick decisions |
| **Custom Tuning** | Fine-tuning | Configurable | Configurable | Parameter optimization |

## Documentation

### Detailed Guides

- **[Advanced Version Guide](Advanced%20Version/README.md)** - Automated batch testing with 6 pre-configured scenarios
- **[Manual Setup Guide](Manual%20Setup/README.md)** - Interactive testing with detailed explanations
- **[Studio Simulator Guide](Answering%20Machine%20Simulator/README.md)** - Creating realistic test scenarios

### AMD Parameter Reference

| Parameter | Range | Default | Purpose |
|-----------|--------|---------|---------|
| `MachineDetectionTimeout` | 3-59s | 30s | Max detection time |
| `MachineDetectionSpeechThreshold` | 1000-6000ms | 2400ms | Min speech duration |
| `MachineDetectionSpeechEndThreshold` | 500-5000ms | 1200ms | Silence after speech |
| `MachineDetectionSilenceTimeout` | 2000-10000ms | 5000ms | Initial silence limit |

## Usage Examples

### Quick Batch Test (Advanced Version)
```python
# Run all 6 AMD configurations automatically
batch_test_all_configurations()
```

### Single Configuration Test
```python
# Test a specific AMD scenario
make_amd_call('residential_fast')
```

### Custom Configuration
```python
# Create and test custom parameters
config = create_custom_config(
    name="My Custom AMD",
    timeout=15,
    speech_threshold=2000
)
```

### Monitor Results
```python
# Track call progress and AMD results
monitor_call_with_amd_results('CAxxxxxxxxxx')
```

## Understanding AMD Results

| Result | Meaning | Action |
|--------|---------|--------|
| `human` | Person answered | Continue conversation |
| `machine_start` | Voicemail beginning | Wait for beep |
| `machine_end_beep` | Beep detected | Leave message |
| `machine_end_silence` | Voicemail ended | Leave message |
| `fax` | Fax machine | Hang up |
| `unknown` | Unclear result | Use fallback logic |

## Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Your Script   │───▶│ Twilio Voice │───▶│  Target Phone   │
│  (AMD Enabled)  │    │     API      │    │   (Test Dest)   │
└─────────────────┘    └──────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────┐
│ Flask Webhook   │◀───│ AMD Results  │
│    Server       │    │   Callback   │
└─────────────────┘    └──────────────┘
```

## Troubleshooting

### Common Issues

1. **No AMD callbacks received**
   - Check ngrok is running and accessible
   - Verify webhook URL in configuration
   - Ensure phone numbers are correct

2. **Always getting 'unknown' results**
   - Increase `machine_detection_timeout`
   - Adjust speech thresholds
   - Check target phone behavior

3. **Webhook server not accessible**
   - Confirm ngrok domain matches `.env`
   - Test webhook URL manually
   - Check firewall settings

### Debug Tips

- Use the webhook server logs to see real-time AMD data
- Test with known scenarios (your own voicemail)
- Monitor call objects for AMD attributes
- Compare different configurations side-by-side

## Additional Resources

- [Twilio AMD Documentation](https://www.twilio.com/docs/voice/answering-machine-detection)
- [Twilio Voice API Reference](https://www.twilio.com/docs/voice/api)
- [TwiML Voice Reference](https://www.twilio.com/docs/voice/twiml)
- [Twilio Studio Documentation](https://www.twilio.com/docs/studio)

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is provided as-is for educational and testing purposes. Please ensure compliance with Twilio's terms of service and applicable regulations when using AMD for production calls.

---

**Need Help?** Check the specific README files in each subdirectory for detailed setup instructions and examples.