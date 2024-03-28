from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_sheets import GoogleSheets
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_google_sheet(*args, **kwargs):
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    header_rows = 1
    
    #daily crimes
    sheet_url = 'https://docs.google.com/spreadsheets/d/1-GpKDEI9_sj9U-MmtYPT6HnJjpaSuXN9GNZLYwUY1No/edit?usp=sharing'
    
    #test
    #sheet_url = 'https://docs.google.com/spreadsheets/d/11XpEfrNR-vf5wcjuEXpsG_ITCxmGvfoum2Yqciv59_g/edit?usp=sharing'
    
    df = GoogleSheets.with_config(ConfigFileLoader(config_path, config_profile)).load(
        sheet_url=sheet_url,
        header_rows=header_rows
    )
    
    new_types = {
        'DR_NO': str,
        'Date Rptd': str,
        'DATE OCC': str,
        'TIME OCC': str,
        'AREA': str,
        'AREA NAME': str,
        'Rpt Dist No': str,
        'Part 1-2': str,
        'Crm Cd': str,
        'Crm Cd Desc': str,
        'Mocodes': str,
        'Vict Age': str,
        'Vict Sex': str,
        'Vict Descent': str,
        'Premis Cd': str,
        'Premis Desc': str,
        'Weapon Used Cd': str,
        'Weapon Desc': str,
        'Status': str,
        'Status Desc': str,
        'Crm Cd 1': str,
        'Crm Cd 2': str,
        'Crm Cd 3': str,
        'Crm Cd 4': str,
        'LOCATION': str,
        'Cross Street': str,
        'LAT': str,
        'LON': str
    }

    df = df.astype(new_types)
    print('aqui3')
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'