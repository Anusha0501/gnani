def send_notification(customer_name: str, message: str) -> None:
    # Mock – in real life you'd call email/SMS API
    print(f"[NOTIFICATION to {customer_name}] {message}")
