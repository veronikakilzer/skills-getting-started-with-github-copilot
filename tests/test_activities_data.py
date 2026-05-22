def test_activities_have_required_fields(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()

    for name, details in activities.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)
