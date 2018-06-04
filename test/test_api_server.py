import requests


# This test behaves randomly...
# def test_search_simple():
#     query = 'http://localhost:8085/api/search?q=emp'
#
#     response = requests.get(query).json()
#     print response
#
#     assert len(response['docs']) == 10
#     assert len(response['docs']) == response['hits']


def test_search_with_path():
    query = 'http://localhost:8085/api/search?q=emp&path=ClassicModels'
    response = requests.get(query).json()

    assert len(response['docs']) == 2
    assert len(response['docs']) == response['hits']
