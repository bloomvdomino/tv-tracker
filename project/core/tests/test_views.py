from django.urls import reverse


class TestHealthCheckView:
    def test_get(self, client):
        response = client.get(reverse("core:health_check"))

        assert response.status_code == 200
        assert response.json()["data"] == "Ok"
