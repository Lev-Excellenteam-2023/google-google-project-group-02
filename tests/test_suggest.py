from data_class.file_data import FileData
import suggest_engine.suggest as suggest


def test_find_match() -> None:
    my_files = FileData("C:\\Users\\Ruben\\Desktop\\Excellenteam\\google "
                        "autocomplete\\Archive\\python-3.8.4-docs-text\\installing")

    # suggest.find_match(["test"], my_files)

