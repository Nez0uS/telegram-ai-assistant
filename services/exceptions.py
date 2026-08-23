class AIServiceError(Exception):
    pass


class AIConnectionError(AIServiceError):
    pass


class AIRateLimitError(AIServiceError):
    pass


class AIProviderError(AIServiceError):
    pass
