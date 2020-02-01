from datetime import timedelta, datetime, date
import random

from pets import db
from pets.models.animal import Animal, AnimalColor, AnimalKind, AnimalGender, AnimalSize
from pets.models.animal_breed import DogBreed, CatBreed
from pets.models.dog import Dog
from pets.models.cat import Cat
from pets.utils.consts import Consts
from pets.models.person import Gender, Role
from pets.models.employee import Employee
from pets.models.manager import Manager


class DataGenerator(object):

    def run(self):
        self.generate_animals()
        self.generate_adoption_requests()
        self.generate_employees()
        self.generate_manager()

    @staticmethod
    def _random_date(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)

    @staticmethod
    def _calc_textual_age(birth_date):
        age = '{0:.1f}'.format((datetime.today() - birth_date).days / 365)
        integer, decimal = age.split('.')
        age = integer if decimal == '0' else age
        return '{} year{} old'.format(age, 's' if float(age) > 1 else '')

    def _generate_common_animal_data(self, name, props):
        params = {}
        params["name"] = name.title()
        params["profile_image"] = "/static/img/adoption/{}.jpg".format(name.lower())
        params["gender"] = props.get("gender", random.choice((AnimalGender.Male, AnimalGender.Female)))

        params["size"] = props.get("size", random.choice(list(AnimalSize.__members__.values())))
        params["weight"] = props.get("weight", float("{}.{}".format(random.randint(3, 20), random.randint(0, 9))))

        params["color"] = props.get("color", random.choice(list(AnimalColor.__members__.values())))
        params["cage"] = props.get("cage", random.randint(1, 20))

        params["birth_date"] = self._random_date(datetime.strptime("2015-01-01", Consts.DATE_FORMAT),
                                              datetime.strptime("2020-01-01", Consts.DATE_FORMAT))
        params["arrival_date"] = self._random_date(params["birth_date"], datetime.now())

        params["fruitful"] = props.get("fruitful", random.choice((True, False)))
        params["is_trained"] = props.get("is_trained", random.choice((True, False)))
        params["friendly"] = props.get("friendly", random.choice((True, False)))

        params["adopted"] = props.get("adopted", random.choice((True, False)))

        return params

    def _generate_dog(self, name, props):
        params = self._generate_common_animal_data(name, props)
        params["kind"] = AnimalKind.Dog
        params["breed"] = random.choice([x.value for x in DogBreed.__members__.values()])
        params["chip"] = random.randrange(100000, 1000000)
        params["is_dangerous"] = random.choice((True, False))

        age = self._calc_textual_age(params["birth_date"])
        dog_details = [
            f'{name} ({age}) is a friendly dog, good with kids <br> and waiting for some love',
            f'{name} ({age}) is a scared dog who has been abandoned at a relatively late age '
            f'<br> Will fit in a home without children',
            f'{name} ({age}) is a very naughty and sociable, well-educated dog needs lots of warmth and love',
            f'{name} ({age}) is a quiet, calm dog but getting along with kids, waiting for someone to take him home',
        ]
        params["details"] = random.choice(dog_details)
        return Dog(params)

    def _generate_cat(self, name, props):
        params = self._generate_common_animal_data(name, props)
        params["kind"] = AnimalKind.Cat
        params["breed"] = random.choice([x.name for x in CatBreed.__members__.values()])
        params["is_playful"] = random.choice((True, False))
        params["is_hairy"] = random.choice((True, False))
        params["is_loud"] = random.choice((True, False))

        age = self._calc_textual_age(params["birth_date"])
        cat_details = [
            f'{name} ({age}) is a friendly cat, good with kids <br> and waiting for some love',
            f'{name} ({age}) is a cute, scared cat who has been through a lot in a very short life time '
            f'<br> will be handed over to a family without children',
            f'{name} ({age}) is a very naughty and sociable, well-educated cat needs lots of warmth and love',
            f'{name} ({age}) is a quiet, calm cat but getting along with kids, waiting a new home',
        ]
        params["details"] = random.choice(cat_details)
        return Cat(params)

    def generate_animals(self):
        dogs = ["belle", "black", "chucky", "goldy", "guy", "joe", "joy", "khaleesi", "levana", "lucky", "nela",
                "pinky", "ryko", "shandy", "simon", "toffee", "alice", "amigo", "bexter", "boba", "cola",
                "hetz", "jinji", "kiki", "kim", "laydy", "lori", "luke", "miles", "rada", "sangi", "simba", "sky",
                "styles", "tau", "tommy", "tyler", "viki"]
        cats = ["basya", "bosik", "joey", "oliver", "oscar", "felix", "lola", "gizmo"]
        chosen_properties = {
          "Belle": {
              "color": AnimalColor.Brown,
              "gender": AnimalGender.Female,
          }
        }
        animals = [self._generate_dog(dog_name, chosen_properties.get(dog_name, {})) for dog_name in dogs]
        animals.extend([self._generate_cat(cat_name, chosen_properties.get(cat_name, {})) for cat_name in cats])

        for animal in animals:
            db.session.add(animal)
            db.session.commit()

    def generate_adoption_requests(self):
        pass

    def _generate_person_data(self, names):
        data = [
            {
                "id": random.randrange(100000000, 999999999),
                "name": name,
                "gender": random.choice([Gender.Male, Gender.Female]),
                "role": Role.Employee,
                "birth_date": self._random_date(datetime.strptime("1980-01-01", Consts.DATE_FORMAT),
                                                datetime.strptime("2000-01-01", Consts.DATE_FORMAT)),
                "phone_number": "{}-{}".format(random.choice(["050", "052", "054"]),
                                               random.randrange(100000000, 999999999)),
                "email": "{}@{}.com".format(name, random.choice(["gmail", "outlook", "hotmail"]))
            } for name in names
        ]
        return data

    def _generate_employee_data(self, names):
        data = self._generate_person_data(names)
        for params in data:
            params["salary"] = random.randrange(1000, 10000)
            params["job_percentages"] = random.randrange(10, 100, 10)
            params["bank_account_details"] = "{}-0{}-{}".format(
                random.randrange(10, 99),
                random.randrange(10, 99),
                random.randrange(100000000, 999999999)
            )
            params["is_employed"] = random.choice([True, False])
        return data

    def _generate_manager_data(self, names):
        data = self._generate_employee_data(names)
        for params in data:
            params["password"] = "12345"
        return data

    def generate_employees(self):
        data = self._generate_employee_data(["Lior Choen", "Eden Levi", "Daniel Bachar", "Ariel Donay", "Mor Azrielant",
                                             "Nitzan Malol", "Shir Ben Yehuda", "Sharon Shivika", "Lean Granot", "Or Lavok",
                                             "Bar Nir", "Gal Biran", "Gili Moskovich", "Hadar Aloni", "Viki Zohar",])
                                             # "Zohar Argov", "Hen Moshe", "Tal Cohen", "Yuval Hamebolbal", "Yarden Moyal",
                                             # "Yam Ragoa", "Rotem Bar", "Meitar Kinor", "Miki Haim", "Noam Nesher"])
        for params in data:
            employee = Employee(params)
            db.session.add(employee)
            db.session.commit()

    def generate_manager(self):
        params = self._generate_manager_data(["Hilaria Bixenshpaner"])[0]
        hilaria = {
            "gender": Gender.Female,
            "id": "301271169",
            "is_employed": True,
            "email": "hilaria@gmail.com"
        }
        params.update(hilaria)

        manager = Manager(params)
        manager.set_password("12345")
        db.session.add(manager)
        db.session.commit()
