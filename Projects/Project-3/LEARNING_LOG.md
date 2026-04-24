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




**What I asked AI to do:**
- e.g., "Generate a function to parse CSV files"

**What I didn't understand in the generated code:**
- e.g., "The `with` statement for file handling was new to me"

**What I learned:**
- e.g., "Context managers automatically close files even if an error occurs"