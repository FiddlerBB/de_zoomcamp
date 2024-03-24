if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    data = data.rename(
        columns={
            "components.co": "carbon_onoxide_CO",
            "components.no": "nitric_oxide_NO",
            "components.no2": "nitrogen_ioxide_NO2",
            "components.o3": "ozone_O3",
            "components.so2": "sulfur_ioxide_SO2",
            "components.pm2_5": "PM2_5",
            "components.pm10": "PM10",
            "components.nh3": "NH3",
            "main.aqi": "aqi",
            "coord.lon": 'longitude',
            "coord.lat": 'latitude'
        }
    )

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
