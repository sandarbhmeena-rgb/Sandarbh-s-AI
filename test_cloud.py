from cloud_engine import test_connection

success, result = test_connection()

if success:
    print("\nGEMINI CONNECTION SUCCESSFUL!")
    print(result)
else:
    print("\nGEMINI CONNECTION FAILED!")
    print(result)