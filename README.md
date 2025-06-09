# Twilio Voice API – Answering Machine Detection (AMD) Demo

This project demonstrates how to use Twilio's Voice API to make outbound calls with Answering Machine Detection (AMD) and fine-tune its parameters for different detection scenarios.

## Requirements

- A Twilio account with Voice capabilities
- Two Twilio phone numbers (one for outbound calls, one for simulating call responses - You can also use your own phone number for testing)
- Python 3.7+ with the following libraries installed:

```bash
pip install twilio flask python-dotenv
```

- A `.env` file configured with:

```env
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+15551234567
INCOMING_PHONE_NUMBER=+15557654321
```

## Project Flow

1. A Flask server is launched to receive Twilio webhook events.
2. A series of AMD use cases are defined with specific configurations.
3. Calls are executed automatically or interactively using those parameters.
4. Call results are monitored and analyzed using Twilio Call SIDs.

## Optional AMD Parameters

Twilio provides four optional parameters to adjust the performance of the AMD engine. Below are the allowed values and descriptions for each:

| Parameter Name                     | Allowed Values     | Default Value |
|----------------------------------|---------------------|----------------|
| MachineDetectionTimeout           | Between 3 and 59    | 30             |
| MachineDetectionSpeechThreshold   | Between 1000 and 6000 | 2400         |
| MachineDetectionSpeechEndThreshold| Between 500 and 5000  | 1200         |
| MachineDetectionSilenceTimeout    | Between 2000 and 10000 | 5000        |

### MachineDetectionTimeout
The number of seconds Twilio should spend attempting to detect an answering machine before timing out. If this time is exceeded, the `AnsweredBy` field will be set to `unknown`.

- Increasing this gives the engine more time to detect long greetings.
- Decreasing it favors quicker responses but may increase `unknown` results.

### MachineDetectionSpeechThreshold
Defines the minimum duration (in milliseconds) of speech activity to be considered a machine.

- Increase to reduce false machine detection on long human greetings.
- Decrease to improve detection of short voicemail greetings.

### MachineDetectionSpeechEndThreshold
The number of milliseconds of silence following speech that indicates the speech segment is over.

- Increase to treat longer silences within greetings as part of the same message.
- Decrease for faster detection of human responses.

### MachineDetectionSilenceTimeout
The number of milliseconds of initial silence after which Twilio will return `AnsweredBy=unknown`.

- Increase to allow more time for initial audio.
- Decrease to fail fast when silence is detected.

## Running the Project

1. Launch the Flask webhook server.
2. Execute test calls using the defined AMD scenarios.
3. Monitor call status using `monitor_call_status(call_sid)`.
4. Use `analyze_recent_calls()` to gather statistics from recent calls.

## Notes

- AMD detection may vary depending on how users or voicemail systems respond.
- Always test with real-world examples to find optimal parameter settings.

## References

- [Twilio AMD Documentation](https://www.twilio.com/docs/voice/answering-machine-detection)
- [Twilio Voice API](https://www.twilio.com/docs/voice/api)