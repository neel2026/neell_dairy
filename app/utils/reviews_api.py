import requests
import random
import json
import time
from datetime import datetime, timedelta
from django.conf import settings

# This is a simulated API client for reviews
# In a real application, this would make actual HTTP requests to an external API

# Sample dairy product reviewer names (Indian names)
REVIEWER_NAMES = [
    "Raj Sharma", "Priya Patel", "Amit Singh", "Neha Gupta", "Vikram Desai", 
    "Ananya Verma", "Arjun Kumar", "Meera Reddy", "Rahul Malhotra", "Shreya Nair",
    "Deepak Joshi", "Kavita Iyer", "Sanjay Agarwal", "Divya Chauhan", "Rajesh Khanna",
    "Sonali Bhatia", "Vijay Menon", "Pooja Shah", "Nikhil Chopra", "Sneha Kulkarni"
]

# Product category specific review templates
DAIRY_REVIEW_TEMPLATES = {
    'CR': [  # Curd
        "This {product} has a perfect balance of tanginess. Really fresh!",
        "I use this {product} for making raita and it's amazing.",
        "The consistency of this {product} is perfect. Not too thick or runny.",
        "Best {product} I've tried. Great for making kadhi.",
        "This {product} has that authentic homemade taste. Fantastic quality!"
    ],
    'ML': [  # Milk
        "This {product} makes perfect chai. Rich and creamy.",
        "My children love this {product}. Pure and fresh taste.",
        "The {product} has the perfect fat content. Great for making sweets.",
        "I've been using this {product} for years. Best quality always.",
        "This {product} doesn't curdle when boiled. Excellent quality!"
    ],
    'LS': [  # Lassi
        "This {product} is so refreshing on hot summer days.",
        "Perfect sweetness in this {product}. Not too overwhelming.",
        "The {product} has authentic Punjabi taste. Love it!",
        "This {product} is thick and creamy. Great after workouts.",
        "I always keep this {product} in my fridge. Great taste!"
    ],
    'MS': [  # MilkShake
        "This {product} is perfectly balanced - not too sweet.",
        "My kids absolutely love this {product}. Great for quick breakfast.",
        "The {product} has a rich, creamy texture. Delicious!",
        "This {product} tastes fresh and natural. No artificial flavors.",
        "Perfect thickness in this {product}. Satisfying and filling."
    ],
    'PN': [  # Paneer
        "This {product} holds its shape well when cooked. Perfect for tikka.",
        "The {product} is soft and fresh. Makes excellent palak paneer.",
        "This {product} doesn't become rubbery after cooking. Great quality.",
        "I use this {product} for all my dishes. Consistent quality.",
        "The {product} absorbs flavors well. Best for curries."
    ],
    'GH': [  # Ghee
        "This {product} has that traditional aroma. Makes food taste better.",
        "The {product} has clear golden color. Pure and authentic.",
        "I use this {product} for making sweets. Perfect results every time.",
        "This {product} has been our family favorite for years.",
        "The {product} has a rich taste. A little goes a long way."
    ],
    'CZ': [  # Cheese
        "This {product} melts perfectly on pizza and sandwiches.",
        "The {product} has a rich, creamy flavor. Not too salty.",
        "This {product} is versatile - great for cooking and eating as is.",
        "I always keep this {product} stocked in my fridge. Family favorite.",
        "The {product} doesn't become oily when melted. Great quality."
    ],
    'IC': [  # Ice-Creams
        "This {product} has the perfect creaminess. Not too sweet.",
        "The {product} has real fruit flavors. Delicious treat!",
        "This {product} is smooth with no ice crystals. Perfect texture.",
        "My children ask for this {product} all the time. Great quality.",
        "The {product} doesn't melt too quickly. Perfect for summer parties."
    ]
}

# Generic reviews for any category
GENERIC_REVIEWS = [
    "Great quality {product}. Highly recommend!",
    "This {product} exceeded my expectations. Will buy again.",
    "Been using this {product} for years. Never disappoints.",
    "Perfect {product} for daily use. Excellent value.",
    "This {product} is better than other brands I've tried."
]

class ReviewsAPI:
    """
    A simulated API client for fetching product reviews.
    In a real application, this would make HTTP requests to an external API.
    """
    
    # Dictionary to store user-submitted reviews
    # Format: {product_id: [list of review dictionaries]}
    user_reviews = {}
    
    @staticmethod
    def get_product_reviews(product_id, product_title, category):
        """
        Simulates fetching reviews for a product from an API.
        
        Args:
            product_id: The ID of the product
            product_title: The title of the product
            category: The category code of the product
            
        Returns:
            A list of review dictionaries
        """
        # Simulate API latency
        time.sleep(0.2)
        
        # Generate a consistent number of reviews for each product
        # based on product_id to ensure same reviews each time
        random.seed(product_id)
        num_reviews = random.randint(3, 8)
        
        # Generate the simulated API reviews
        reviews = []
        
        # Generate reviews with timestamps spread over the last 90 days
        for i in range(num_reviews):
            # Generate a random rating (weighted towards higher ratings)
            rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.2, 0.3, 0.35])[0]
            
            # Select a review template based on category or use generic
            if category in DAIRY_REVIEW_TEMPLATES:
                review_templates = DAIRY_REVIEW_TEMPLATES[category]
            else:
                review_templates = GENERIC_REVIEWS
            
            # Format the review with the product title
            review_text = random.choice(review_templates).format(product=product_title)
            
            # Generate a random date within the last 90 days
            days_ago = random.randint(0, 90)
            review_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            # Select a random reviewer name
            reviewer_name = random.choice(REVIEWER_NAMES)
            
            # Create review object
            review = {
                "id": f"{product_id}-{i}",
                "product_id": product_id,
                "rating": rating,
                "reviewer_name": reviewer_name,
                "review_text": review_text,
                "date": review_date
            }
            
            reviews.append(review)
            
        # Add any user-submitted reviews for this product
        if product_id in ReviewsAPI.user_reviews:
            reviews.extend(ReviewsAPI.user_reviews[product_id])
        
        # Sort reviews by date (newest first)
        reviews.sort(key=lambda x: x["date"], reverse=True)
        
        # Simulate API response structure
        response = {
            "status": "success",
            "product_id": product_id,
            "count": len(reviews),
            "average_rating": round(sum(r["rating"] for r in reviews) / len(reviews), 1) if reviews else 0,
            "reviews": reviews
        }
        
        return response
    
    @staticmethod
    def submit_review(product_id, user_name, rating, review_text, user_id=None):
        """
        Simulates submitting a review to an API.
        In a real application, this would send a POST request to an external API.
        
        Args:
            product_id: The ID of the product
            user_name: The name of the reviewer
            rating: The rating (1-5)
            review_text: The review text
            user_id: The ID of the user submitting the review (for permission control)
            
        Returns:
            A dictionary with the response status
        """
        # Simulate API latency
        time.sleep(0.5)
        
        # Create a review object
        review_id = f"{product_id}-user-{int(time.time())}"
        today = datetime.now().strftime("%Y-%m-%d")
        
        review = {
            "id": review_id,
            "product_id": product_id,
            "rating": rating,
            "reviewer_name": user_name,
            "review_text": review_text,
            "date": today,
            "is_user_submitted": True,  # Flag to identify user-submitted reviews
            "user_id": user_id  # Store user ID for permission control
        }
        
        # Store the review in our "database"
        if product_id not in ReviewsAPI.user_reviews:
            ReviewsAPI.user_reviews[product_id] = []
        
        ReviewsAPI.user_reviews[product_id].append(review)
        
        # Simulate a successful API response
        response = {
            "status": "success",
            "message": "Review submitted successfully",
            "review_id": review_id
        }
        
        return response
        
    @staticmethod
    def get_review_by_id(review_id):
        """
        Retrieves a specific review by its ID.
        
        Args:
            review_id: The ID of the review to retrieve
            
        Returns:
            The review object or None if not found
        """
        # Check all product reviews
        for product_id, reviews in ReviewsAPI.user_reviews.items():
            for review in reviews:
                if review["id"] == review_id:
                    return review
        
        return None
    
    @staticmethod
    def edit_review(review_id, rating, review_text, user_id=None):
        """
        Edits an existing review.
        
        Args:
            review_id: The ID of the review to edit
            rating: The updated rating
            review_text: The updated review text
            user_id: The ID of the user attempting to edit (for permission control)
            
        Returns:
            A dictionary with the response status
        """
        # Simulate API latency
        time.sleep(0.5)
        
        # Find the review
        for product_id, reviews in ReviewsAPI.user_reviews.items():
            for i, review in enumerate(reviews):
                if review["id"] == review_id:
                    # Check if the user has permission to edit
                    if user_id is not None and review.get("user_id") is not None and review["user_id"] != user_id:
                        # User doesn't have permission
                        return {
                            "status": "error",
                            "message": "You don't have permission to edit this review",
                            "review_id": review_id
                        }
                    
                    # Update the review
                    ReviewsAPI.user_reviews[product_id][i]["rating"] = rating
                    ReviewsAPI.user_reviews[product_id][i]["review_text"] = review_text
                    ReviewsAPI.user_reviews[product_id][i]["date"] = datetime.now().strftime("%Y-%m-%d") + " (Edited)"
                    
                    # Simulate a successful API response
                    return {
                        "status": "success",
                        "message": "Review updated successfully",
                        "review_id": review_id
                    }
        
        # Review not found
        return {
            "status": "error",
            "message": "Review not found",
            "review_id": review_id
        }
    
    @staticmethod
    def delete_review(review_id, user_id=None):
        """
        Deletes a review by its ID.
        
        Args:
            review_id: The ID of the review to delete
            user_id: The ID of the user attempting to delete (for permission control)
            
        Returns:
            A dictionary with the response status
        """
        # Simulate API latency
        time.sleep(0.5)
        
        # Find and delete the review
        for product_id, reviews in ReviewsAPI.user_reviews.items():
            for i, review in enumerate(reviews):
                if review["id"] == review_id:
                    # Check if user has permission to delete
                    if user_id is not None and review.get("user_id") is not None and review["user_id"] != user_id:
                        # User doesn't have permission
                        return {
                            "status": "error",
                            "message": "You don't have permission to delete this review",
                            "review_id": review_id
                        }
                    
                    # Remove the review
                    del ReviewsAPI.user_reviews[product_id][i]
                    
                    # Clean up empty product entries
                    if not ReviewsAPI.user_reviews[product_id]:
                        del ReviewsAPI.user_reviews[product_id]
                    
                    # Simulate a successful API response
                    return {
                        "status": "success",
                        "message": "Review deleted successfully",
                        "review_id": review_id
                    }
        
        # Review not found
        return {
            "status": "error",
            "message": "Review not found",
            "review_id": review_id
        } 