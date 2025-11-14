import sys

from sunpy.data import cache

from sunpy.time import parse_time

from sunpy.net import Fido
from sunpy.net import attrs as a

from sunpy.timeseries import TimeSeries

from sunpy.coordinates import spice


def download_sc_dataset(sc_name, ds_type, time_window):
    """
    Download PSP/SolO/ACE data using CDAweb formatted into a pandas.DataFrame.

    Parameters
    ----------

    sc_name: 'psp', 'solo' or 'ace'
        String of the spacecraft name
    
    ds_type: 'mag' or 'sw'
        String selecting either magnetic or solar wind data
    
    time_window: tuple of date str
        Strings of start and end date
    
    Returns
    -------

    time_series: pandas.DataFrame
        Timeseries of spacecraft dataset downloaded.
    """

    # Check if input is correct
    if sc_name not in ('psp', 'solo', 'ace'):
        sys.exit("Spacecraft name not recognised, use 'psp', 'solo' or 'ace'.")
    
    if ds_type not in ('mag', 'sw'):
        sys.exit("Dataset name not recognised, use 'mag' or 'sw'.")

    # Assign path of data
    data_path = 'data/' + sc_name + '/'
            
    # Assign dataset depending on input
    if sc_name == 'psp' and ds_type == 'mag':
        ds_name = 'PSP_FLD_L2_MAG_RTN_1MIN'
    elif sc_name == 'psp' and ds_type == 'sw':
        ds_name = 'PSP_SWP_SPC_L3I'

    if sc_name == 'solo' and ds_type == 'mag':
        ds_name = 'SOLO_L2_MAG-RTN-NORMAL-1-MINUTE'
    elif sc_name == 'solo' and ds_type == 'sw':
        ds_name = 'SOLO_L2_SWA-PAS-GRND-MOM'

    if sc_name == 'ace' and ds_type == 'mag':
        ds_name = 'AC_H2_MFI'
    elif sc_name == 'ace' and ds_type == 'sw':
        ds_name = 'AC_H2_SWE'
    
    # Unpack time window
    tstart, tend = parse_time(time_window[0]), parse_time(time_window[1])

    # Search and download for the desired dataset
    res_ds = Fido.search(a.Time(tstart, tend), a.cdaweb.Dataset(ds_name))
    files_ds = Fido.fetch(res_ds, path=data_path)

    # Create time series
    time_series = TimeSeries(files_ds, concatenate=True)
    time_series_df = time_series.to_dataframe()
    return time_series_df

def get_trajectory(timeseries_df, sc_name):

    """
    Obtain S/C trajectory information for a timeseries (PSP/SolO only).

    Parameters
    ----------
    time_series: pandas.DataFrame
        Timeseries of PSP/SolO dataset.

    sc_name: 'psp' or 'solo'
        String of the spacecraft name

    Returns
    -------

    sc_trajectory_hgs: astropy.SkyCoord
        Coordinates of SolO or PSP during timeseries, calculated in a Heliocentric frame using SPICE kernels.

    obstime: np.array
        Time series over which the trajectory and data is calculated.
    
    """
    # Check if input is correct
    if sc_name not in ('psp', 'solo'):
        sys.exit("Spacecraft name not recognised, use 'psp' or 'solo'.")
    
    # Initialise kernels
    solo_kernel_urls = [
        "spk/de421.bsp",
        "spk/solo_ANC_soc-orbit-stp_20200210-20301120_280_V1_00288_V01.bsp",
    ]
    solo_kernel_urls = [f"http://spiftp.esac.esa.int/data/SPICE/SOLAR-ORBITER/kernels/{url}"
                for url in solo_kernel_urls]

    psp_kernels = ["https://spdf.gsfc.nasa.gov/pub/data/psp/ephemeris/spice/ephemerides/spp_nom_20180812_20250831_v040_RO7.bsp"]

    kernels = solo_kernel_urls + psp_kernels

    kernel_files = [cache.download(url) for url in kernels]
    spice.initialize(kernel_files)

    # Get time window from time series
    obstime = timeseries_df.index

    # Calculate spacecraft trajectory around the sun
    if sc_name == 'psp':
        sc_traj = spice.get_body('SOLAR PROBE PLUS', obstime)
    else:
        sc_traj = spice.get_body('Solar Orbiter', obstime)

    sc_trajectory_hgs = sc_traj.heliographic_stonyhurst

    return sc_trajectory_hgs, obstime

def bin_distance(ds, counts=10):
    """Get SC params median and stdev binned by distance from a dataset.
    """
    # Create bins
    bins = np.arange(0, 1 + 1/counts, 1/counts)
    #bins = np.arange(-0.025, 1 + 1/20, 1/20) # centered on 0.05 AU
    ds['distance_bin'] = pd.cut(ds['Distance'], bins)

    # Group by distance bins and compute median, min, max
    sc_dist_med = ds.groupby('distance_bin', observed=False).median().reset_index()
    sc_dist_std = ds.groupby('distance_bin', observed=False).std().reset_index()

    return sc_dist_med, sc_dist_std