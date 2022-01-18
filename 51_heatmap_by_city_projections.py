from collections import OrderedDict
import cdstoolbox as ct

# Heatmap of ambient 2m Temperature (2D color map); ERA5 (historic) -> CMIP5 (prediction)

# Define dictionary of cities to extract data from
  # ALO: Use only European cities (for better comparison - any project cities related to UHI? -> PHEWE project: 

cities = OrderedDict({   # (cities taken from the PHEWE project)
    'Helsinki': {'lat': 60.1102, 'lon': 24.7385},
    'Stockholm': {'lat': 59.3262,'lon': 17.8419},
    'Dublin': {'lat': 53.3239, 'lon': -6.5258},
    'Rotterdam': {'lat': 51.9130, 'lon': 4.4539},
    'London': {'lat': 51.5287,'lon': -0.2416},
    'Prague': {'lat': 50.0598,'lon': 14.3255},
    'Krakow': {'lat': 50.0468,'lon': 19.9348},
    'Paris': {'lat': 48.8589,'lon': 2.2769},
    'Budapest': {'lat': 47.4813,'lon': 18.9902},    
    'Zurich': {'lat': 47.3775,'lon': 8.4666},    
    'Ljubljana': {'lat': 46.0662,'lon': 14.4620},    
    'Milan': {'lat': 45.4628,'lon': 9.1076},    
    'Bucharest': {'lat': 44.4379,'lon': 26.0245},   
    'Rome': {'lat': 41.9097,'lon': 12.2558},    
    'Barcelona': {'lat': 41.3927,'lon': 2.0701},    
    'Athens': {'lat': 37.9908,'lon': 23.7033},    
})

# Define label, latitude and longitude lists
city_labels = list(cities.keys()) 
lats = [cities[k]['lat'] for k in cities.keys()] 
lons = [cities[k]['lon'] for k in cities.keys()] 

# Define global functions
#   Retrieve monthly average temperature (CMIP5)
def retrieve_cmip5():
    data = ct.catalogue.retrieve(
        'projections-cmip5-monthly-single-levels',  # (use MPI -> compatible NetCDF file format)
        {
            'ensemble_member': 'r1i1p1',
            'experiment': 'rcp_4_5',
            'variable': '2m_temperature',
            'model': 'mpi_esm_lr',
            'period': '200601-210012',
        }
    )
    return data

# Initialise the application
@ct.application(title='Heatmap by city in Europe (projections)')

# Define a livefigure and data output for the application
@ct.output.livefigure()
@ct.output.download()

def application():
    """Define a function that extracts monthly average Near Surface Air Temperature 
    for the predefined cities and plot them on a heatmap.

    Application main steps:

    - retrieve temperature gridded data
    - extract data at given locations using ct.observation.interp_from_grid
    - plot data as a heatmap
    """
    
    # Get CMIP5 data
    data = retrieve_cmip5()
    
    # Select one year from data set
    data_oney = ct.cube.index_select(data, time=[288,300])
    
    # Interpolate data for the defined list of cities
    cities_temperature = ct.observation.interp_from_grid(data_oney, lat=lats, lon=lons)
    
    # Plot the temperature data for each city as a heatmap with time on the x axis
    fig = ct.chart.heatmap(
        cities_temperature,
        xdim='time',
        yticks = city_labels, # assign the city's name to the y ticks
        layout_kwargs = {
            'title': 'Monthly 2m average temperature in 2031'
        }
    )

    return fig, cities_temperature
