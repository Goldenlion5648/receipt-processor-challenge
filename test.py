import requests
import json


def make_post(payload_string: str):
    return requests.post("http://localhost:8080/receipts/process", 
              headers = {'Content-type': 'application/json', 'Accept': 'text/plain'},
              data=payload_string)

def test(json_value, expected_points):
    correct = make_post(json.dumps(json_value))
    response_json = json.loads(correct.content.decode())
    response_id = response_json["id"]
    # print(response_id)
    points = requests.get(f"http://localhost:8080/receipts/{response_id}/points")
    assert json.loads(points.content)["points"] == expected_points

test({
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
        },
        {
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
        },
        {
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
        },
        {
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
        },
        {
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
        }
    ],
    "total": "35.35"
}, 28)

test({
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}, 109)

test({
    "retailer": "Walgreens",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "08:13",
    "total": "2.65",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
        {"shortDescription": "Dasani", "price": "1.40"}
    ]
}, 15)

test({
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "13:13",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
}, 31)

test({
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "14:00",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
}, 31)

test({
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "14:40",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
}, 41)


def test_invalid_receipt(json_dict):
    missing_parts = make_post(json.dumps(json_dict))
    assert missing_parts.content == b"The receipt is invalid."

test_invalid_receipt({
    "retailer": "Target"
})

test_invalid_receipt({
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "14:40",
    "total": "1.25",
    "items": [
]
})

test_invalid_receipt({
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "24:00",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
})

test_invalid_receipt({
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "14:70",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
})

result_from_invalid = make_post("{")
response_from_invalid = result_from_invalid.content
assert response_from_invalid == b"The receipt is invalid."

print("all tests passed")