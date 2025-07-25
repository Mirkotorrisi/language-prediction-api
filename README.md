# Language Detection Model API

This application provides a simple model that predicts the language from a text

The app is exposed using `FastAPI`, with a single POST route available in the builtin `/docs`

- POST  `/identify-language`

    ***Body***:

        {
            text: "Text to identify"
        }

    ***Output***:

        {
            "language_code": "IT",
            "confidence": 0.98
        }