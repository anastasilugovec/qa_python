import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

class TestBooksCollector:

    @pytest.mark.parametrize("name", ["Some Book", "Another Book"])
    def test_add_new_book_adds_books(self, collector, name):
        collector.add_new_book(name)
        # Проверяем, что книга добавилась в список
        books_genre = collector.get_books_genre()
        assert name in books_genre

    # 1) Добавление книги: валидное имя и затем отсутствие жанра
    def test_add_new_book_valid_and_no_genre_after_add(self, collector):
        collector.add_new_book("БезЖанра")
        books_genre = collector.get_books_genre()
        assert "БезЖанра" in books_genre
        assert collector.get_book_genre("БезЖанра") == ""

    # 2) Проверка, что книги с возрастным рейтингом не попадают в список для детей
    def test_books_with_age_rating_not_in_children_list(self, collector):
        name = "КнигаСВозрастнымРейтингом"
        collector.add_new_book(name)
        collector.set_book_genre(name, "Ужасы")  # допустим, жанр не для детей
        children = collector.get_books_for_children()
        assert name not in children

    # 3) Добавление новой книги и проверка, что жанр пустой по умолчанию
    def test_add_book_and_check_no_genre_initially(self, collector):
        collector.add_new_book("НовинкаБезЖанра")
        assert collector.get_book_genre("НовинкаБезЖанра") == ""
        assert "НовинкаБезЖанра" in collector.get_books_genre()

    # 4) Установка валидных жанров для партий книг (параметризовано)
    @pytest.mark.parametrize("name,genre", [
        ("Neuromancer", "Фантастика"),
        ("It", "Ужасы"),
    ])
    def test_set_book_genre_valid(self, collector, name, genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == genre

    # 5) Неправильные случаи для жанров: несуществующая книга и неверный жанр
    def test_set_book_genre_invalid_book_and_genre(self, collector):
        collector.set_book_genre("NonExistent", "Фантастика")
        assert collector.get_book_genre("NonExistent") is None

        collector.add_new_book("I, Robot")
        collector.set_book_genre("I, Robot", "Научная фантастика")
        assert collector.get_book_genre("I, Robot") == ""

    # 6) Получение списка книг по конкретному жанру (параметризовано)
    @pytest.mark.parametrize("genre, expected", [
        ("Фантастика", ["Book1"]),
        ("Ужасы", ["Book2"]),
    ])
    def test_get_books_with_specific_genre(self, collector, genre, expected):
        # подготовим книги и установим жанры
        collector.add_new_book("Book1")
        collector.set_book_genre("Book1", "Фантастика")
        collector.add_new_book("Book2")
        collector.set_book_genre("Book2", "Ужасы")
        collector.add_new_book("Book3")
        # для каждого жанра устанавливаем только нужную книгу
        if genre == "Фантастика":
            # Book3 не меняем, оставляем без жанра или в другом жанре
            pass
        elif genre == "Ужасы":
            # Book3 не меняем
            pass
        # вызываем функцию
        books = collector.get_books_with_specific_genre(genre)
        assert books == expected
    # 8) Проверка списка жанров текущего состояния
    def test_get_books_genre_snapshot(self, collector):
        collector.add_new_book("Alpha")
        collector.set_book_genre("Alpha", "Комедии")
        snapshot = collector.get_books_genre()
        assert snapshot == {"Alpha": "Комедии"}

    # 9) Проверка списка детей
    def test_get_books_for_children(self, collector):
        collector.add_new_book("Kid1")
        collector.add_new_book("Kid2")
        collector.add_new_book("Adult1")

        collector.set_book_genre("Kid1", "Комедии")  # допустим для детей
        collector.set_book_genre("Kid2", "Ужасы")  # ограничение по возрасту
        collector.set_book_genre("Adult1", "Фантастика")

        children = collector.get_books_for_children()
        assert "Kid1" in children
        assert "Kid2" not in children
        assert "Adult1" in children

    # 10) Работа со Избранным: добавление, дубликаты, удаление, единичные тесты
    @pytest.mark.parametrize("name", ["FavoriteBook", "NiceBook"])
    def test_add_book_in_favorites_valid(self, collector, name):
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        assert name in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate_and_invalid(self, collector):
        collector.add_new_book("NiceBook")
        collector.add_book_in_favorites("NiceBook")
        collector.add_book_in_favorites("NiceBook")  # дубликат не добавится
        assert collector.get_list_of_favorites_books().count("NiceBook") == 1

        collector.add_book_in_favorites("NonExist")
        assert "NonExist" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_and_empty(self, collector):
        collector.add_new_book("ToRemove")
        collector.add_book_in_favorites("ToRemove")
        collector.delete_book_from_favorites("ToRemove")
        assert collector.get_list_of_favorites_books() == []

    def test_full_workflow_minimal(self, collector):
        collector.add_new_book("The Hobbit")
        collector.add_new_book("It")
        collector.set_book_genre("The Hobbit", "Комедии")
        collector.set_book_genre("It", "Ужасы")
        collector.add_book_in_favorites("The Hobbit")
        collector.add_book_in_favorites("It")

        assert collector.get_book_genre("The Hobbit") == "Комедии"
        assert set(collector.get_list_of_favorites_books()) == {"The Hobbit", "It"}

        collector.delete_book_from_favorites("It")
        assert collector.get_list_of_favorites_books() == ["The Hobbit"]