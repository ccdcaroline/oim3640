## Date: April 24, 2026 

**What I asked AI to do:**
- Build a Python program that takes a place name, uses APIs to find its location, and then finds the nearest MBTA stop with some basic info.

**What I didn't understand in the generated code:** 
- The quote(place_name) part was new to me. I didn’t know why the place name had to be changed before being used in the URL.
- I didn’t fully understand how the API response is structured, especially lines like data.get("features", []) and features[0]["center"]. It wasn’t obvious how the code knows where to find latitude and longitude.
- The requests.get(url, params=params) part was also a little confusing, especially how the params dictionary gets added to the URL automatically.

**What I learned:** 
- quote() makes sure the place name is formatted correctly for a URL (like replacing spaces with %20), so the API request works properly.
- API responses come back as JSON, which is basically a nested dictionary
- The params dictionary in requests.get() is automatically converted into URL query parameters, which makes the code cleaner and easier to read.


## Date: April 24, 2026 

**What I asked AI to do:**
- Turn my MBTA stop finder into a Flask web app where the user can type in a place and get the nearest MBTA stop.

**What I didn't understand in the generated code:**
- eI was also confused by request.form.get("place") because I did not realize it gets the user’s answer from the HTML form.
- The try and except parts were a little confusing because there are different types of errors being handled. 
- I also was confused why only North Station would work when I would type in a location. 

**What I learned:**
- Flask can take what the user types into HTML and use it in Python.
- The app uses Mapbox to turn the place into coordinates, then uses the MBTA API to find the closest stop.
- try and except help the app show a helpful error message instead of crashing.
- The result page uses Flask variables to display the place, stop name, and wheelchair accessibility.