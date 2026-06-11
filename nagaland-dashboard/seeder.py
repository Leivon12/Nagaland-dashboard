# seeder.py

import pandas as pd
from app import app
from models import db, District, RegistrationStat

EXCEL_FILE = 'annual_report/Tables_Annual_Report_2023_Nagaland.xlsx'
YEAR = 2023

# Maps sheet name → area_type label
SHEETS = {
    'Table 1(I)' : 'Rural',
    'Table 1 (II)': 'Urban',
}

def clean_table1(sheet_name):
    """
    Reads a Table 1 sheet and returns a clean DataFrame.
    Skips the title rows, junk rows, and the TOTAL row.
    """
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, header=None)

    # Row 5 has the real column indices (0,1,2...), row 3-4 has headers
    # Actual data starts at row 6
    df = df.iloc[6:].reset_index(drop=True)

    # Rename columns positionally
    df.columns = [
        'sl_no', 'district', 'census_population',
        'reg_units', 'returns_due', 'returns_received',
        'est_midyear_pop_total', 'est_midyear_pop_adjusted'
    ]

    # Drop rows where district is NaN or contains 'TOTAL'
    df = df[df['district'].notna()]
    df = df[~df['district'].astype(str).str.upper().str.contains('TOTAL')]

    # Clean up types
    df['census_population']        = pd.to_numeric(df['census_population'], errors='coerce')
    df['reg_units']                = pd.to_numeric(df['reg_units'], errors='coerce')
    df['returns_due']              = pd.to_numeric(df['returns_due'], errors='coerce')
    df['returns_received']         = pd.to_numeric(df['returns_received'], errors='coerce')
    df['est_midyear_pop_total']    = pd.to_numeric(df['est_midyear_pop_total'], errors='coerce')
    df['est_midyear_pop_adjusted'] = pd.to_numeric(df['est_midyear_pop_adjusted'], errors='coerce')

    return df


def seed():
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        print("Tables created.")

        for sheet_name, area_type in SHEETS.items():
            df = clean_table1(sheet_name)
            print(f"Seeding {sheet_name} ({area_type}) — {len(df)} rows")

            for _, row in df.iterrows():
                district_name = str(row['district']).strip()

                # Get or create district
                district = District.query.filter_by(name=district_name).first()
                if not district:
                    district = District(name=district_name)
                    db.session.add(district)
                    db.session.flush()  # gets the ID before commit

                stat = RegistrationStat(
                    district_id              = district.id,
                    area_type                = area_type,
                    year                     = YEAR,
                    census_population        = int(row['census_population'])        if pd.notna(row['census_population'])        else None,
                    reg_units                = int(row['reg_units'])                if pd.notna(row['reg_units'])                else None,
                    returns_due              = int(row['returns_due'])              if pd.notna(row['returns_due'])              else None,
                    returns_received         = int(row['returns_received'])         if pd.notna(row['returns_received'])         else None,
                    est_midyear_pop_total    = float(row['est_midyear_pop_total'])  if pd.notna(row['est_midyear_pop_total'])    else None,
                    est_midyear_pop_adjusted = int(row['est_midyear_pop_adjusted']) if pd.notna(row['est_midyear_pop_adjusted']) else None,
                )
                db.session.add(stat)

        db.session.commit()
        print("Seeding complete.")


if __name__ == '__main__':
    seed()