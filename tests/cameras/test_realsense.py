#!/usr/bin/env python

# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Example of running a specific test:
# ```bash
# pytest tests/cameras/test_opencv.py::test_connect
# ```

from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from lerobot.cameras.configs import Cv2Rotation
from lerobot.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError

pytest.importorskip("pyrealsense2")

from lerobot.cameras.realsense import RealSenseCamera, RealSenseCameraConfig

TEST_ARTIFACTS_DIR = Path(__file__).parent.parent / "artifacts" / "cameras"
BAG_FILE_PATH = TEST_ARTIFACTS_DIR / "test_rs.bag"

# NOTE(Steven): For some reason these tests take ~20sec in macOS but only ~2sec in Linux.


def mock_rs_config_enable_device_from_file(rs_config_instance, _sn):
    return rs_config_instance.enable_device_from_file(str(BAG_FILE_PATH), repeat_playback=True)


def mock_rs_config_enable_device_bad_file(rs_config_instance, _sn):
    return rs_config_instance.enable_device_from_file("non_existent_file.bag", repeat_playback=True)


@pytest.fixture(name="patch_realsense", autouse=True)
def fixture_patch_realsense():
    """Automatically mock pyrealsense2.config.enable_device for all tests."""
    with patch(
        "pyrealsense2.config.enable_device", side_effect=mock_rs_config_enable_device_from_file
    ) as mock:
        yield mock


@pytest.fixture
def make_camera(request):
    def create_camera(config):
        camera = RealSenseCamera(config)

        def disconnect_if_connected():
            if camera.is_connected:
                camera.disconnect()

        request.addfinalizer(disconnect_if_connected)
        return camera

    return create_camera


def test_abc_implementation(make_camera):
    """Instantiation should raise an error if the class doesn't implement abstract methods/properties."""
    config = RealSenseCameraConfig(serial_number_or_name="042")
    _ = make_camera(config)


def test_connect(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042")
    camera = make_camera(config)

    camera.connect(warmup=False)
    assert camera.is_connected


def test_connect_already_connected(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042")
    camera = make_camera(config)
    camera.connect(warmup=False)

    with pytest.raises(DeviceAlreadyConnectedError):
        camera.connect(warmup=False)


def test_connect_invalid_camera_path(make_camera, patch_realsense):
    patch_realsense.side_effect = mock_rs_config_enable_device_bad_file
    config = RealSenseCameraConfig(serial_number_or_name="042")
    camera = make_camera(config)

    with pytest.raises(ConnectionError):
        camera.connect(warmup=False)


def test_invalid_width_connect(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042", width=99999, height=480, fps=30)
    camera = make_camera(config)

    with pytest.raises(ConnectionError):
        camera.connect(warmup=False)


def test_read(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042", width=640, height=480, fps=30)
    camera = make_camera(config)
    camera.connect(warmup=False)

    img = camera.read()
    assert isinstance(img, np.ndarray)


# TODO(Steven): Fix this test for the latest version of pyrealsense2.
@pytest.mark.skip("Skipping test: pyrealsense2 version > 2.55.1.6486")
def test_read_depth(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042", width=640, height=480, fps=30, use_depth=True)
    camera = make_camera(config)
    camera.connect(warmup=False)

    img = camera.read_depth(timeout_ms=2000)  # NOTE(Steven): Reading depth takes longer in CI environments.
    assert isinstance(img, np.ndarray)


def test_read_before_connect(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042")
    camera = make_camera(config)

    with pytest.raises(DeviceNotConnectedError):
        _ = camera.read()


def test_disconnect(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042")
    camera = make_camera(config)
    camera.connect(warmup=False)

    camera.disconnect()

    assert not camera.is_connected


def test_disconnect_before_connect(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042")
    camera = make_camera(config)

    with pytest.raises(DeviceNotConnectedError):
        camera.disconnect()


def test_async_read(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042", width=640, height=480, fps=30)
    camera = make_camera(config)
    camera.connect(warmup=False)

    img = camera.async_read()

    assert camera.thread is not None
    assert camera.thread.is_alive()
    assert isinstance(img, np.ndarray)


def test_async_read_timeout(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042", width=640, height=480, fps=30)
    camera = make_camera(config)
    camera.connect(warmup=False)

    with pytest.raises(TimeoutError):
        camera.async_read(timeout_ms=0)


def test_async_read_before_connect(make_camera):
    config = RealSenseCameraConfig(serial_number_or_name="042")
    camera = make_camera(config)

    with pytest.raises(DeviceNotConnectedError):
        _ = camera.async_read()


@pytest.mark.parametrize(
    "rotation",
    [
        Cv2Rotation.NO_ROTATION,
        Cv2Rotation.ROTATE_90,
        Cv2Rotation.ROTATE_180,
        Cv2Rotation.ROTATE_270,
    ],
    ids=["no_rot", "rot90", "rot180", "rot270"],
)
def test_rotation(make_camera, rotation):
    config = RealSenseCameraConfig(serial_number_or_name="042", rotation=rotation)
    camera = make_camera(config)
    camera.connect(warmup=False)

    img = camera.read()
    assert isinstance(img, np.ndarray)

    if rotation in (Cv2Rotation.ROTATE_90, Cv2Rotation.ROTATE_270):
        assert camera.width == 480
        assert camera.height == 640
        assert img.shape[:2] == (640, 480)
    else:
        assert camera.width == 640
        assert camera.height == 480
        assert img.shape[:2] == (480, 640)
