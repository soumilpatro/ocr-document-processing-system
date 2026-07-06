from fastapi import HTTPException


class DuplicateDocumentException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=409,
            detail={
                "errorCode": "DUPLICATE_DOCUMENT",
                "message": "This document has already been processed."
            }
        )


class FileTooLargeException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=413,
            detail={
                "errorCode": "FILE_TOO_LARGE",
                "message": "Uploaded file exceeds maximum size."
            }
        )


class UnsupportedFileException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=400,
            detail={
                "errorCode": "UNSUPPORTED_FILE",
                "message": "Only PDF, JPG and PNG files are supported."
            }
        )


class NoTextExtractedException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=400,
            detail={
                "errorCode": "NO_TEXT_EXTRACTED",
                "message": "OCR could not extract any readable text."
            }
        )