class Loader:

    @staticmethod
    def load(file_name: str) -> list[str]:
        with open(file_name, "r") as f:
            result = f.readlines()
            return [line.strip('\n') for line in result]
