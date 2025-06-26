import argparse
import os
import pandas as pd
from cpcb_fetcher import get_cpcb_location_ids, get_latest_sensors, get_all_measurements, CITY_BBOX

SAVE_DIR = r"E:\Kaatru\CPCB_Measurements"

def main():
    parser = argparse.ArgumentParser(description="Fetch CPCB Air Quality Measurements")

    parser.add_argument("--city", help="City name (e.g., chennai, delhi, gurugram)")
    parser.add_argument("--location-id", nargs="+", type=int, help="One or more specific location IDs (space-separated)")

    parser.add_argument("--type", required=True, choices=["daily", "hourly"], help="Data frequency")
    parser.add_argument("--output", required=True, help="Output CSV file name")
    parser.add_argument("--from-date", required=True, help="Start date in YYYY-MM-DD")
    parser.add_argument("--to-date", required=True, help="End date in YYYY-MM-DD")
    parser.add_argument("--parameter", help="Optional: Filter by air quality parameter (e.g., pm25, no2, o3)", required=False)

    args = parser.parse_args()

    if not args.city and not args.location_id:
        print("❌ Either --city or --location-id must be provided.")
        return

    filename = args.output
    from_date = args.from_date
    to_date = args.to_date
    parameter_filter = args.parameter.lower() if args.parameter else None
    frequency = args.type.lower()

    output_path = os.path.join(SAVE_DIR, filename)

    if os.path.exists(output_path):
        print(f"⚠ File '{filename}' already exists in {SAVE_DIR}.")
        print("❌ Please provide a different --output file name.")
        return

    os.makedirs(SAVE_DIR, exist_ok=True)

    try:
        location_ids = []

        if args.location_id:
            location_ids = args.location_id
            print(f"📍 Using manually provided location ID(s): {location_ids}")
        elif args.city:
            city = args.city.lower()
            if city not in CITY_BBOX:
                print("❌ Invalid city. Choose from:", ", ".join(CITY_BBOX.keys()))
                return
            bbox = CITY_BBOX[city]
            location_ids = get_cpcb_location_ids(*bbox)

        if not location_ids:
            print("⚠ No CPCB locations found. Exiting.")
            return

        final_data = []

        for loc_id in location_ids:
            sensor_ids = get_latest_sensors(loc_id)
            if not sensor_ids:
                print(f"⚠ No sensors found for location {loc_id}.")
                continue

            for sensor_id in sensor_ids:
                print(f"📡 Fetching {frequency} data for sensor {sensor_id} (location {loc_id})")
                data = get_all_measurements(
                    sensor_id,
                    loc_id,
                    frequency=frequency,
                    from_date=from_date,
                    to_date=to_date,
                    parameter=parameter_filter
                )
                final_data.extend(data)

        if not final_data:
            print("⚠ No data found for the given date range and filters. No file was created.")
            return

        df = pd.DataFrame(final_data)
        df.to_csv(output_path, index=False)
        print(f"✅ Data saved to {output_path}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
