import argparse
import os
import pandas as pd
from cpcb_fetcher import get_cpcb_location_ids, get_latest_sensors, get_all_measurements, CITY_BBOX

SAVE_DIR = r"E:\Kaatru\CPCB_Measurements"

def main():
    parser = argparse.ArgumentParser(description="Fetch CPCB Air Quality Measurements")
    parser.add_argument("--city", required=True, help="City name (e.g., chennai, delhi, gurugram)")
    parser.add_argument("--type", required=True, choices=["daily", "hourly"], help="Data frequency")
    parser.add_argument("--output", required=True, help="Output CSV file name")
    parser.add_argument("--from-date", required=True, help="Start date in YYYY-MM-DD")
    parser.add_argument("--to-date", required=True, help="End date in YYYY-MM-DD")
    parser.add_argument("--parameter", help="Optional: Filter by air quality parameter (e.g., pm25, no2, o3)", required=False)
    parser.add_argument("--location-id", help="Optional: Specific location ID to fetch data for", required=False)

    args = parser.parse_args()

    city = args.city.lower()
    frequency = args.type.lower()
    filename = args.output
    from_date = args.from_date
    to_date = args.to_date
    parameter_filter = args.parameter.lower() if args.parameter else None
    location_id_arg = args.location_id

    if city not in CITY_BBOX:
        print("❌ Invalid city. Choose from:", ", ".join(CITY_BBOX.keys()))
        return

    output_path = os.path.join(SAVE_DIR, filename)

    if os.path.exists(output_path):
        print(f"⚠ File '{filename}' already exists in {SAVE_DIR}.")
        print("❌ Please provide a different --output file name.")
        return

    os.makedirs(SAVE_DIR, exist_ok=True)

    try:
        if location_id_arg:
            try:
                location_ids = [int(location_id_arg)]
                print(f"📍 Fetching data for specific location ID: {location_id_arg}")
            except ValueError:
                print("❌ Invalid location ID format. Must be an integer.")
                return
        else:
            bbox = CITY_BBOX[city]
            location_ids = get_cpcb_location_ids(*bbox)

        if not location_ids:
            print(f"⚠ No CPCB locations found in {city}. Exiting.")
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
            print("⚠ No data found for the given date range and city. No file was created.")
            return

        df = pd.DataFrame(final_data)
        df.to_csv(output_path, index=False)
        print(f"✅ Data saved to {output_path}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
