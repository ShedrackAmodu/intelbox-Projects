from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from storeadmin.models import Product
from storefront.models import Product as StorefrontProduct 
from django.templatetags.static import static
from django.utils import timezone
class Command(BaseCommand):
    help = 'Add products to the database and create related tables'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Cart (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER,
                    FOREIGN KEY (user_id) REFERENCES Users(id),
                    FOREIGN KEY (product_id) REFERENCES Products(id)
                )
            ''')  

            products = [ 
                ('CD Player A', 'High-quality CD player with excellent sound', 49.99, '/static/products/cd_player_a.jpg', 15, 'Supplier A', 1),
                ('CD Player B', 'Compact and portable CD player', 39.99, '/static/products/cd_player_b.jpg', 10, 'Supplier B', 1),
                ('CD Player C', 'Durable CD player with long battery life', 59.99, '/static/products/cd_player_c.jpg', 20, 'Supplier C', 1),
                ('CD Player D', 'High fidelity CD player with Bluetooth', 69.99, '/static/products/cd_player_d.jpg', 8, 'Supplier D', 1),
                ('CD Player E', 'Economical CD player with good sound', 29.99, '/static/products/cd_player_e.jpg', 25, 'Supplier E', 1),
                ('Smartphone A', 'Latest model with high performance', 499.99, '/static/products/smartphone_a.jpg', 30, 'Supplier F', 1),
                ('Smartphone B', 'Affordable smartphone with decent specs', 199.99, '/static/products/smartphone_b.jpg', 50, 'Supplier G', 1),
                ('Laptop A', 'Powerful laptop with lots of features', 999.99, '/static/products/laptop_a.jpg', 12, 'Supplier H', 1),
                ('Laptop B', 'Compact laptop perfect for students', 599.99, '/static/products/laptop_b.jpg', 18, 'Supplier I', 1),
                ('Headphones A', 'Noise-cancelling over-ear headphones', 79.99, '/static/products/headphones_a.jpg', 40, 'Supplier J', 1),
                ('Headphones B', 'Wireless in-ear headphones', 49.99, '/static/products/headphones_b.jpg', 35, 'Supplier K', 1),
  
                ('T-Shirt A', 'Comfortable cotton t-shirt', 19.99, '/static/products/tshirt_a.jpg', 50, 'Supplier D', 2),
                ('T-Shirt B', 'Stylish t-shirt with a graphic design', 24.99, '/static/products/tshirt_b.jpg', 30, 'Supplier E', 2),
                ('Jeans A', 'Classic blue jeans', 49.99, '/static/products/jeans_a.jpg', 20, 'Supplier F', 2),
                ('Jeans B', 'Ripped jeans with a modern fit', 59.99, '/static/products/jeans_b.jpg', 15, 'Supplier G', 2),
                ('Jacket A', 'Warm and cozy winter jacket', 89.99, '/static/products/jacket_a.jpg', 10, 'Supplier H', 2),
                ('Jacket B', 'Lightweight jacket for spring', 69.99, '/static/products/jacket_b.jpg', 25, 'Supplier I', 2),
                ('Crocs A', 'Unisex classic clogs', 34.99, '/static/products/crocs_a.jpg', 46, 'Supplier M', 2),
                ('Crocs B', 'Unisex baya clogs', 34.99, '/static/products/crocs_b.jpg', 130, 'Supplier M', 2),
                ('Sweater A', 'Cozy knit sweater for cold weather', 39.99, '/static/products/sweater_a.jpg', 15, 'Supplier J', 2),
                ('Sweater B', 'Crewneck sweater with ribbed cuffs', 49.99, '/static/products/sweater_b.jpg', 20, 'Supplier K', 2),
                ('Dress A', 'Floral print summer dress', 29.99, '/static/products/dress_a.jpg', 25, 'Supplier L', 2),
                ('Dress B', 'Little black dress for special occasions', 39.99, '/static/products/dress_b.jpg', 10, 'Supplier N', 2),
                ('Shorts A', 'Denim shorts with frayed hem', 24.99, '/static/products/shorts_a.jpg', 35, 'Supplier O', 2),
                ('Shorts B', 'Athletic shorts with moisture-wicking fabric', 19.99, '/static/products/shorts_b.jpg', 40, 'Supplier P', 2),
                
                ('Refrigerator A', 'Energy-efficient refrigerator with ample storage', 599.99, '/static/products/refrigerator_a.jpg', 10, 'Supplier A', 3),
                ('Refrigerator B', 'Compact refrigerator suitable for small spaces', 399.99, '/static/products/refrigerator_b.jpg', 15, 'Supplier B', 3),
                ('Washing Machine A', 'High-capacity washing machine with multiple settings', 499.99, '/static/products/washing_machine_a.jpg', 8, 'Supplier C', 3),
                ('Washing Machine B', 'Front-loading washing machine with energy-saving features', 699.99, '/static/products/washing_machine_b.jpg', 7, 'Supplier D', 3),
                ('Microwave A', 'Compact microwave with quick cooking settings', 99.99, '/static/products/microwave_a.jpg', 20, 'Supplier E', 3),
                ('Microwave B', 'Large microwave with convection cooking', 199.99, '/static/products/microwave_b.jpg', 12, 'Supplier F', 3),
                ('Dishwasher A', 'Energy-efficient dishwasher with multiple wash cycles', 399.99, '/static/products/dishwasher_a.jpg', 9, 'Supplier G', 3),
                ('Dishwasher B', 'Compact dishwasher suitable for small kitchens', 299.99, '/static/products/dishwasher_b.jpg', 14, 'Supplier H', 3),
                ('Blender A', 'High-speed blender for smoothies and soups', 59.99, '/static/products/blender_a.jpg', 25, 'Supplier I', 3),
                ('Blender B', 'Compact blender with multiple speed settings', 39.99, '/static/products/blender_b.jpg', 30, 'Supplier J', 3),
                ('Toaster A', '2-slice toaster with adjustable browning control', 29.99, '/static/products/toaster_a.jpg', 50, 'Supplier K', 3),
                ('Toaster B', '4-slice toaster with defrost and reheat functions', 49.99, '/static/products/toaster_b.jpg', 35, 'Supplier L', 3),
                ('Coffee Maker A', 'Single-serve coffee maker with quick brew feature', 79.99, '/static/products/coffee_maker_a.jpg', 20, 'Supplier M', 3),
                ('Coffee Maker B', 'Drip coffee maker with programmable timer', 99.99, '/static/products/coffee_maker_b.jpg', 18, 'Supplier N', 3),
                ('Air Conditioner A', 'Portable air conditioner with remote control', 299.99, '/static/products/air_conditioner_a.jpg', 12, 'Supplier O', 3),
                
                ('Notebook A', 'Hardcover notebook for writing', 5.99, '/static/products/notebook_a.jpg', 50, 'Supplier H', 4),
                ('Notebook B', 'Softcover notebook for drawing', 4.99, '/static/products/notebook_b.jpg', 40, 'Supplier I', 4),
                ('Book A', 'Interesting novel by a famous author', 9.99, '/static/products/book_a.jpg', 25, 'Supplier F', 4),
                ('Book B', 'Non-fiction book on a popular topic', 14.99, '/static/products/book_b.jpg', 15, 'Supplier G', 4),
                ('Book C', 'Science fiction novel set in a futuristic world', 12.99, '/static/products/book_c.jpg', 20, 'Supplier H', 4),
                ('Book D', 'Romantic novel with an engaging storyline', 7.99, '/static/products/book_d.jpg', 30, 'Supplier I', 4),
                ('Book E', 'Thriller novel full of suspense', 10.99, '/static/products/book_e.jpg', 25, 'Supplier J', 4),
                ('Book F', 'Historical fiction novel set in ancient times', 11.99, '/static/products/book_f.jpg', 18, 'Supplier K', 4),
                ('Book G', 'Fantasy novel with magical creatures', 13.99, '/static/products/book_g.jpg', 22, 'Supplier L', 4),
                ('Book H', 'Mystery novel with a gripping plot', 8.99, '/static/products/book_h.jpg', 27, 'Supplier M', 4),
                ('Book I', 'Biography of a famous personality', 15.99, '/static/products/book_i.jpg', 16, 'Supplier N', 4),
                ('Book J', 'Self-help book with practical advice', 9.49, '/static/products/book_j.jpg', 24, 'Supplier O', 4),
                ('Book K', 'Childrens book with colorful illustrations', 6.99, '/static/products/book_k.jpg', 35, 'Supplier P', 4),
                ('Book L', 'Cookbook with delicious recipes', 12.49, '/static/products/book_l.jpg', 20, 'Supplier Q', 4),
                ('Book M', 'Travel guide to exotic destinations', 13.49, '/static/products/book_m.jpg', 19, 'Supplier R', 4),
                ('Book N', 'Poetry book with beautiful verses', 7.49, '/static/products/book_n.jpg', 28, 'Supplier S', 4),
                ('Book O', 'Classic novel reprint with new foreword', 10.49, '/static/products/book_o.jpg', 17, 'Supplier T', 4),
                ('Book P', 'Graphic novel with stunning artwork', 16.99, '/static/products/book_p.jpg', 21, 'Supplier U', 4),
                ('Book Q', 'Health and wellness book', 11.49, '/static/products/book_q.jpg', 26, 'Supplier V', 4),
                ('Book R', 'Science textbook for high school students', 19.99, '/static/products/book_r.jpg', 14, 'Supplier W', 4),
                ('Book S', 'Business book with strategies for success', 14.49, '/static/products/book_s.jpg', 23, 'Supplier X', 4),
                ('Book T', 'Art book with famous paintings and commentary', 18.99, '/static/products/book_t.jpg', 12, 'Supplier Y', 4),
   
                ('Facial Sheet Mask A', 'Face & Eye Sheet Masks for Dehydrated, Dull and Tired Skin, With Hyaluronic Acid and Glycerine', 6.97, '/static/products/facial_sheet_mask_a.jpg', 40, 'Supplier D', 5),
                ('Facial Sheet Mask B', 'Anti-Aging Face Mask with Collagen', 7.99, '/static/products/facial_sheet_mask_b.jpg', 35, 'Supplier E', 5),
                ('Hair Serum A', 'Nourishing hair serum for dry hair', 14.99, '/static/products/hair_serum_a.jpg', 25, 'Supplier F', 5),
                ('Hair Serum B', 'Anti-frizz hair serum with argan oil', 12.99, '/static/products/hair_serum_b.jpg', 30, 'Supplier G', 5),
                ('Moisturizer A', 'Hydrating moisturizer for all skin types', 19.99, '/static/products/moisturizer_a.jpg', 20, 'Supplier H', 5),
                ('Moisturizer B', 'Oil-free moisturizer with SPF 15', 17.99, '/static/products/moisturizer_b.jpg', 22, 'Supplier I', 5),
                ('Lip Balm A', 'Moisturizing lip balm with shea butter', 3.99, '/static/products/lip_balm_a.jpg', 50, 'Supplier J', 5),
                ('Lip Balm B', 'Tinted lip balm with natural ingredients', 4.99, '/static/products/lip_balm_b.jpg', 45, 'Supplier K', 5),
                ('Sunscreen A', 'Broad-spectrum sunscreen SPF 50', 9.99, '/static/products/sunscreen_a.jpg', 30, 'Supplier L', 5),
                ('Sunscreen B', 'Water-resistant sunscreen SPF 30', 8.99, '/static/products/sunscreen_b.jpg', 35, 'Supplier M', 5),
                ('Shampoo A', 'Volumizing shampoo for fine hair', 10.99, '/static/products/shampoo_a.jpg', 40, 'Supplier N', 5),
                ('Shampoo B', 'Anti-dandruff shampoo with zinc pyrithione', 11.99, '/static/products/shampoo_b.jpg', 38, 'Supplier O', 5),
                ('Conditioner A', 'Moisturizing conditioner for dry hair', 10.49, '/static/products/conditioner_a.jpg', 42, 'Supplier P', 5),
                ('Conditioner B', 'Color-safe conditioner for treated hair', 11.49, '/static/products/conditioner_b.jpg', 36, 'Supplier Q', 5),
                ('Face Wash A', 'Gentle face wash for sensitive skin', 6.99, '/static/products/face_wash_a.jpg', 45, 'Supplier R', 5),
                ('Face Wash B', 'Deep cleansing face wash with salicylic acid', 7.49, '/static/products/face_wash_b.jpg', 40, 'Supplier S', 5),
                ('Body Lotion A', 'Hydrating body lotion with aloe vera', 8.49, '/static/products/body_lotion_a.jpg', 50, 'Supplier T', 5),
                ('Body Lotion B', 'Firming body lotion with caffeine', 9.49, '/static/products/body_lotion_b.jpg', 48, 'Supplier U', 5),
                ('Eye Cream A', 'Anti-wrinkle eye cream with retinol', 15.99, '/static/products/eye_cream_a.jpg', 28, 'Supplier V', 5),
                ('Eye Cream B', 'Brightening eye cream with vitamin C', 14.99, '/static/products/eye_cream_b.jpg', 30, 'Supplier W', 5),
   
                ('Weighing Scale A', 'Mechanical weighing scale with easy to read dial', 19.79, '/static/products/weighing_scale_a.jpg', 2, 'Supplier O', 6),
                ('Weighing Scale B', 'Electronic Bath Scales with High Precision Sensors', 9.79, '/static/products/weighing_scale_b.jpg', 10, 'Supplier O', 6),
                ('Hiking Backpack', 'Water-resistant backpack for hiking adventures', 39.99, '/static/products/hiking_backpack.jpg', 15, 'Supplier P', 6),
                ('Tent', '2-person dome tent for camping trips', 69.99, '/static/products/tent.jpg', 8, 'Supplier Q', 6),
                ('Sleeping Bag', 'Lightweight sleeping bag for outdoor use', 29.99, '/static/products/sleeping_bag.jpg', 20, 'Supplier R', 6),
                ('Camping Stove', 'Portable camping stove with propane burner', 49.99, '/static/products/camping_stove.jpg', 12, 'Supplier S', 6),
                ('Fishing Rod', 'Fiberglass fishing rod for freshwater fishing', 29.99, '/static/products/fishing_rod.jpg', 18, 'Supplier T', 6),
                ('Tennis Racket', 'Carbon fiber tennis racket for beginners', 59.99, '/static/products/tennis_racket.jpg', 10, 'Supplier U', 6),
                ('Soccer Ball', 'Size 5 soccer ball for training and matches', 19.99, '/static/products/soccer_ball.jpg', 25, 'Supplier V', 6),
                ('Basketball', 'Official size basketball for outdoor courts', 29.99, '/static/products/basketball.jpg', 20, 'Supplier W', 6),
                ('Golf Clubs Set', 'Complete set of golf clubs with bag', 199.99, '/static/products/golf_clubs_set.jpg', 5, 'Supplier X', 6),
                ('Swimming Goggles', 'Anti-fog swimming goggles for adults', 14.99, '/static/products/swimming_goggles.jpg', 30, 'Supplier Y', 6),
                ('Cycling Helmet', 'Adjustable cycling helmet for safety', 24.99, '/static/products/cycling_helmet.jpg', 35, 'Supplier Z', 6),
                ('Yoga Mat', 'Non-slip yoga mat for indoor and outdoor use', 19.99, '/static/products/yoga_mat.jpg', 15, 'Supplier A', 6),
                ('Resistance Bands Set', 'Set of resistance bands for home workouts', 29.99, '/static/products/resistance_bands_set.jpg', 20, 'Supplier B', 6),
   
                ('RC plane', 'Toy planes for kids above 5 years old', 8.56, '/static/products/Rc_plane.jpg', 80, 'Supplier Q', 7),
                ('Lego Set A', 'Building blocks for creative play', 29.99, '/static/products/lego_set_a.jpg', 40, 'Supplier A', 7),
                ('Lego Set B', 'Advanced building set for older kids', 49.99, '/static/products/lego_set_b.jpg', 30, 'Supplier B', 7),
                ('Board Game A', 'Fun board game for the whole family', 19.99, '/static/products/board_game_a.jpg', 50, 'Supplier C', 7),
                ('Board Game B', 'Strategy game with complex rules', 24.99, '/static/products/board_game_b.jpg', 25, 'Supplier D', 7),
                ('Puzzle A', '1000-piece puzzle with a beautiful landscape', 14.99, '/static/products/puzzle_a.jpg', 60, 'Supplier E', 7),
                ('Puzzle B', '500-piece puzzle with a cartoon theme', 9.99, '/static/products/puzzle_b.jpg', 70, 'Supplier F', 7),
                ('Doll A', 'Fashion doll with multiple outfits', 12.99, '/static/products/doll_a.jpg', 35, 'Supplier G', 7),
                ('Doll B', 'Baby doll with accessories', 15.99, '/static/products/doll_b.jpg', 40, 'Supplier H', 7),
                ('Action Figure A', 'Superhero action figure with movable parts', 18.99, '/static/products/action_figure_a.jpg', 45, 'Supplier I', 7),
                ('Action Figure B', 'Villain action figure with accessories', 16.99, '/static/products/action_figure_b.jpg', 50, 'Supplier J', 7),
                ('RC Car A', 'Remote-controlled car with high speed', 22.99, '/static/products/rc_car_a.jpg', 30, 'Supplier K', 7),
                ('RC Car B', 'Off-road remote-controlled truck', 27.99, '/static/products/rc_car_b.jpg', 25, 'Supplier L', 7),
                ('Stuffed Animal A', 'Soft and cuddly teddy bear', 8.99, '/static/products/stuffed_animal_a.jpg', 70, 'Supplier M', 7),
                ('Stuffed Animal B', 'Plush bunny with long ears', 7.99, '/static/products/stuffed_animal_b.jpg', 75, 'Supplier N', 7),
                ('Toy Train Set', 'Electric train set with tracks and accessories', 39.99, '/static/products/toy_train_set.jpg', 20, 'Supplier O', 7),
                ('Play-Doh Set', 'Modeling clay for creative fun', 9.99, '/static/products/play_doh_set.jpg', 60, 'Supplier P', 7),
                ('Educational Toy A', 'Learning tablet for kids with educational games', 49.99, '/static/products/educational_toy_a.jpg', 20, 'Supplier Q', 7),
                ('Educational Toy B', 'Interactive globe with facts and quizzes', 34.99, '/static/products/educational_toy_b.jpg', 25, 'Supplier R', 7),
                ('Outdoor Game Set', 'Set of outdoor games for kids', 29.99, '/static/products/outdoor_game_set.jpg', 40, 'Supplier S', 7),
  
                ('Mirror A', '800x600 Bathroom Wall Mirror with LED Lights, with Demister Pad and Touch Sensor', 64.60, '/static/products/mirror_a.jpg', 60, 'Supplier A', 8),
                ('Mirror B', '50 x 70 Small Bathroom Wall Shaving Mirror with Storage', 33.40, '/static/products/mirror_b.jpg', 15, 'Supplier A', 8),
                ('Sofa A', '3-seater sofa with plush cushions', 299.99, '/static/products/sofa_a.jpg', 10, 'Supplier B', 8),
                ('Sofa B', '2-seater loveseat with fabric upholstery', 199.99, '/static/products/sofa_b.jpg', 12, 'Supplier C', 8),
                ('Dining Table A', 'Wooden dining table with 4 chairs', 399.99, '/static/products/dining_table_a.jpg', 8, 'Supplier D', 8),
                ('Dining Table B', 'Glass-top dining table with metal legs', 349.99, '/static/products/dining_table_b.jpg', 7, 'Supplier E', 8),
                ('Chair A', 'Ergonomic office chair with lumbar support', 129.99, '/static/products/chair_a.jpg', 20, 'Supplier F', 8),
                ('Chair B', 'Set of 2 dining chairs with cushioned seats', 89.99, '/static/products/chair_b.jpg', 15, 'Supplier G', 8),
                ('Bed Frame A', 'Queen size bed frame with wooden slats', 249.99, '/static/products/bed_frame_a.jpg', 5, 'Supplier H', 8),
                ('Bed Frame B', 'King size metal bed frame with headboard', 299.99, '/static/products/bed_frame_b.jpg', 4, 'Supplier I', 8),
                ('Wardrobe A', '3-door wardrobe with mirror', 499.99, '/static/products/wardrobe_a.jpg', 6, 'Supplier J', 8),
                ('Wardrobe B', '2-door wardrobe with drawers', 399.99, '/static/products/wardrobe_b.jpg', 8, 'Supplier K', 8),
                ('Bookshelf A', '5-tier wooden bookshelf', 149.99, '/static/products/bookshelf_a.jpg', 10, 'Supplier L', 8),
                ('Bookshelf B', 'Metal bookshelf with adjustable shelves', 99.99, '/static/products/bookshelf_b.jpg', 12, 'Supplier M', 8),
                ('Coffee Table A', 'Modern coffee table with glass top', 89.99, '/static/products/coffee_table_a.jpg', 18, 'Supplier N', 8),
                ('Coffee Table B', 'Rustic coffee table with storage', 79.99, '/static/products/coffee_table_b.jpg', 20, 'Supplier O', 8),
                ('TV Stand A', 'Wooden TV stand with drawers', 199.99, '/static/products/tv_stand_a.jpg', 9, 'Supplier P', 8),
                ('TV Stand B', 'Metal TV stand with glass shelves', 149.99, '/static/products/tv_stand_b.jpg', 11, 'Supplier Q', 8),
                ('Desk A', 'L-shaped computer desk with storage', 179.99, '/static/products/desk_a.jpg', 7, 'Supplier R', 8),
                ('Desk B', 'Compact writing desk with drawers', 129.99, '/static/products/desk_b.jpg', 10, 'Supplier S', 8), 

                ('Motorcycle Headlights A', '66W 3000LM DOT LED Headlight with DRL High Low Beam, Compatible with Enduro Motorcycle Pit Bike', 49.28 , '/static/products/motorcyle_headlights_a.jpg', 12, 'Supplier E',9),
                ('Car Wax', 'High-quality car wax for glossy finish', 19.99, '/static/products/car_wax.jpg', 50, 'Supplier A', 9),
                ('Car Wash Shampoo', 'Gentle shampoo for car exterior', 12.99, '/static/products/car_wash_shampoo.jpg', 40, 'Supplier B', 9),
                ('Microfiber Towels', 'Soft and absorbent towels for car cleaning', 9.99, '/static/products/microfiber_towels.jpg', 60, 'Supplier C', 9),
                ('Tire Pressure Gauge', 'Digital tire pressure gauge with LCD display', 14.99, '/static/products/tire_pressure_gauge.jpg', 30, 'Supplier D', 9),
                ('Car Battery Charger', 'Automatic car battery charger', 49.99, '/static/products/car_battery_charger.jpg', 20, 'Supplier E', 9),
                ('Jump Starter', 'Portable jump starter for dead batteries', 79.99, '/static/products/jump_starter.jpg', 15, 'Supplier F', 9),
                ('Oil Filter', 'High-performance oil filter for engine protection', 8.99, '/static/products/oil_filter.jpg', 70, 'Supplier G', 9),
                ('Air Filter', 'Replacement air filter for improved engine performance', 12.99, '/static/products/air_filter.jpg', 60, 'Supplier H', 9),
                ('Spark Plugs', 'Set of spark plugs for smooth engine ignition', 19.99, '/static/products/spark_plugs.jpg', 50, 'Supplier I', 9),
                ('Wiper Blades', 'Pair of windshield wiper blades', 16.99, '/static/products/wiper_blades.jpg', 40, 'Supplier J', 9),
                ('Car Floor Mats', 'All-weather rubber floor mats for car interior', 29.99, '/static/products/car_floor_mats.jpg', 25, 'Supplier K', 9),
                ('Car Seat Covers', 'Universal fit car seat covers', 34.99, '/static/products/car_seat_covers.jpg', 30, 'Supplier L', 9),
                ('Car Organizer', 'Foldable car trunk organizer', 24.99, '/static/products/car_organizer.jpg', 35, 'Supplier M', 9),
                ('Emergency Kit', 'Compact roadside emergency kit', 39.99, '/static/products/emergency_kit.jpg', 20, 'Supplier N', 9),
                ('Car Vacuum Cleaner', 'Handheld vacuum cleaner for car interior', 49.99, '/static/products/car_vacuum_cleaner.jpg', 15, 'Supplier O', 9),
  
                ('Crisps A', 'Flame Grilled Steak Flavour Potato Crisps', 11.00, '/static/products/crisps_a.jpg', 100, 'Supplier T', 10),
                ('Crisps B', 'Sizzling King Prawn Potato Crisps', 11.00, '/static/products/crisps_b.jpg', 100, 'Supplier T', 10),
                ('Bread', 'Whole wheat bread loaf', 2.50, '/static/products/bread.jpg', 30, 'Supplier U', 10),
                ('Milk', 'Fresh cows milk', 1.99, '/static/products/milk.jpg', 50, 'Supplier V', 10),
                ('Eggs', 'Large grade A eggs', 3.50, '/static/products/eggs.jpg', 40, 'Supplier W',10),
                ('Butter', 'Salted butter', 3.25, '/static/products/butter.jpg', 25, 'Supplier X', 10),
                ('Cheese', 'Cheddar cheese block', 4.50, '/static/products/cheese.jpg', 20, 'Supplier Y', 10),
                ('Yogurt', 'Greek yogurt tub', 2.75, '/static/products/yogurt.jpg', 35, 'Supplier Z', 10),
                ('Apples', 'Fresh red apples', 1.20, '/static/products/apples.jpg', 60, 'Supplier A', 10),
                ('Bananas', 'Ripe bananas', 0.60, '/static/products/bananas.jpg', 80, 'Supplier B', 10),
                ('Oranges', 'Juicy oranges', 1.50, '/static/products/oranges.jpg', 45, 'Supplier C', 10),
                ('Tomatoes', 'Vine-ripened tomatoes', 2.00, '/static/products/tomatoes.jpg', 40, 'Supplier D', 10),
                ('Potatoes', 'Bag of russet potatoes', 3.00, '/static/products/potatoes.jpg', 50, 'Supplier E', 10),
                ('Onions', 'Yellow onions', 1.75, '/static/products/onions.jpg', 55, 'Supplier F', 10),
                ('Carrots', 'Fresh carrots', 1.80, '/static/products/carrots.jpg', 65, 'Supplier G', 10),
                ('Spinach', 'Organic baby spinach', 2.25, '/static/products/spinach.jpg', 30, 'Supplier H', 10),
                ('Broccoli', 'Fresh broccoli florets', 2.50, '/static/products/broccoli.jpg', 35, 'Supplier I', 10),
                ('Chicken', 'Boneless chicken breasts', 7.50, '/static/products/chicken.jpg', 15, 'Supplier J', 10),
                ('Beef', 'Lean ground beef', 9.00, '/static/products/beef.jpg', 20, 'Supplier K', 10),
                ('Salmon', 'Wild-caught salmon fillets', 10.99, '/static/products/salmon.jpg', 10, 'Supplier L', 10),         
                ]
            for product in products:
                name, description, price, image_path, stock, supplier, category_id = product
                image_url = static(image_path)
                cursor.execute('''
                    SELECT name FROM storeadmin_product WHERE name = %s
                ''', [name])
                result = cursor.fetchone()
                if result:
                    # Update existing product
                    cursor.execute('''
                        UPDATE storeadmin_product
                        SET stock = %s
                        WHERE name = %s
                    ''', [stock, name])
                else:
                    # Insert new product    
                    cursor.execute('''
                        INSERT INTO storeadmin_product (name, description, price, image_url, stock, supplier, category_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', [name, description, price, image_url, stock, supplier, category_id])
            for product in products:
                name, description, price, image_path, stock, supplier, category_id = product
                image_url = static(image_path)
                now = timezone.now()
                cursor.execute('''
                    SELECT name FROM storefront_product WHERE name = %s
                ''', [name])
                resultp = cursor.fetchone()            
                if resultp:
                    # Update existing product
                    cursor.execute('''
                        UPDATE storefront_product
                        SET stock = %s, updated_at = %s
                        WHERE name = %s
                    ''', [stock,now, name])
                else:
                       
                    created_at = timezone.now()
                    updated_at= timezone.now()
                    cursor.execute( '''
                               INSERT INTO storefront_product (name, description, price, stock, created_at, image_url, updated_at )
                              VALUES (%s, %s, %s, %s, %s,%s, %s)
                               ''', 
                               [name, description, price,stock,  created_at,image_url , updated_at])
            self.stdout.write(self.style.SUCCESS('Tables created and populated with sample data successfully.'))