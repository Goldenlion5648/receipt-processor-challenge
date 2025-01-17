import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import hashlib
import uuid
import re
from math import ceil

db = {}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = ''
        found = re.match(r"/receipts/(.+?)/points", self.path)
        if not found:
            self.send_response(404)
            self.send_header('Content-type','application/json')
            self.end_headers()
            message = f"Path does not exist"
        else:
            result = get_points(found.group(1))
            if not result:
                self.send_response(404, "NotFound")
                self.send_header('Content-type','application/json')
                self.end_headers()
                message = "No receipt found for that ID."
            else:
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                message = "No receipt found for that ID."
                        
        self.wfile.write(bytes(message, "utf8"))
        # self.wfile.write(b"we heard you")
        # self.send_header('Content-type','text/html')
        # self.end_headers()

    def do_POST(self):
        if self.path == "/receipts/process":
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            try:
                result = process_receipts(body.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                self.wfile.write(b"The receipt is invalid.", "utf8")
                return
            self.wfile.write(bytes(json.dumps(result), "utf8"))
        else:
            self.send_response(400, "The receipt is invalid.")
            self.send_header('Content-type','application/text')
            self.end_headers()
            self.wfile.write(b"The receipt is invalid.")

        
def process_receipts(json_to_read: str):
    id_generated = str(uuid.uuid4())
    while id_generated in db:
        id_generated = str(uuid.uuid4())
    json_as_dict = json.loads(json_to_read)
    db[id_generated] = json_as_dict
    return {"id": id_generated}


def get_points(id_to_find):
    if id_to_find not in db:
        return False
    current_json = db[id_to_find]
    # One point for every alphanumeric character in the retailer name.
    score = sum(letter.isalnum() for letter in current_json["retailer"])
    total_as_float = float(current_json["total"])
    
    # 50 points if the total is a round dollar amount with no cents.
    if total_as_float == int(total_as_float):
        score += 50
        
    # 25 points if the total is a multiple of 0.25.
    total_divided = total_as_float / .25
    if total_divided == int(total_divided):
        score += 25
        
    # points for every 2 items
    score += 5 * (len(current_json["items"]) // 2)
    
    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in current_json["items"]:
        cur_price = float(item["price"])
        if len(item["shortDescription"].strip()) % 3 == 0:
            cur_price = ceil(cur_price * 0.2)
            score += cur_price
            
    # 6 points if the day in the purchase date is odd.
    if int(current_json["purchaseDate"].split("-")[-1]) % 2 == 1:
        score += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    purchase_time = current_json["purchaseTime"]
    hours, minutes = map(int, purchase_time.split(":"))
    if (hours == 14 and minutes >= 1) or (hours == 15):
        score += 10
    return {"points" : score}
            

def run_tests():
    expected_scores = [28, 109]
    file_index = 0
    for file in os.listdir("examples"):
        if not file.startswith("github"):
            continue
        with open(f"examples/{file}") as f:
            contents = f.read()
            result = process_receipts(contents)
            assert "id" in result
            points_calculated_dict = get_points(result["id"])
            assert "points" in points_calculated_dict
            assert points_calculated_dict["points"] == expected_scores[file_index]
            print(file, "passed")
        file_index += 1
        

if __name__ == '__main__':
    PORT = 8080
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
