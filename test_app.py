import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Home route test
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'version': '1.0'}

# Fahrenheit to Celsius
@pytest.mark.parametrize("temp, expected", [(212, 100.0), (32, 0.0), (-40, -40.0)])
def test_convert_temp_f_to_c(client, temp, expected):
    response = client.get(f'/convert-temp?temp={temp}&scale=fahrenheit&target_scale=celsius')
    assert response.status_code == 200
    assert response.json['converted_temp'] == pytest.approx(expected, rel=1e-2)

# Celsius to Fahrenheit
@pytest.mark.parametrize("temp, expected", [(100, 212.0), (0, 32.0), (-40, -40.0)])
def test_convert_temp_c_to_f(client, temp, expected):
    response = client.get(f'/convert-temp?temp={temp}&scale=celsius&target_scale=fahrenheit')
    assert response.status_code == 200
    assert response.json['converted_temp'] == pytest.approx(expected, rel=1e-2)

# Kelvin to Celsius
@pytest.mark.parametrize("temp, expected", [(273.15, 0.0), (373.15, 100.0), (233.15, -40.0)])
def test_convert_temp_k_to_c(client, temp, expected):
    response = client.get(f'/convert-temp?temp={temp}&scale=kelvin&target_scale=celsius')
    assert response.status_code == 200
    assert response.json['converted_temp'] == pytest.approx(expected, rel=1e-2)

# Kelvin to Fahrenheit
@pytest.mark.parametrize("temp, expected", [(273.15, 32.0), (373.15, 212.0), (233.15, -40.0)])
def test_convert_temp_k_to_f(client, temp, expected):
    response = client.get(f'/convert-temp?temp={temp}&scale=kelvin&target_scale=fahrenheit')
    assert response.status_code == 200
    assert response.json['converted_temp'] == pytest.approx(expected, rel=1e-2)

# Invalid scale handling
def test_convert_temp_invalid_scale(client):
    response = client.get('/convert-temp?temp=100&scale=unknown&target_scale=celsius')
    assert response.status_code == 400
    assert 'error' in response.json
