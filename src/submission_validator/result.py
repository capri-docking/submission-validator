from dataclasses import dataclass


@dataclass
class CheckResult:
    passed: bool
    message: str | None = None

    def __bool__(self) -> bool:
        return self.passed
