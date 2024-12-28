from enum import Enum

class LLMEnums(Enum):
    OPENAI ="OPENAI"
    COHERE = "COHERE"

class OpenAIEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT="assistant"

class CoHereEnum(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT="CHATBOT"

    DOCUMENT="search_document"
    QUERy="search_query"

class DocumentTypeEnum(Enum):
    DOCUMENT="document"
    QUERY="query"