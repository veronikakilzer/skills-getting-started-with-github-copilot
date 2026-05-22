import urllib.parse


def test_get_root_redirect(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location") == "/static/index.html"


def test_get_all_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect at least one known activity
    assert "Chess Club" in data


def test_signup_successful(client):
    activity = "Chess Club"
    email = "tester@example.com"
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_student(client):
    activity = "Chess Club"
    email = "dup@example.com"
    # first signup
    r1 = client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    assert r1.status_code == 200
    # duplicate
    r2 = client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    assert r2.status_code == 400


def test_signup_nonexistent_activity(client):
    resp = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    assert resp.status_code == 404


def test_unregister_successful(client):
    activity = "Programming Class"
    email = "remove-me@example.com"
    # ensure present
    r1 = client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    assert r1.status_code == 200

    r2 = client.delete(f"/activities/{urllib.parse.quote(activity)}/participants", params={"email": email})
    assert r2.status_code == 200
    assert "Unregistered" in r2.json().get("message", "")

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_not_participant(client):
    resp = client.delete("/activities/Chess%20Club/participants", params={"email": "not-in-list@example.com"})
    assert resp.status_code == 404


def test_unregister_nonexistent_activity(client):
    resp = client.delete("/activities/NoSuch/participants", params={"email": "a@b.com"})
    assert resp.status_code == 404
