from cloud_engine import get_available_models

try:
    models = get_available_models()

    print("\nAvailable Gemini Flash models:")

    for model in models:
        print("-", model)

    if not models:
        print("No suitable Flash models found.")

except Exception as error:
    print("\nModel discovery failed:")
    print(type(error).__name__, error)