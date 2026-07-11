def mask_name(name: str | None) -> str | None:
    if not name:
        return name

    words = name.split()

    masked = []

    for word in words:

        if len(word) <= 1:
            masked.append(word)

        elif len(word) == 2:
            masked.append(word[0] + "*")

        else:
            masked.append(
                word[0] + "*" * (len(word) - 2) + word[-1]
            )

    return " ".join(masked)


def mask_account_number(account_number: str | None) -> str | None:

    if not account_number:
        return account_number

    account_number = str(account_number)

    if len(account_number) <= 4:
        return "*" * len(account_number)

    return "*" * (len(account_number) - 4) + account_number[-4:]


def mask_ifsc(ifsc: str | None) -> str | None:

    if not ifsc:
        return ifsc

    if len(ifsc) <= 4:
        return "*" * len(ifsc)

    return ifsc[:4] + "*" * (len(ifsc) - 4)