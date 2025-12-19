import pytest

from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()


    # 1) Добавление книги: валидное имя и затем отсутствие жанра
    def test_add_new_book_valid_and_no_genre_after_add(self):
        c = BooksCollector()
        c.add_new_book("БезЖанра")
        assert "БезЖанра" in c.get_books_genre()
        assert c.get_books_genre()["БезЖанра"] == ""

    # 2) Проверка, что книги с возрастным рейтингом не попадают в список для детей
    def test_books_with_age_rating_not_in_children_list(self):
        c = BooksCollector()
        c.add_new_book("КнигаСВозрастнымРейтингом")
        c.set_book_genre("КнигаСВозрастнымРейтингом", "Ужасы")  # возрастной рейтинг присутствует в жанрах
        children = c.get_books_for_children()
        assert "КнигаСВозрастнымРейтингом" not in children

    # 3) Добавление новой книги и проверка, что жанр пустой по умолчанию
    def test_add_book_and_check_no_genre_initially(self):
        c = BooksCollector()
        c.add_new_book("НовинкаБезЖанра")
        assert c.get_book_genre("НовинкаБезЖанра") == ""
        assert "НовинкаБезЖанра" in c.get_books_genre()

    # 4) Установка валидных жанров для партий книг (параметризовано)
    @pytest.mark.parametrize("name,genre", [
        ("Neuromancer", "Фантастика"),
        ("It", "Ужасы"),
    ])
    def test_set_book_genre_valid(self, name, genre):
        self.add_new_book(name)
        self.set_book_genre(name, genre)
        assert self.get_book_genre(name) == genre

    # 5) Неправильные случаи для жанров: несуществующая книга и неверный жанр
    def test_set_book_genre_invalid_book_and_genre(self):
        c = BooksCollector()
        c.set_book_genre("NonExistent", "Фантастика")
        assert c.get_book_genre("NonExistent") is None

        c.add_new_book("I, Robot")
        c.set_book_genre("I, Robot", "Научная фантастика")
        assert c.get_book_genre("I, Robot") == ""

    # 6) Получение списка книг по конкретному жанру (параметризовано)
    @pytest.mark.parametrize("genre, expected", [
        ("Фантастика", ["Book1"]),
        ("Ужасы", ["Book2"]),
    ])
    def test_get_books_with_specific_genre(self, expected, collector, genre=None):
        c = collector
        c.add_new_book("Book1")
        c.add_new_book("Book2")
        c.add_new_book("Book3")
        if genre == "Фантастика":
            c.set_book_genre("Book1", "Фантастика")
            c.set_book_genre("Book2", "Ужасы")
            c.set_book_genre("Book3", "Детективы")
        else:
            c.set_book_genre("Book2", "Ужасы")

        books = c.get_books_with_specific_genre(genre)
        assert books == expected

    # 7) Получение списка книг по неверному/несуществующему жанру
    def test_get_books_with_specific_genre_invalid(self):
        c = BooksCollector()
        c.add_new_book("BookX")
        c.set_book_genre("BookX", "Фантастика")
        assert c.get_books_with_specific_genre("Мультфильмы") == []

    # 8) Проверка списка жанров текущего состояния (сниппет)
    def test_get_books_genre_snapshot(self):
        c = BooksCollector()
        c.add_new_book("Alpha")
        c.set_book_genre("Alpha", "Комедии")
        snapshot = c.get_books_genre()
        assert snapshot == {"Alpha": "Комедии"}

    # 9) Проверка списка детей под условия: Kid1 допустим, Kid2 возрастное, Adult1 взрослый
    def test_get_books_for_children(self):
        c = BooksCollector()
        c.add_new_book("Kid1")
        c.add_new_book("Kid2")
        c.add_new_book("Adult1")

        c.set_book_genre("Kid1", "Комедии")  # допустим для детей
        c.set_book_genre("Kid2", "Ужасы")  # ограничение по возрасту
        c.set_book_genre("Adult1", "Фантастика")

        children = c.get_books_for_children()
        assert "Kid1" in children
        assert "Kid2" not in children
        assert "Adult1" in children

    # 10) Работа со Избранным: добавление, дубликаты, удаление, единичные тесты
    @pytest.mark.parametrize("name", ["FavoriteBook", "NiceBook"])
    def test_add_book_in_favorites_valid(self, name):
        c = self
        c.add_new_book(name)
        c.add_book_in_favorites(name)
        assert name in c.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate_and_invalid(self):
        c = BooksCollector()
        c.add_new_book("NiceBook")
        c.add_book_in_favorites("NiceBook")
        c.add_book_in_favorites("NiceBook")  # дубликат не добавится
        assert c.get_list_of_favorites_books().count("NiceBook") == 1

        c.add_book_in_favorites("NonExist")
        assert "NonExist" not in c.get_list_of_favorites_books()

    def test_delete_book_from_favorites_and_empty(self):
        c = BooksCollector()
        c.add_new_book("ToRemove")
        c.add_book_in_favorites("ToRemove")
        c.delete_book_from_favorites("ToRemove")
        assert c.get_list_of_favorites_books() == []

    def test_full_workflow_minimal(self):
        c = BooksCollector()
        c.add_new_book("The Hobbit")
        c.add_new_book("It")
        c.set_book_genre("The Hobbit", "Комедии")
        c.set_book_genre("It", "Ужасы")
        c.add_book_in_favorites("The Hobbit")
        c.add_book_in_favorites("It")

        assert c.get_book_genre("The Hobbit") == "Комедии"
        assert set(c.get_list_of_favorites_books()) == {"The Hobbit", "It"}

        c.delete_book_from_favorites("It")
        assert c.get_list_of_favorites_books() == ["The Hobbit"]

    def add_new_book(self, name):
        pass

    def set_book_genre(self, name, genre):
        pass

    def get_book_genre(self, name):
        pass

    def add_book_in_favorites(self, name):
        pass

    def get_list_of_favorites_books(self):
        pass

