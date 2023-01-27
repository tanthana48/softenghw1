import requests



def test_create_machine():
    url = "http://127.0.0.1:5000/create-machine"

    data = {
        "name": "test",
        "location": "test"
    }

    r = requests.post(url, data=data)

    assert r.json() == {'message': 'Success'}


def test_edit_machine():
    url = "http://127.0.0.1:5000/edit-machine"

    data = {
        "machine_id": "1",
        "name": "test2"
    }

    r = requests.post(url, data=data)

    assert r.json() == {'message': 'Success'}


def test_delete_machine():
    url = "http://127.0.0.1:5000/delete-machine/5"

    r = requests.get(url)

    assert r.json() == {'message': 'Success'}


def test_add_product():
    url = "http://127.0.0.1:5000/add-product"

    data = {
        "machine_id": "2",
        "product_name": "sprite",
        "amount": "10"
    }

    r = requests.post(url, data=data)

    assert r.json() == {'message': 'Success'}


def test_edit_product():
    url = "http://127.0.0.1:5000/edit-product"

    data = {
        "product_id": "1",
        "amount": "10"
    }

    r = requests.post(url, data=data)

    assert r.json() == {'message': 'Success'}


def test_remove_product():
    url = "http://127.0.0.1:5000/remove-product/1"

    r = requests.get(url)

    assert r.json() == {'message': 'Success'}


if __name__ == '__main__':
    test_create_machine()
    test_edit_machine()
    test_delete_machine()
    test_add_product()
    test_edit_product()
    test_remove_product()
