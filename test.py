db={
    "accessKey": "2ad9577e-96ef-11ed-933d-204ef64b1094",
    "secretKey": "577d2219-a99a-4d72-a146-9537f6209984",
    "item_type": [
        "Food",
        "Beverages",
        "Clothing",
        "Stationaries",
        "Wearables",
        "Electronics Accessories"
    ],
    "users": [
        {
            "name": "shashi",
            "email": "shashikrkhatri9546@gmail.com",
            "password": "Shashi@1000",
            "username": "shashi_khatri",
            "purchases": {
                "2023-01-18": [
                    {
                        "item_name": "Maggie",
                        "item_type": "Food",
                        "item_price": "14",
                        "purchase_time": "2023-01-18 12:22:21.843510+05:30"
                    }
                ]
            }
        },
        {
            "name": "umesh",
            "email": "umesh123@gmail.com",
            "password": "Umesh@123",
            "username": "umesh_das",
            "purchases": {
                "2023-01-18": [
                    {
                        "item_name": "Samosa",
                        "item_type": "Food",
                        "item_price": "7",
                        "purchase_time": "2023-01-18 12:23:03.491849+05:30"
                    }
                ]
            }
        }
    ]
}
print(len(db["users"]))