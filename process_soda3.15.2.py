# developed by Subhadeep Maishal
# Indian Institute of Technology, Kharagpur
# subhadeepmaishal@kgpian.iitkgp.ac.in
# for more about SODA data visit (https://www2.atmos.umd.edu/%7Eocean/index_files/soda3.15.2_mn_download_b.htm)
# duration of avail 1980-2021+
# about CROCO and CROCO tools visit: https://www.croco-ocean.org/
import os
import xarray as xr
import argparse

DEFAULT_INPUT_DIR = "/scratch/20cl91p02/CROCO_TOOL_FIX/Oforc_SODA"
DEFAULT_OUTPUT_DIR = "/scratch/20cl91p02/CROCO_TOOL_FIX/Oforc_SODA/output_soda"
DEFAULT_YEAR_START = 1980
DEFAULT_MONTH_START = 1
DEFAULT_YEAR_END = 1982
DEFAULT_MONTH_END = 12
DEFAULT_DATA_TYPE = "monthly"  # Default data type

def extract_variables(input_file):
    ds = xr.open_dataset(input_file)

    # Rename variables
    variable_mapping = {'u': 'uo', 'v': 'vo', 'ssh': 'zos', 'temp': 'thetao', 'salt': 'so'}
    ds = ds.rename(variable_mapping)

    # Extracting desired variables
    ds_subset = ds[['uo', 'vo', 'zos', 'thetao', 'so']]
    ds.close()
    return ds_subset

def create_monthly_files(input_dir, output_dir, start_year, end_year, start_month, end_month):
    for year in range(start_year, end_year + 1):
        input_file = f"{input_dir}/soda3.15.2_mn_ocean_reg_{year}.nc"
        
        if os.path.exists(input_file):
            for month in range(start_month, end_month + 1):
                output_file = f"{output_dir}/soda3.15.2_{year}_{month:02d}_{DEFAULT_DATA_TYPE}.nc"

                ds_subset = extract_variables(input_file)

                try:
                    ds_monthly = ds_subset.isel(time=(year - start_year) * 12 + month - start_month)
                    ds_monthly.to_netcdf(output_file)
                    print(f"Saved {output_file}")
                except IndexError:
                    print(f"Skipping {output_file} - Index out of bounds or data not available")
        else:
            print(f"Skipping {input_file} - File not found")

def main():
    parser = argparse.ArgumentParser(description="Process SODA3.15.2 data and create monthly files.")
    parser.add_argument("--input-dir", type=str, default=DEFAULT_INPUT_DIR, help="Input directory for yearly files")
    parser.add_argument("--output-dir", type=str, default=DEFAULT_OUTPUT_DIR, help="Output directory for monthly files")
    parser.add_argument("--start-year", type=int, default=DEFAULT_YEAR_START, help="Start year")
    parser.add_argument("--end-year", type=int, default=DEFAULT_YEAR_END, help="End year")
    parser.add_argument("--start-month", type=int, default=DEFAULT_MONTH_START, help="Start month")
    parser.add_argument("--end-month", type=int, default=DEFAULT_MONTH_END, help="End month")

    args = parser.parse_args()

    create_monthly_files(args.input_dir, args.output_dir, args.start_year, args.end_year, args.start_month, args.end_month)

if __name__ == "__main__":
    main()
