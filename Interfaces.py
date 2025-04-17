

class Checkable():

    def check(self) -> bool:
        pass

class SelfFixing():

    def fix(self) -> None:
        pass

class EditorAdjusted():

    def no_edit(self) -> list[str]:
        return []

    def no_show(self) -> list[str]:
        return []