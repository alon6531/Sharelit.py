import Client

if __name__ == "__main__":
    try:
        client = Client.Client()
    except Exception as e:
        print(f"Client failed to start: {e}")