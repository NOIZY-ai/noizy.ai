import os
try:
    path = "/Volumes/JOE/NKI/_TEST_CREATED_BY_PYTHON"
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "success.txt"), "w") as f:
        f.write("It worked")
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
