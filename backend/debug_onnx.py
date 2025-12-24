try:
    import onnxruntime
    print("onnxruntime imported successfully")
    print(f"Version: {onnxruntime.__version__}")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
