import sqlite3


class DbManager:
    def __init__(self):
        self.connect = sqlite3.connect('./db/weather_app_db.sqlite')
        self.cursor = self.connect.cursor()

    def commit(self) -> None:
        self.connect.commit()

    def add_to_favorites(self, city: str) -> bool:
        already_added = False

        for fav_city in self.get_deleted_cities():
            if city in fav_city:
                self.undelete_from_favorites(city)
                return False

        for fav_city in self.get_favorite_cities():
            if city in fav_city:
                already_added = True
                print('already added')
                break

        if not already_added:
            self.cursor.execute(
                "INSERT INTO favorite_cities(city_name) VALUES(?)", (city.lower().strip(), )
            )

        self.commit()

        return already_added

    def get_city_id(self, city: str):
        result = self.cursor.execute(
            "SELECT id FROM favorite_cities WHERE city_name=?", (city.lower().strip(), )
        ).fetchone()

        return result[0] if result else result

    def delete_from_favorites(self, city: str) -> None:
        city_id = self.get_city_id(city)

        self.cursor.execute(
            "UPDATE favorite_cities SET is_deleted=1 WHERE id=?", (city_id, )
        )

        self.commit()

    def undelete_from_favorites(self, city: str) -> None:
        city_id = self.get_city_id(city)

        self.cursor.execute(
            "UPDATE favorite_cities SET is_deleted=0 WHERE id=?", (city_id, )
        )

        self.commit()

    def set_default(self, city: str) -> None:
        """Weather data of the default city is shown right when the app is opened"""
        self.cursor.execute(
            "UPDATE favorite_cities SET is_default=0 WHERE is_default=1"
        )  # reset default city

        city_id = self.get_city_id(city)

        self.cursor.execute(
            "UPDATE favorite_cities SET is_default=1 WHERE id=?", (city_id, )
        )

        self.commit()

    def get_favorite_cities(self) -> list:
        return self.cursor.execute(
            "SELECT city_name FROM favorite_cities WHERE is_deleted=0 ORDER BY is_deleted DESC"
        ).fetchall()

    def get_deleted_cities(self) -> list:
        return self.cursor.execute(
            "SELECT city_name FROM favorite_cities WHERE is_deleted=1"
        ).fetchall()

    def get_default_favorite_city(self) -> str:
        result = self.cursor.execute(
            "SELECT city_name FROM favorite_cities WHERE is_deleted=0 AND is_default=1"
        ).fetchone()

        return result[0] if result else result

    def add_all_parameters(self, parameters: list) -> None:
        """This function will be used only once after the DB is created
         to initialize all the parameters"""

        already_added = bool(
            self.cursor.execute(
                "SELECT * FROM settings"
            ).fetchall()
        )

        if not already_added:
            for parameter in parameters:
                self.cursor.execute(
                    "INSERT INTO settings(parameter) VALUES(?)", (parameter, )
                )

        self.commit()

    def get_parameter_id(self, parameter: str):
        return self.cursor.execute(
            "SELECT id FROM settings WHERE parameter=?", (parameter, )
        ).fetchone()[0]

    def select_parameter(self, parameter: str) -> None:
        parameter_id = self.get_parameter_id(parameter)

        self.cursor.execute(
            "UPDATE settings SET is_selected=1 WHERE id=?", (parameter_id,)
        )

        self.commit()

    def unselect_parameter(self, parameter: str) -> None:
        parameter_id = self.get_parameter_id(parameter)

        self.cursor.execute(
            "UPDATE settings SET is_selected=0 WHERE id=?", (parameter_id, )
        )

        self.commit()

    def get_selected_parameters(self) -> list:
        return self.cursor.execute(
            "SELECT parameter FROM settings WHERE is_selected=1"
        ).fetchall()

    def get_unselected_parameters(self) -> list:
        return self.cursor.execute(
            "SELECT parameter FROM settings WHERE is_selected=0"
        ).fetchall()

    def close(self):
        self.connect.close()
