from pathlib import Path

import pytest

import power_system_simulation.validate_power_system_simulation as pss

DATA_PATH = Path(__file__).parent / "data"
DATA_EXCEPTION_SET = DATA_PATH / "Exception_test_data"

# wrong metadata
metadata_transformers = DATA_EXCEPTION_SET / "meta_data_transformers.json"
metadata_Sources = DATA_EXCEPTION_SET / "meta_data_source.json"

# wrong Input network
input_network_feeders = DATA_EXCEPTION_SET / "input_network_data_feederID.json"
input_network_feederTransformer = DATA_EXCEPTION_SET / "input_network_data_feederTransformer.json"
input_network_EV = DATA_EXCEPTION_SET / "input_network_data_EV.json"


# correct input data
metadata = DATA_EXCEPTION_SET / "meta_data.json"
input_network = DATA_EXCEPTION_SET / "input_network_data.json"
active_power_profile = DATA_EXCEPTION_SET / "active_power_profile.parquet"
reactive_power_profile = DATA_EXCEPTION_SET / "reactive_power_profile.parquet"
ev_active_power_profile = DATA_EXCEPTION_SET / "ev_active_power_profile.parquet"


def test_TooManyTransformers():
    with pytest.raises(pss.TooManyTransformers):
        pss.validate_power_system_simulation(input_network, metadata_transformers, ev_active_power_profile)


def test_TooManySources():
    with pytest.raises(pss.TooManySources):
        pss.validate_power_system_simulation(input_network, metadata_Sources, ev_active_power_profile)


def test_NotAllFeederIDsareValid():
    with pytest.raises(pss.NotAllFeederIDsareValid):
        pss.validate_power_system_simulation(input_network_feeders, metadata, ev_active_power_profile)


def test_TransformerAndFeedersNotConnected():
    with pytest.raises(pss.TransformerAndFeedersNotConnected):
        pss.validate_power_system_simulation(
            input_network_feederTransformer,
            metadata,
            ev_active_power_profile,
        )


def test_TooFewEVs():
    with pytest.raises(pss.TooFewEVs):
        pss.validate_power_system_simulation(input_network_EV, metadata, ev_active_power_profile)
