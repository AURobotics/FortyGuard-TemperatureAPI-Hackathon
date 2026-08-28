import geopandas as gpd 
countries = gpd.read_file(
    "ne_10m_admin_0_countries.shp"
)

usa = countries[countries["ADMIN"] == "United States of Americas"]
print(usa[["ADMIN","geometry"]])