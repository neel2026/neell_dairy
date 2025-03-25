import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from app.models import Product, Review

# Realistic Indian names for reviews
REVIEWER_NAMES = [
    "Raj Sharma", "Priya Patel", "Amit Singh", "Neha Gupta", "Vikram Desai", 
    "Ananya Verma", "Arjun Kumar", "Meera Reddy", "Rahul Malhotra", "Shreya Nair",
    "Deepak Joshi", "Kavita Iyer", "Sanjay Agarwal", "Divya Chauhan", "Rajesh Khanna",
    "Sonali Bhatia", "Vijay Menon", "Pooja Shah", "Nikhil Chopra", "Sneha Kulkarni",
    "Varun Saxena", "Ritu Choudhury", "Mohit Kapoor", "Anjali Mehta", "Kiran Rao"
]

# Product category specific review templates
DAIRY_REVIEW_TEMPLATES = {
    'CR': {  # Curd
        1: [
            "This {product} has a sour taste. Not the quality I expected.",
            "The {product} spoiled very quickly. Wouldn't recommend.",
            "This {product} lacks freshness and has an off-putting texture.",
            "Not creamy at all for a {product}. Disappointing purchase.",
            "The {product} was too watery and had a strange aftertaste."
        ],
        2: [
            "This {product} is average at best. Not very thick or creamy.",
            "The {product} is a bit too tangy for my taste.",
            "The consistency of this {product} could be better.",
            "{product} doesn't have that homemade taste I was looking for.",
            "This {product} is okay for cooking but not good enough to eat plain."
        ],
        3: [
            "Decent {product} for everyday use. Nothing extraordinary.",
            "This {product} has a balanced taste. Good for making raita.",
            "Standard quality {product}. Does the job for cooking.",
            "The {product} has a nice consistency but could be creamier.",
            "Satisfactory {product} for the price. Good shelf life."
        ],
        4: [
            "Really good {product}! Creamy texture and perfect tanginess.",
            "This {product} is fresh and has a wonderful consistency.",
            "Great {product} for making lassi and desserts. Very versatile.",
            "The {product} has that authentic homemade taste. Quite impressed!",
            "Very good quality {product}. Tastes fresh and natural."
        ],
        5: [
            "Excellent {product}! Reminds me of homemade dahi from my childhood.",
            "Best {product} I've ever bought! Perfect thickness and taste.",
            "This {product} is amazing for making kadhi. Rich and creamy!",
            "The {product} is absolutely delicious. My family loves it!",
            "Outstanding quality {product}. Will definitely buy again!"
        ]
    },
    'ML': {  # Milk
        1: [
            "This {product} has a strange aftertaste. Not fresh at all.",
            "The {product} spoiled within a day. Very disappointed.",
            "This {product} is too watery and lacks flavor.",
            "Not worth the money. This {product} tastes artificial.",
            "The {product} curdled when I made tea. Poor quality."
        ],
        2: [
            "This {product} is just okay. Not very creamy or fresh.",
            "The {product} is a bit too thin for my preference.",
            "Average {product}. Nothing special about it.",
            "This {product} doesn't taste as good as other brands.",
            "The {product} is acceptable for tea but not good for direct consumption."
        ],
        3: [
            "Decent {product} for everyday use. Good for making tea.",
            "Standard quality {product}. No complaints.",
            "This {product} has a reasonable taste and freshness.",
            "The {product} is good enough for cooking and beverages.",
            "Satisfactory {product} with adequate fat content."
        ],
        4: [
            "Really good {product}! Fresh and creamy.",
            "This {product} makes excellent tea and coffee.",
            "Great {product} with the right balance of creaminess.",
            "The {product} tastes fresh and natural. Very happy with it!",
            "High-quality {product} that my children enjoy drinking."
        ],
        5: [
            "Excellent {product}! Tastes just like fresh farm milk.",
            "Best {product} in the market! Rich, creamy, and absolutely delicious.",
            "This {product} has amazing flavor. Perfect for making sweets.",
            "The {product} is outstanding. My family loves it!",
            "Fantastic quality {product}. Will never switch to any other brand!"
        ]
    },
    'LS': {  # Lassi
        1: [
            "This {product} is too watery and lacks flavor.",
            "The {product} has an artificial sweetness. Not enjoyable at all.",
            "This {product} doesn't have the authentic taste I expected.",
            "Not worth the money. This {product} tastes like diluted yogurt.",
            "The {product} has a strange aftertaste. Very disappointing."
        ],
        2: [
            "This {product} is just okay. Could be creamier.",
            "The {product} is a bit too sour for my taste.",
            "Average {product}. Nothing special about it.",
            "This {product} doesn't have enough flavor.",
            "The {product} is acceptable but not something I'd buy again."
        ],
        3: [
            "Decent {product} for a quick refreshment.",
            "This {product} has a good balance of sweetness and tanginess.",
            "Standard quality {product}. Satisfies the craving.",
            "The {product} has a nice consistency. Good for summer days.",
            "Reasonable {product} for the price. Good taste."
        ],
        4: [
            "Really good {product}! Perfectly balanced flavors.",
            "This {product} is quite thick and refreshing.",
            "Great {product} with authentic taste. Very enjoyable.",
            "The {product} has that homemade quality. Quite impressed!",
            "Very good quality {product}. Perfect sweetness level."
        ],
        5: [
            "Excellent {product}! Just like what I used to get from Punjab!",
            "Best {product} I've ever had! Thick, creamy, and perfectly sweetened.",
            "This {product} is amazing. Authentic taste and texture.",
            "The {product} is absolutely delicious. Nothing compares to it!",
            "Outstanding quality {product}. Refreshing and satisfying!"
        ]
    },
    'MS': {  # Milkshake
        1: [
            "This {product} tastes artificial. Not enjoyable at all.",
            "The {product} is too watery and lacks flavor.",
            "This {product} has an unpleasant aftertaste.",
            "Not worth the money. This {product} is too sweet.",
            "The {product} lacks creaminess. Very disappointing."
        ],
        2: [
            "This {product} is just okay. Nothing special.",
            "The {product} could have better flavor.",
            "Average {product}. Wouldn't buy it again.",
            "This {product} is too thin for a milkshake.",
            "The {product} is acceptable but not particularly tasty."
        ],
        3: [
            "Decent {product} for occasional indulgence.",
            "This {product} has a good flavor but could be creamier.",
            "Standard quality {product}. Satisfies the sweet tooth.",
            "The {product} has a nice taste. Good for a quick drink.",
            "Satisfactory {product} for the price. Reasonable flavor."
        ],
        4: [
            "Really good {product}! Creamy and flavorful.",
            "This {product} is thick and has a great taste.",
            "Great {product} with perfect sweetness. Very enjoyable.",
            "The {product} has that cafe-like quality. Quite impressed!",
            "Very good quality {product}. Perfect for dessert."
        ],
        5: [
            "Excellent {product}! Thick, creamy, and perfectly flavored!",
            "Best {product} in the market! Rich and absolutely delicious.",
            "This {product} is amazing. Perfect blend of milk and flavor.",
            "The {product} is outstanding. A real treat!",
            "Fantastic quality {product}. Will definitely buy again!"
        ]
    },
    'PN': {  # Paneer
        1: [
            "This {product} is too hard and rubbery. Poor quality.",
            "The {product} crumbled when I tried to cook it.",
            "This {product} has no flavor at all. Very bland.",
            "Not worth the money. This {product} spoiled quickly.",
            "The {product} had a sour taste. Very disappointing."
        ],
        2: [
            "This {product} is average. Not very fresh.",
            "The {product} is a bit too dry for my preference.",
            "Mediocre {product}. There are better options available.",
            "This {product} doesn't hold well during cooking.",
            "The {product} is acceptable for curries but not for grilling."
        ],
        3: [
            "Decent {product} for everyday cooking.",
            "This {product} has good texture. Works well in curries.",
            "Standard quality {product}. No complaints.",
            "The {product} has consistent quality. Good for daily use.",
            "Satisfactory {product} for the price. Does the job."
        ],
        4: [
            "Really good {product}! Soft and fresh.",
            "This {product} holds its shape well during cooking.",
            "Great {product} with perfect texture. Very versatile.",
            "The {product} has that homemade quality. Quite impressed!",
            "Very good quality {product}. Makes delicious dishes."
        ],
        5: [
            "Excellent {product}! Soft, fresh, and absolutely delicious!",
            "Best {product} I've ever bought! Perfect for all dishes.",
            "This {product} is amazing. Just like homemade!",
            "The {product} is outstanding. Makes the best palak paneer!",
            "Fantastic quality {product}. Fresh and perfectly textured!"
        ]
    },
    'GH': {  # Ghee
        1: [
            "This {product} doesn't have the authentic aroma. Disappointing.",
            "The {product} has a strange taste. Not pure at all.",
            "This {product} solidifies oddly. Poor quality.",
            "Not worth the money. This {product} might be adulterated.",
            "The {product} lacks flavor. Very disappointing."
        ],
        2: [
            "This {product} is just okay. Not very aromatic.",
            "The {product} doesn't enhance the flavor of food much.",
            "Average {product}. Nothing special about it.",
            "This {product} is a bit too oily and lacks that traditional smell.",
            "The {product} is acceptable for everyday cooking but not for special dishes."
        ],
        3: [
            "Decent {product} for everyday cooking.",
            "This {product} has good clarity and reasonable aroma.",
            "Standard quality {product}. Does the job.",
            "The {product} has consistent quality. Good for daily use.",
            "Satisfactory {product} for the price. Reasonable taste."
        ],
        4: [
            "Really good {product}! Rich aroma and flavor.",
            "This {product} enhances the taste of every dish.",
            "Great {product} with that traditional smell. Very happy!",
            "The {product} has that homemade quality. Quite impressed!",
            "Very good quality {product}. Makes food taste better."
        ],
        5: [
            "Excellent {product}! Pure, aromatic, and absolutely fantastic!",
            "Best {product} in the market! Just like homemade ghee.",
            "This {product} is amazing. Perfect aroma and flavor.",
            "The {product} is outstanding. Makes even simple dishes delicious!",
            "Fantastic quality {product}. Will never buy any other brand!"
        ]
    },
    'CZ': {  # Cheese
        1: [
            "This {product} has a rubbery texture. Not good at all.",
            "The {product} doesn't melt properly. Very disappointing.",
            "This {product} has an artificial taste.",
            "Not worth the money. This {product} lacks flavor.",
            "The {product} spoiled quickly. Poor quality."
        ],
        2: [
            "This {product} is just okay. Nothing special.",
            "The {product} is a bit too salty for my taste.",
            "Average {product}. There are better options available.",
            "This {product} doesn't have enough flavor.",
            "The {product} is acceptable for sandwiches but not for gourmet cooking."
        ],
        3: [
            "Decent {product} for everyday use.",
            "This {product} melts well on pizzas and sandwiches.",
            "Standard quality {product}. Satisfies basic cheese cravings.",
            "The {product} has consistent quality. Good for daily use.",
            "Satisfactory {product} for the price. Does the job."
        ],
        4: [
            "Really good {product}! Creamy and flavorful.",
            "This {product} melts perfectly for pizza and pasta.",
            "Great {product} with excellent texture. Very versatile.",
            "The {product} has a rich flavor. Quite impressed!",
            "Very good quality {product}. Makes dishes taste better."
        ],
        5: [
            "Excellent {product}! Creamy, rich, and absolutely delicious!",
            "Best {product} I've bought! Perfect for all cheese dishes.",
            "This {product} is amazing. Melts beautifully and tastes great.",
            "The {product} is outstanding. Enhances every dish!",
            "Fantastic quality {product}. Will definitely buy again!"
        ]
    },
    'IC': {  # Ice-Creams
        1: [
            "This {product} has an artificial taste. Not creamy at all.",
            "The {product} melts too quickly and has poor texture.",
            "This {product} is too sweet and lacks flavor depth.",
            "Not worth the money. This {product} has ice crystals in it.",
            "The {product} doesn't taste fresh. Very disappointing."
        ],
        2: [
            "This {product} is just okay. Nothing special.",
            "The {product} is a bit too sweet for my preference.",
            "Average {product}. There are tastier options available.",
            "This {product} doesn't have enough flavor.",
            "The {product} is acceptable but not something I'd buy again."
        ],
        3: [
            "Decent {product} for occasional indulgence.",
            "This {product} has good flavor but could be creamier.",
            "Standard quality {product}. Satisfies the sweet tooth.",
            "The {product} has a nice taste. Good for hot summer days.",
            "Satisfactory {product} for the price. Reasonable flavor."
        ],
        4: [
            "Really good {product}! Creamy and flavorful.",
            "This {product} has a great texture and perfect sweetness.",
            "Great {product} with excellent flavor. Very enjoyable.",
            "The {product} has that premium quality. Quite impressed!",
            "Very good quality {product}. Perfect for dessert."
        ],
        5: [
            "Excellent {product}! Creamy, rich, and absolutely delicious!",
            "Best {product} I've ever had! Perfect blend of flavors.",
            "This {product} is amazing. Smooth texture and fantastic taste.",
            "The {product} is outstanding. A real treat!",
            "Fantastic quality {product}. Will definitely buy again!"
        ]
    }
}

# Default reviews for categories not specifically covered
DEFAULT_REVIEW_TEXTS = {
    1: [
        "Very disappointed with this product. Not worth the money.",
        "Poor quality. Would not recommend to anyone.",
        "Doesn't work as advertised. Waste of money.",
        "Had to return it. Terrible product.",
        "Very unsatisfied with my purchase."
    ],
    2: [
        "Below average product. Expected better quality.",
        "Not the worst, but wouldn't buy again.",
        "Mediocre at best. There are better options available.",
        "Somewhat disappointed with this purchase.",
        "It works, but there are many issues with it."
    ],
    3: [
        "Average product. Does what it claims to do.",
        "Decent quality for the price.",
        "Not bad, but not great either.",
        "It's okay. Meets basic expectations.",
        "Middle of the road product. Satisfactory."
    ],
    4: [
        "Good product. Happy with my purchase.",
        "Works well and good value for money.",
        "Above average quality. Would recommend.",
        "Very satisfied with this product.",
        "Almost perfect. Minor issues but overall great."
    ],
    5: [
        "Excellent product! Exceeded my expectations.",
        "Perfect in every way. Highly recommend!",
        "Best purchase I've made. Amazing quality.",
        "Absolutely love this product. Worth every penny.",
        "Outstanding quality and performance. 10/10 would buy again."
    ]
}

class Command(BaseCommand):
    help = 'Generates dummy reviews for products in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num-reviews',
            type=int,
            default=5,
            help='Number of reviews to generate per product'
        )
        
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing reviews before creating new ones'
        )

    def handle(self, *args, **options):
        num_reviews = options['num_reviews']
        clear_existing = options['clear_existing']
        
        # Get all products and users
        products = Product.objects.all()
        users = User.objects.all()
        
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please create at least one user.'))
            return
        
        if not products:
            self.stdout.write(self.style.ERROR('No products found. Please create at least one product.'))
            return
        
        # Clear existing reviews if specified
        if clear_existing:
            Review.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all existing reviews.'))
        
        # Generate reviews
        reviews_created = 0
        
        for product in products:
            # Determine how many reviews to create for this product (random between 1 and num_reviews)
            product_reviews = random.randint(1, num_reviews)
            
            for _ in range(product_reviews):
                # Select a random user
                user = random.choice(users)
                
                # Generate a random rating (weighted towards higher ratings)
                rating_weights = [0.05, 0.1, 0.2, 0.3, 0.35]  # Probabilities for ratings 1-5
                rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights)[0]
                
                # Get category-specific review templates
                category = product.category
                if category in DAIRY_REVIEW_TEMPLATES:
                    review_templates = DAIRY_REVIEW_TEMPLATES[category][rating]
                else:
                    review_templates = DEFAULT_REVIEW_TEXTS[rating]
                
                # Select a random review template and format it with the product title
                review_template = random.choice(review_templates)
                review_text = review_template.format(product=product.title)
                
                # Generate a random date within the last 90 days
                days_ago = random.randint(0, 90)
                created_at = timezone.now() - timedelta(days=days_ago)
                
                # Update user's first_name and last_name with a random name
                # This only updates the attributes for the review display, not in the database
                reviewer_name = random.choice(REVIEWER_NAMES)
                first_name, last_name = reviewer_name.split(' ', 1)
                
                # Create the review with the custom name
                review = Review.objects.create(
                    product=product,
                    user=user,
                    rating=rating,
                    review_text=review_text,
                    created_at=created_at
                )
                
                # Store the reviewer name in the review_text if it doesn't exist
                if not user.first_name:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                
                reviews_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {reviews_created} dairy-specific reviews for {products.count()} products.')
        ) 