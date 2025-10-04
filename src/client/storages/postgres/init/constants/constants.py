from typing import ClassVar

from src.modules.activity.schemas import ActivityInit
from src.modules.building.schemas import BuildingCreate
from src.modules.organization.schemas import OrganizationInit


class BuildingInitCosts:
    BUILDINGS_FOR_INIT: ClassVar[list[BuildingCreate]] = [
        BuildingCreate(
            address="г. Москва, ул. Ленина 1", latitude=55.7558, longitude=37.6173
        ),
        BuildingCreate(
            address="г. Санкт-Петербург, пр. Невский 10",
            latitude=59.9343,
            longitude=30.3351,
        ),
        BuildingCreate(
            address="г. Новосибирск, ул. Красный проспект 20",
            latitude=55.0415,
            longitude=82.9346,
        ),
        BuildingCreate(
            address="г. Екатеринбург, ул. Малышева 50",
            latitude=56.8389,
            longitude=60.6057,
        ),
        BuildingCreate(
            address="г. Нижний Новгород, ул. Большая Покровская 15",
            latitude=56.3269,
            longitude=44.0075,
        ),
        BuildingCreate(
            address="г. Казань, Кремлёвская ул. 3", latitude=55.7903, longitude=49.1347
        ),
        BuildingCreate(
            address="г. Челябинск, пр. Ленина 70", latitude=55.1644, longitude=61.4368
        ),
        BuildingCreate(
            address="г. Омск, ул. Ленина 5", latitude=54.9924, longitude=73.3686
        ),
        BuildingCreate(
            address="г. Ростов-на-Дону, ул. Большая Садовая 40",
            latitude=47.2357,
            longitude=39.7015,
        ),
        BuildingCreate(
            address="г. Уфа, пр. Октября 25", latitude=54.7388, longitude=55.9721
        ),
    ]


class ActivityInitCosts:
    ACTIVITIES_FOR_INIT: ClassVar[list[ActivityInit]] = [
        ActivityInit(name="Еда", parent_sid=None, parent_name=None),
        ActivityInit(name="Мясная продукция", parent_sid=None, parent_name="Еда"),
        ActivityInit(
            name="Копчености", parent_sid=None, parent_name="Мясная продукция"
        ),
        ActivityInit(name="Молочная продукция", parent_sid=None, parent_name="Еда"),
        ActivityInit(name="Автомобили", parent_sid=None, parent_name=None),
        ActivityInit(name="Грузовые", parent_sid=None, parent_name="Автомобили"),
        ActivityInit(name="Легковые", parent_sid=None, parent_name="Автомобили"),
        ActivityInit(name="Запчасти", parent_sid=None, parent_name="Легковые"),
        ActivityInit(name="Аксессуары", parent_sid=None, parent_name="Легковые"),
        ActivityInit(name="Ремонт", parent_sid=None, parent_name=None),
    ]


class OrganizationInitCosts:
    ORGANIZATIONS_FOR_INIT: ClassVar[list[OrganizationInit]] = [
        OrganizationInit(
            name="ООО Ромашка",
            phones=["+7-495-123-45-67"],
            address="г. Москва, ул. Ленина 1",
            office="Офис 1",
            latitude=55.7558,
            longitude=37.6173,
            activity_name="Еда",
        ),
        OrganizationInit(
            name="АО Северная Звезда",
            phones=["+7-812-234-56-78", "+7-812-234-56-79"],
            address="г. Санкт-Петербург, пр. Невский 10",
            office="Офис 2",
            latitude=59.9343,
            longitude=30.3351,
            activity_name="Мясная продукция",
        ),
        OrganizationInit(
            name="ООО Сибирь Продукт",
            phones=[],
            address="г. Новосибирск, ул. Красный проспект 20",
            office="Офис 3",
            latitude=55.0415,
            longitude=82.9346,
            activity_name="Копчености",
        ),
        OrganizationInit(
            name="ЗАО Урал Лакто",
            phones=["+7-343-111-2222", "+7-343-333-4444", "+7-343-555-6666"],
            address="г. Екатеринбург, ул. Малышева 50",
            office="Офис 4",
            latitude=56.8389,
            longitude=60.6057,
            activity_name="Молочная продукция",
        ),
        OrganizationInit(
            name="ООО Нижегородский Автокомплекс",
            phones=["+7-831-777-88-99"],
            address="г. Нижний Новгород, ул. Большая Покровская 15",
            office="Офис 5",
            latitude=56.3269,
            longitude=44.0075,
            activity_name="Автомобили",
        ),
        OrganizationInit(
            name="АО Казань Трак",
            phones=["+7-843-123-45-67"],
            address="г. Казань, Кремлёвская ул. 3",
            office="Офис 6",
            latitude=55.7903,
            longitude=49.1347,
            activity_name="Грузовые",
        ),
        OrganizationInit(
            name="ООО ЧелябСтрой",
            phones=["+7-351-222-33-44"],
            address="г. Челябинск, пр. Ленина 70",
            office="Офис 7",
            latitude=55.1644,
            longitude=61.4368,
            activity_name="Легковые",
        ),
        OrganizationInit(
            name="ООО Омск Автоэксперт",
            phones=["+7-381-555-66-77", "+7-381-888-99-00"],
            address="г. Омск, ул. Ленина 5",
            office="Офис 8",
            latitude=54.9924,
            longitude=73.3686,
            activity_name="Запчасти",
        ),
        OrganizationInit(
            name="ЗАО Ростов Комплект",
            phones=["+7-863-111-2222"],
            address="г. Ростов-на-Дону, ул. Большая Садовая 40",
            office="Офис 9",
            latitude=47.2357,
            longitude=39.7015,
            activity_name="Аксессуары",
        ),
        OrganizationInit(
            name="ООО БашАвто Ремонт",
            phones=[
                "+7-347-123-4567",
                "+7-347-234-5678",
                "+7-347-345-6789",
                "+7-347-456-7890",
            ],
            address="г. Уфа, пр. Октября 25",
            office="Офис 10",
            latitude=54.7388,
            longitude=55.9721,
            activity_name="Ремонт",
        ),
    ]


class InitCosts:
    def __init__(self):
        self.Building = BuildingInitCosts()
        self.Activity = ActivityInitCosts()
        self.Organization = OrganizationInitCosts()
