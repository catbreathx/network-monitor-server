import base64


def get_body_from_email(email) -> str:
    base64_content = email.get_payload()[0].get_payload()
    base64_content = bytes(base64_content, "utf-8")
    result = base64.urlsafe_b64decode(base64_content).decode()

    return result
