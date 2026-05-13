from app import app, db, bcrypt
from models import Product, Brand, User, CartItem, Favorite, Order
import json

def create_admin():
    """Создание администратора"""
    admin = User.query.filter_by(email='Admin@mail.ru').first()
    if not admin:
        admin = User(
            username='Admin',
            email='Admin@mail.ru',
            password=bcrypt.generate_password_hash('Nikiw01908923').decode('utf-8'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Администратор успешно создан!")
    else:
        admin.is_admin = True
        db.session.commit()
        print("ℹ️ Администратор уже существует")

def seed():
    with app.app_context():
        print("📦 Удаление старых таблиц...")
        # Удаляем все старые таблицы
        db.drop_all()
        db.create_all()
        print("✅ Новые таблицы созданы!")
        
        print("🗑️ Очистка данных...")
        # Очищаем все данные
        try:
            db.session.query(CartItem).delete()
            db.session.query(Favorite).delete()
            db.session.query(Order).delete()
            db.session.query(Product).delete()
            db.session.query(Brand).delete()
            db.session.commit()
        except:
            db.session.rollback()

        # Товары с характеристиками и реальными картинками
        products_data = [
            # Смартфоны (10 товаров)
            {
                'name': 'Samsung Galaxy S24 Ultra', 'category': 'Смартфоны', 'brand': 'Samsung',
                'price': 129990, 'old_price': 139990, 'rating': 4.9, 'stock': 25,
                'image_url': 'https://images.samsung.com/ru/smartphones/galaxy-s24-ultra/images/galaxy-s24-ultra-highlights-color-titanium-gray.jpg',
                'description': 'Флагманский смартфон Samsung Galaxy S24 Ultra с инновационным титановым корпусом, процессором Snapdragon 8 Gen 3 и камерой 200 МП.',
                'specs': {'Экран': '6.8" Dynamic AMOLED 2X, 120Hz', 'Процессор': 'Snapdragon 8 Gen 3', 'Память': '12/512 ГБ', 'Камера': '200+50+12+10 МП', 'Аккумулятор': '5000 мАч', 'ОС': 'Android 14'}
            },
            {
                'name': 'iPhone 15 Pro Max', 'category': 'Смартфоны', 'brand': 'Apple',
                'price': 149990, 'old_price': 159990, 'rating': 4.8, 'stock': 15,
                'image_url': 'https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/iphone-15-pro-max-natural-titanium-select',
                'description': 'iPhone 15 Pro Max с чипом A17 Pro, титановым корпусом и профессиональной системой камер.',
                'specs': {'Экран': '6.7" Super Retina XDR, 120Hz', 'Процессор': 'A17 Pro', 'Память': '8/256 ГБ', 'Камера': '48+12+12 МП', 'Аккумулятор': '4422 мАч', 'ОС': 'iOS 17'}
            },
            {
                'name': 'Xiaomi 14 Pro', 'category': 'Смартфоны', 'brand': 'Xiaomi',
                'price': 79990, 'old_price': 89990, 'rating': 4.7, 'stock': 30,
                'image_url': 'https://i01.appmifile.com/webfile/globalimg/products/pc/xiaomi-14-pro/specs.png',
                'description': 'Мощный флагман от Xiaomi с процессором Snapdragon 8 Gen 3 и камерой Leica.',
                'specs': {'Экран': '6.73" AMOLED, 120Hz', 'Процессор': 'Snapdragon 8 Gen 3', 'Память': '12/256 ГБ', 'Камера': '50+50+50 МП Leica', 'Аккумулятор': '4880 мАч', 'ОС': 'Android 14, HyperOS'}
            },
            {
                'name': 'Google Pixel 8 Pro', 'category': 'Смартфоны', 'brand': 'Google',
                'price': 69990, 'rating': 4.6, 'stock': 20,
                'image_url': 'https://lh3.googleusercontent.com/pixel-8-pro-bay-1.png',
                'description': 'Смартфон Google Pixel 8 Pro с чистым Android и передовыми AI-функциями камеры.',
                'specs': {'Экран': '6.7" LTPO OLED, 120Hz', 'Процессор': 'Google Tensor G3', 'Память': '12/256 ГБ', 'Камера': '50+48+48 МП', 'Аккумулятор': '5050 мАч', 'ОС': 'Android 14'}
            },
            {
                'name': 'OnePlus 12', 'category': 'Смартфоны', 'brand': 'OnePlus',
                'price': 89990, 'rating': 4.5, 'stock': 18,
                'image_url': 'https://oasis.opstatics.com/content/dam/oasis/page/2023/oneplus-12/product-image/12-black.png',
                'description': 'OnePlus 12 с мощным процессором и быстрой зарядкой 100W.',
                'specs': {'Экран': '6.82" AMOLED, 120Hz', 'Процессор': 'Snapdragon 8 Gen 3', 'Память': '16/512 ГБ', 'Камера': '50+48+64 МП', 'Аккумулятор': '5400 мАч', 'ОС': 'Android 14, OxygenOS'}
            },
            {
                'name': 'Samsung Galaxy A55', 'category': 'Смартфоны', 'brand': 'Samsung',
                'price': 39990, 'rating': 4.4, 'stock': 40,
                'image_url': 'https://images.samsung.com/ru/smartphones/galaxy-a55/buy/A55_Color_Selection_AwesomeNavy.png',
                'description': 'Среднебюджетный смартфон Samsung с отличным экраном и камерой.',
                'specs': {'Экран': '6.6" Super AMOLED, 120Hz', 'Процессор': 'Exynos 1480', 'Память': '8/256 ГБ', 'Камера': '50+12+5 МП', 'Аккумулятор': '5000 мАч', 'ОС': 'Android 14'}
            },
            {
                'name': 'Realme GT 5', 'category': 'Смартфоны', 'brand': 'Realme',
                'price': 54990, 'rating': 4.3, 'stock': 22,
                'image_url': 'https://image01.realme.net/general/20230828/1693206969475.png',
                'description': 'Игровой смартфон Realme GT 5 с мощной системой охлаждения.',
                'specs': {'Экран': '6.74" AMOLED, 144Hz', 'Процессор': 'Snapdragon 8 Gen 2', 'Память': '12/256 ГБ', 'Камера': '50+8+2 МП', 'Аккумулятор': '5240 мАч', 'ОС': 'Android 13, Realme UI'}
            },
            {
                'name': 'Huawei P60 Pro', 'category': 'Смартфоны', 'brand': 'Huawei',
                'price': 69990, 'rating': 4.4, 'stock': 12,
                'image_url': 'https://consumer.huawei.com/content/dam/huawei-cbg-site/common/mkt/pdp/phones/p60-pro/design.png',
                'description': 'Флагман Huawei с выдающейся камерой и уникальным дизайном.',
                'specs': {'Экран': '6.67" OLED, 120Hz', 'Процессор': 'Snapdragon 8+ Gen 1', 'Память': '8/256 ГБ', 'Камера': '48+13+48 МП', 'Аккумулятор': '4815 мАч'}
            },
            {
                'name': 'OPPO Find X7 Ultra', 'category': 'Смартфоны', 'brand': 'OPPO',
                'price': 109990, 'rating': 4.6, 'stock': 10,
                'image_url': 'https://www.oppo.com/content/dam/oppo/common/mkt/v2-2/find-x7-ultra/overview/find-x7-ultra.png',
                'description': 'Премиальный смартфон OPPO с камерой Hasselblad.',
                'specs': {'Экран': '6.82" AMOLED, 120Hz', 'Процессор': 'Snapdragon 8 Gen 3', 'Память': '16/512 ГБ', 'Камера': '50+50+50+50 МП', 'Аккумулятор': '5000 мАч', 'ОС': 'Android 14, ColorOS'}
            },
            {
                'name': 'Nothing Phone 2', 'category': 'Смартфоны', 'brand': 'Nothing',
                'price': 49990, 'rating': 4.3, 'stock': 35,
                'image_url': 'https://nothing.tech/cdn/shop/files/phone-2-white-front-back.png',
                'description': 'Уникальный смартфон с прозрачным дизайном и светодиодной подсветкой Glyph.',
                'specs': {'Экран': '6.7" OLED, 120Hz', 'Процессор': 'Snapdragon 8+ Gen 1', 'Память': '12/256 ГБ', 'Камера': '50+50 МП', 'Аккумулятор': '4700 мАч', 'ОС': 'Android 13, Nothing OS'}
            },
            # Ноутбуки (10 товаров)
            {
                'name': 'Apple MacBook Pro 16 M3 Max', 'category': 'Ноутбуки', 'brand': 'Apple',
                'price': 399990, 'rating': 4.9, 'stock': 8,
                'image_url': 'https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/mbp16-spaceblack-select-202410',
                'description': 'Самый мощный MacBook Pro с чипом M3 Max для профессионалов.',
                'specs': {'Экран': '16.2" Liquid Retina XDR', 'Процессор': 'Apple M3 Max', 'Память': '36/1024 ГБ', 'Вес': '2.14 кг', 'Батарея': 'до 22 часов'}
            },
            {
                'name': 'Lenovo ThinkPad X1 Carbon Gen 11', 'category': 'Ноутбуки', 'brand': 'Lenovo',
                'price': 159990, 'rating': 4.7, 'stock': 15,
                'image_url': 'https://www.lenovo.com/medias/lenovo-laptop-thinkpad-x1-carbon-gen-11-hero.png',
                'description': 'Премиальный бизнес-ноутбук с отличной клавиатурой и долгой автономностью.',
                'specs': {'Экран': '14" IPS, 2.8K', 'Процессор': 'Intel Core i7-1365U', 'Память': '16/512 ГБ', 'Вес': '1.12 кг', 'Батарея': 'до 15 часов'}
            },
            {
                'name': 'ASUS ROG Zephyrus G14', 'category': 'Ноутбуки', 'brand': 'ASUS',
                'price': 129990, 'rating': 4.8, 'stock': 12,
                'image_url': 'https://dlcdnwebimgs.asus.com/gain/32E83531-4A72-4E9B-8382-4A71FD926702/w717/h525',
                'description': 'Компактный игровой ноутбук с мощной начинкой и отличным дисплеем.',
                'specs': {'Экран': '14" QHD, 165Hz', 'Процессор': 'AMD Ryzen 9 7940HS', 'Видеокарта': 'NVIDIA RTX 4060', 'Память': '16/512 ГБ', 'Вес': '1.65 кг'}
            },
            {
                'name': 'Dell XPS 15', 'category': 'Ноутбуки', 'brand': 'Dell',
                'price': 179990, 'rating': 4.6, 'stock': 10,
                'image_url': 'https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/xps-notebooks/xps-15-9530',
                'description': 'Стильный и мощный ноутбук с безрамочным дисплеем InfinityEdge.',
                'specs': {'Экран': '15.6" OLED, 3.5K', 'Процессор': 'Intel Core i9-13900H', 'Видеокарта': 'NVIDIA RTX 4070', 'Память': '32/1TB ГБ', 'Вес': '1.92 кг'}
            },
            {
                'name': 'HP Spectre x360', 'category': 'Ноутбуки', 'brand': 'HP',
                'price': 149990, 'rating': 4.5, 'stock': 18,
                'image_url': 'https://www.hp.com/us-en/shop/app/assets/images/product/7P3J4UA-ABA_1.jpg',
                'description': 'Трансформер премиум-класса с OLED дисплеем.',
                'specs': {'Экран': '14" OLED, 2.8K', 'Процессор': 'Intel Core i7-1355U', 'Память': '16/512 ГБ', 'Вес': '1.37 кг', 'Батарея': 'до 13 часов'}
            },
            {
                'name': 'Acer Swift 3', 'category': 'Ноутбуки', 'brand': 'Acer',
                'price': 59990, 'rating': 4.2, 'stock': 25,
                'image_url': 'https://static.acer.com/up/Resource/Acer/Laptops/Swift_3/KSP/20201120/Acer-Swift-3-KSP-banner-1920x1080.png',
                'description': 'Доступный ультрабук для работы и учебы.',
                'specs': {'Экран': '14" IPS, Full HD', 'Процессор': 'AMD Ryzen 5 5500U', 'Память': '8/256 ГБ', 'Вес': '1.2 кг', 'Батарея': 'до 12 часов'}
            },
            {
                'name': 'MSI Stealth 16', 'category': 'Ноутбуки', 'brand': 'MSI',
                'price': 199990, 'rating': 4.7, 'stock': 7,
                'image_url': 'https://asset.msi.com/resize/image/global/product/product_1698987260a7a5c0c7c8e2b1e8b5f2a3d1e4f6a5b7.png',
                'description': 'Тонкий и мощный игровой ноутбук для киберспортсменов.',
                'specs': {'Экран': '16" QHD+, 240Hz', 'Процессор': 'Intel Core i9-13900H', 'Видеокарта': 'NVIDIA RTX 4070', 'Память': '32/1TB', 'Вес': '1.99 кг'}
            },
            {
                'name': 'Huawei MateBook 16', 'category': 'Ноутбуки', 'brand': 'Huawei',
                'price': 89990, 'rating': 4.4, 'stock': 20,
                'image_url': 'https://consumer.huawei.com/content/dam/huawei-cbg-site/common/mkt/pdp/pc/matebook-16-2022/imgs/huawei-matebook-16-2022-space-grey.png',
                'description': 'Продуктивный ноутбук с большим дисплеем для работы.',
                'specs': {'Экран': '16" IPS, 2.5K', 'Процессор': 'AMD Ryzen 9 5900H', 'Память': '16/512 ГБ', 'Вес': '1.99 кг', 'Батарея': 'до 12 часов'}
            },
            {
                'name': 'Samsung Galaxy Book3 Ultra', 'category': 'Ноутбуки', 'brand': 'Samsung',
                'price': 169990, 'rating': 4.6, 'stock': 9,
                'image_url': 'https://images.samsung.com/ru/computers/galaxy-book3-ultra/buy/galaxy-book3-ultra-graphite.png',
                'description': 'Флагманский ноутбук Samsung с AMOLED дисплеем.',
                'specs': {'Экран': '16" AMOLED, 3K', 'Процессор': 'Intel Core i9-13900H', 'Видеокарта': 'NVIDIA RTX 4070', 'Память': '32/1TB', 'Вес': '1.79 кг'}
            },
            {
                'name': 'Xiaomi Mi Notebook Pro 14', 'category': 'Ноутбуки', 'brand': 'Xiaomi',
                'price': 79990, 'rating': 4.3, 'stock': 22,
                'image_url': 'https://i01.appmifile.com/webfile/globalimg/products/pc/xiaomi-notebook-pro-14/specs.png',
                'description': 'Качественный ноутбук с хорошим соотношением цена/качество.',
                'specs': {'Экран': '14" IPS, 2.5K, 120Hz', 'Процессор': 'Intel Core i5-12450H', 'Память': '16/512 ГБ', 'Вес': '1.5 кг', 'Батарея': 'до 11 часов'}
            },
            # Наушники (10 товаров)
            {
                'name': 'Apple AirPods Pro 2', 'category': 'Наушники', 'brand': 'Apple',
                'price': 24990, 'old_price': 27990, 'rating': 4.8, 'stock': 50,
                'image_url': 'https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/airpods-pro-2-hero-select-202409',
                'description': 'Лучшие TWS наушники с активным шумоподавлением и чипом H2.',
                'specs': {'Тип': 'Внутриканальные, TWS', 'Подключение': 'Bluetooth 5.3', 'Шумоподавление': 'Активное', 'Время работы': '6 + 30 часов', 'Влагозащита': 'IPX4'}
            },
            {
                'name': 'Samsung Galaxy Buds3 Pro', 'category': 'Наушники', 'brand': 'Samsung',
                'price': 19990, 'rating': 4.6, 'stock': 35,
                'image_url': 'https://images.samsung.com/ru/galaxy-buds3-pro/buy/galaxy-buds3-pro-silver.png',
                'description': 'Премиальные TWS наушники Samsung с AI-шумоподавлением.',
                'specs': {'Тип': 'Внутриканальные, TWS', 'Подключение': 'Bluetooth 5.4', 'Шумоподавление': 'Адаптивное', 'Время работы': '7 + 28 часов', 'Влагозащита': 'IP57'}
            },
            {
                'name': 'Sony WH-1000XM5', 'category': 'Наушники', 'brand': 'Sony',
                'price': 34990, 'rating': 4.9, 'stock': 20,
                'image_url': 'https://www.sony.ru/image/5d02da5df552836db894cead8a68f5f3?fmt=pjpeg&wid=1200&hei=800&bgcolor=F1F5F9&bgc=F1F5F9',
                'description': 'Лучшие полноразмерные наушники с шумоподавлением.',
                'specs': {'Тип': 'Полноразмерные', 'Подключение': 'Bluetooth 5.2', 'Шумоподавление': 'Активное', 'Время работы': '30 часов', 'Вес': '250 г'}
            },
            {
                'name': 'AirPods Max', 'category': 'Наушники', 'brand': 'Apple',
                'price': 54990, 'rating': 4.7, 'stock': 10,
                'image_url': 'https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/airpods-max-select-spacegray-202011',
                'description': 'Премиальные полноразмерные наушники Apple с пространственным аудио.',
                'specs': {'Тип': 'Полноразмерные', 'Подключение': 'Bluetooth 5.0', 'Шумоподавление': 'Активное', 'Время работы': '20 часов', 'Вес': '384 г'}
            },
            {
                'name': 'JBL Tune 770NC', 'category': 'Наушники', 'brand': 'JBL',
                'price': 8990, 'rating': 4.3, 'stock': 45,
                'image_url': 'https://www.jbl.com/dw/image/v2/BFND_PRD/on/demandware.static/-/Sites-masterCatalog_Harman/default/dw9c6f9f8a/JBL_TUNE770NC_HERO_BLACK.png',
                'description': 'Доступные наушники JBL с хорошим звуком и шумоподавлением.',
                'specs': {'Тип': 'Полноразмерные', 'Подключение': 'Bluetooth 5.3', 'Шумоподавление': 'Активное', 'Время работы': '40 часов', 'Вес': '220 г'}
            },
            {
                'name': 'Nothing Ear (2)', 'category': 'Наушники', 'brand': 'Nothing',
                'price': 12990, 'rating': 4.4, 'stock': 30,
                'image_url': 'https://nothing.tech/cdn/shop/files/Ear2_Black_Product_Image_1.png',
                'description': 'Стильные TWS наушники с прозрачным дизайном и Hi-Res Audio.',
                'specs': {'Тип': 'Внутриканальные, TWS', 'Подключение': 'Bluetooth 5.3', 'Шумоподавление': 'Адаптивное', 'Время работы': '6 + 30 часов', 'Влагозащита': 'IP54'}
            },
            {
                'name': 'OnePlus Buds Pro 2', 'category': 'Наушники', 'brand': 'OnePlus',
                'price': 14990, 'rating': 4.5, 'stock': 28,
                'image_url': 'https://www.oneplus.com/content/dam/oasis/page/2023/02/buds-pro-2/overview/buds-pro-2-black.png',
                'description': 'TWS наушники с поддержкой пространственного аудио и Dynaudio.',
                'specs': {'Тип': 'Внутриканальные, TWS', 'Подключение': 'Bluetooth 5.3', 'Шумоподавление': 'Адаптивное', 'Время работы': '9 + 30 часов', 'Влагозащита': 'IP55'}
            },
            {
                'name': 'Sennheiser Momentum 4', 'category': 'Наушники', 'brand': 'Sennheiser',
                'price': 34990, 'rating': 4.7, 'stock': 12,
                'image_url': 'https://www.sennheiser.com/globalassets/digizuite/54945-en-hd_momentum_4_white_01.png',
                'description': 'Аудиофильские наушники с исключительным качеством звука.',
                'specs': {'Тип': 'Полноразмерные', 'Подключение': 'Bluetooth 5.2', 'Шумоподавление': 'Адаптивное', 'Время работы': '60 часов', 'Вес': '293 г'}
            },
            {
                'name': 'Huawei FreeBuds Pro 3', 'category': 'Наушники', 'brand': 'Huawei',
                'price': 17990, 'rating': 4.5, 'stock': 25,
                'image_url': 'https://consumer.huawei.com/content/dam/huawei-cbg-site/common/mkt/pdp/audio/freebuds-pro-3/imgs/huawei-freebuds-pro-3-white.png',
                'description': 'TWS наушники Huawei с тройным динамиком и ANC 3.0.',
                'specs': {'Тип': 'Внутриканальные, TWS', 'Подключение': 'Bluetooth 5.2', 'Шумоподавление': 'Интеллектуальное', 'Время работы': '6.5 + 25 часов', 'Влагозащита': 'IP54'}
            },
            {
                'name': 'Xiaomi Redmi Buds 5 Pro', 'category': 'Наушники', 'brand': 'Xiaomi',
                'price': 4990, 'rating': 4.2, 'stock': 60,
                'image_url': 'https://i01.appmifile.com/webfile/globalimg/products/pc/redmi-buds-5-pro/specs.png',
                'description': 'Бюджетные TWS наушники с хорошим шумоподавлением.',
                'specs': {'Тип': 'Внутриканальные, TWS', 'Подключение': 'Bluetooth 5.3', 'Шумоподавление': 'Активное', 'Время работы': '10 + 38 часов', 'Влагозащита': 'IP54'}
            }
        ]

        print("📝 Добавление товаров...")
        for data in products_data:
            specs_json = json.dumps(data['specs'], ensure_ascii=False)
            product = Product(
                name=data['name'],
                category=data['category'],
                brand=data.get('brand', ''),
                price=data['price'],
                old_price=data.get('old_price'),
                image_url=data['image_url'],
                description=data['description'],
                specs=specs_json,
                stock=data.get('stock', 10),
                rating=data.get('rating', 0)
            )
            db.session.add(product)
            print(f"  ✅ {data['name']}")

        # Добавление брендов
        brands_data = [
            'Apple', 'Samsung', 'Xiaomi', 'Google', 'OnePlus', 'Huawei', 'OPPO', 'Realme', 
            'Nothing', 'Lenovo', 'Dell', 'HP', 'ASUS', 'Acer', 'MSI', 'Sony', 'Sennheiser',
            'JBL', 'Bose', 'NVIDIA', 'AMD', 'Intel', 'Kingston', 'Corsair', 'Logitech'
        ]
        
        print("\n🏷️ Добавление брендов...")
        for brand_name in brands_data:
            brand = Brand(name=brand_name, logo_url=f'https://logo.clearbit.com/{brand_name.lower().replace(" ", "")}.com')
            db.session.add(brand)
            print(f"  ✅ {brand_name}")

        db.session.commit()
        
        # Создаем администратора
        create_admin()
        
        print(f"\n{'='*50}")
        print(f"🎉 Успешно добавлено {len(products_data)} товаров!")
        print(f"🏷️ Брендов: {len(brands_data)}")
        print(f"\n👤 Данные администратора:")
        print(f"   Email: Admin@mail.ru")
        print(f"   Пароль: Nikiw01908923")
        print(f"🔗 Админ-панель: http://localhost:5000/admin")
        print(f"{'='*50}")

if __name__ == "__main__":
    seed()