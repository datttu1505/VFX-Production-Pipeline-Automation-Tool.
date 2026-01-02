import argparse
import re
from pymongo import MongoClient

def filter_xytech_paths(filepath):
    """Filter Xytech file paths using the pattern"""
    pat = re.compile(r"^/hpsans\d+/.+", re.IGNORECASE)
    paths = []
    seen = set()
    
    with open(filepath) as file:
        for line in file:
            line = line.rstrip("\n")
            if pat.match(line) and line not in seen:
                paths.append(line)
                seen.add(line)
    
    return paths

def process_baselight_file(filepath):
    """Process baselight file - adjust based on your file format"""
    data = []
    with open(filepath) as file:
        # Parse based on your baselight file structure
        # This is a placeholder - adjust to your actual format
        for line in file:
            line = line.strip()
            if line:
                data.append({"content": line})
    return data

def main():
    parser = argparse.ArgumentParser(description='Process Baselight and Xytech files into MongoDB')
    parser.add_argument('--baselight', required=True, help='Path to Baselight file')
    parser.add_argument('--xytech', required=True, help='Path to Xytech file')
    parser.add_argument('--db-name', default='production_db', help='MongoDB database name')
    parser.add_argument('--mongo-uri', default='mongodb://localhost:27017/', help='MongoDB connection URI')
    
    args = parser.parse_args()
    
    # Connect to MongoDB
    client = MongoClient(args.mongo_uri)
    db = client[args.db_name]
    
    # Process and insert Xytech data (with filter)
    print("Processing Xytech file...")
    xytech_paths = filter_xytech_paths(args.xytech)
    xytech_collection = db['xytech']
    
    if xytech_paths:
        # Insert as documents
        xytech_docs = [{"path": path} for path in xytech_paths]
        xytech_collection.insert_many(xytech_docs)
        print(f"Inserted {len(xytech_docs)} Xytech paths")
    
    # Process and insert Baselight data (as is)
    print("Processing Baselight file...")
    baselight_data = process_baselight_file(args.baselight)
    baselight_collection = db['baselight']
    
    if baselight_data:
        baselight_collection.insert_many(baselight_data)
        print(f"Inserted {len(baselight_data)} Baselight records")
    
    print("Done!")
    client.close()

if __name__ == "__main__":
    main()