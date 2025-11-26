import enum

class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    BANNED = "banned"

class UserRole(enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"

class DATABASE(enum.Enum):
    ACCOUNT = "account"
    QUESTION = "question"
    ANSWER = "answer"
    REVIEW = "review"
    REPORT = "report"

class COLLECTION(enum.Enum):
    USER = "user"
    QUESTION = "question"
    ANSWER = "answer"
    REVIEW = "review"
    REPORT = "report"